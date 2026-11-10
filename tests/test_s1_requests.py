"""S-1 Submit and track a maintenance request (docs/design/S-1.md).

Tests written before the code (handout 6b). Expected values come from the acceptance criteria
in docs/requirements/backlog.md and the exact messages in the design doc. Values the interviews
did not settle are read from app.settings, never hard-coded (S-1 D8).
"""

import re
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app import settings
from tests.helpers import count_requests, set_status

NOT_FOUND = {"detail": "Not found"}
UNKNOWN_USER = {"detail": "Unknown user"}
INVALID_BODY = {"detail": "Invalid request body"}
TIME_FORMAT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")  # D5


def ids(resp):
    return [r["id"] for r in resp.json()]


# ---------------------------------------------------------------- acceptance criteria


def test_ac1_resident_submits_request_shown_as_open(world):
    # AC-1: R1 of unit 12 in Mountain Ridge submits "Plumbing" / "Kitchen sink leaks".
    # REQUEST_CATEGORIES[0] is the provisional "Plumbing" (D8); tests never hard-code it.
    category = settings.REQUEST_CATEGORIES[0]
    before = datetime.now(timezone.utc).date().isoformat()
    resp = world.submit("R1", "MR", category, "Kitchen sink leaks")
    after = datetime.now(timezone.utc).date().isoformat()
    assert resp.status_code == 201

    listed = world.list_requests("R1", "MR")
    assert listed.status_code == 200
    mine = [r for r in listed.json() if r["id"] == resp.json()["id"]]
    assert len(mine) == 1
    req = mine[0]
    assert req["status"] == "Open"
    assert req["category"] == category
    assert req["description"] == "Kitchen sink leaks"
    assert req["created_at"][:10] in {before, after}  # "today's date" (UTC, D5)


@pytest.mark.parametrize("description", ["", "   "], ids=["empty", "only-spaces"])
def test_ac2_blank_description_rejected_and_list_unchanged(world, description):
    # AC-2: an empty or space-only description shows "Description is required",
    # and R1's request list is unchanged.
    world.submit("R1", "MR", description="Earlier request")
    before = world.list_requests("R1", "MR").json()

    resp = world.submit("R1", "MR", description=description)
    assert resp.status_code == 422
    assert resp.json() == {"detail": "Description is required"}
    assert world.list_requests("R1", "MR").json() == before


def test_ac3_other_community_resident_does_not_see_request(world):
    # AC-3: R1 has an Open request in Mountain Ridge; R2 of Pine Hollow opens the
    # Pine Hollow list and R1's request is not listed.
    rid = world.submit("R1", "MR").json()["id"]
    world.submit("R2", "PH", description="Hallway light out")
    resp = world.list_requests("R2", "PH")
    assert resp.status_code == 200
    assert rid not in ids(resp)
    assert all(r["community_id"] == world.communities["PH"] for r in resp.json())


def test_ac4_other_community_direct_id_returns_not_found(world):
    # AC-4: R2 of Pine Hollow opens R1's request by its ID: "Not found" and none of
    # the request's details.
    rid = world.submit("R1", "MR", description="Kitchen sink leaks").json()["id"]
    resp = world.get(f"/requests/{rid}", "R2")
    assert resp.status_code == 404
    assert resp.json() == NOT_FOUND
    assert "Kitchen sink leaks" not in resp.text


def test_ac5_neighbor_in_same_community_does_not_see_request(world):
    # AC-5: R3 of unit 20 in Mountain Ridge opens the Mountain Ridge list and R1's
    # request is not listed (D2).
    rid = world.submit("R1", "MR").json()["id"]
    resp = world.list_requests("R3", "MR")
    assert resp.status_code == 200
    assert rid not in ids(resp)


def test_ac6_resident_sees_in_progress_status(world):
    # AC-6: R1's request has status In progress; R1 opens it and sees In progress.
    rid = world.submit("R1", "MR").json()["id"]
    set_status(rid, "In progress")
    resp = world.get(f"/requests/{rid}", "R1")
    assert resp.status_code == 200
    assert resp.json()["status"] == "In progress"


# ---------------------------------------------------------------- rules (section 6)


def test_r1_resident_of_two_communities_sees_each_list_separately(world):
    from app import seed

    both = seed.create_user()
    seed.add_membership(both, world.communities["MR"], "resident", world.units["MR-14"])
    seed.add_membership(both, world.communities["PH"], "resident", world.units["PH-3"])
    world.users["BOTH"] = both
    in_mr = world.submit("BOTH", "MR").json()["id"]
    in_ph = world.submit("BOTH", "PH").json()["id"]
    assert ids(world.list_requests("BOTH", "MR")) == [in_mr]
    assert ids(world.list_requests("BOTH", "PH")) == [in_ph]


@pytest.mark.parametrize("viewer", ["R3", "R2", "R4", "M1", "M2", "B1", "ADMIN", "NOBODY"])
def test_r2_hidden_request_answers_exactly_like_missing_one(world, viewer):
    rid = world.submit("R1", "MR").json()["id"]
    hidden = world.get(f"/requests/{rid}", viewer)
    missing = world.get(f"/requests/{rid + 1000}", viewer)
    assert hidden.status_code == missing.status_code == 404
    assert hidden.content == missing.content
    assert hidden.json() == NOT_FOUND


@pytest.mark.parametrize("caller", ["R2", "M1", "M2", "B1", "ADMIN", "NOBODY"])
def test_r3_r5_post_by_non_resident_is_404_and_nothing_saved(world, caller):
    before = count_requests()
    resp = world.submit(caller, "MR")
    assert resp.status_code == 404
    assert resp.json() == NOT_FOUND
    assert count_requests() == before


def test_r4_new_request_is_open_first_and_total_grows_by_one(world):
    world.submit("R1", "MR", description="First")
    before = count_requests()
    new = world.submit("R1", "MR", description="Second").json()
    assert count_requests() == before + 1
    assert new["status"] == "Open"
    assert ids(world.list_requests("R1", "MR"))[0] == new["id"]


@pytest.mark.parametrize(
    "body",
    [
        {"description": "x"},
        {"category": None, "description": "x"},
        {"category": 5, "description": "x"},
        {"category": "Other", "description": ["x"]},
    ],
    ids=["missing-category", "null-category", "number-category", "list-description"],
)
def test_r5_rejected_post_saves_nothing(world, body):
    before = count_requests()
    resp = world.post(f"/communities/{world.communities['MR']}/requests", "R1", json=body)
    assert resp.status_code == 422
    assert resp.json() == INVALID_BODY
    assert count_requests() == before


# ---------------------------------------------------------------- edge cases and decisions


@pytest.mark.parametrize(
    "header",
    [None, "", "abc", "0", "007", "+1", " 1", "1 ", "1.0", "999999"],
    ids=["missing", "empty", "text", "zero", "leading-zeros", "plus", "lead-space",
         "trail-space", "decimal", "unknown"],
)
@pytest.mark.parametrize("endpoint", ["list", "item", "post"])
def test_d1_unknown_caller_gets_401(world, header, endpoint):
    rid = world.submit("R1", "MR").json()["id"]
    headers = {} if header is None else {"X-User-Id": header}
    mr = world.communities["MR"]
    if endpoint == "list":
        resp = world.client.get(f"/communities/{mr}/requests", headers=headers)
    elif endpoint == "item":
        resp = world.client.get(f"/requests/{rid}", headers=headers)
    else:
        resp = world.client.post(f"/communities/{mr}/requests", headers=headers,
                                 json={"category": settings.REQUEST_CATEGORIES[0], "description": "x"})
    assert resp.status_code == 401
    assert resp.json() == UNKNOWN_USER


def test_d14_repeated_user_header_gets_401(world):
    mr = world.communities["MR"]
    uid = str(world.users["R1"])
    resp = world.client.get(f"/communities/{mr}/requests",
                            headers=[("X-User-Id", uid), ("X-User-Id", uid)])
    assert resp.status_code == 401
    assert resp.json() == UNKNOWN_USER


@pytest.mark.parametrize("bad_id", ["abc", "0", "-1", "1.5", "9223372036854775808"])
def test_d14_bad_path_ids_are_404(world, bad_id):
    for resp in (
        world.get(f"/requests/{bad_id}", "R1"),
        world.get(f"/communities/{bad_id}/requests", "R1"),
        world.post(f"/communities/{bad_id}/requests", "R1",
                   json={"category": settings.REQUEST_CATEGORIES[0], "description": "x"}),
    ):
        assert resp.status_code == 404
        assert resp.json() == NOT_FOUND


def test_d6_caller_checked_before_path(world):
    resp = world.client.get("/requests/abc", headers={"X-User-Id": "999999"})
    assert resp.status_code == 401


def test_d6_membership_checked_before_body(world):
    resp = world.post(f"/communities/{world.communities['MR']}/requests", "M1", json=[1, 2])
    assert resp.status_code == 404


def test_d6_description_checked_before_category(world):
    resp = world.submit("R1", "MR", category="No such category", description="  ")
    assert resp.json() == {"detail": "Description is required"}


@pytest.mark.parametrize(
    "content",
    [b"", b"not json", b"[]", b"null", b'"text"', b'{"category": "x",'],
    ids=["empty", "not-json", "array", "null", "string", "truncated"],
)
def test_d15_body_must_be_a_json_object(world, content):
    before = count_requests()
    resp = world.client.post(
        f"/communities/{world.communities['MR']}/requests",
        headers={**world.h("R1"), "Content-Type": "application/json"},
        content=content,
    )
    assert resp.status_code == 422
    assert resp.json() == INVALID_BODY
    assert count_requests() == before


def test_d15_description_too_long(world):
    resp = world.submit("R1", "MR", description="x" * (settings.MAX_DESCRIPTION_CHARS + 1))
    assert resp.status_code == 422
    assert resp.json() == {"detail": "Description is too long"}


def test_d9_description_that_fits_only_after_trimming_is_stored_trimmed(world):
    text = "y" * settings.MAX_DESCRIPTION_CHARS
    resp = world.submit("R1", "MR", description=f"  {text}  ")
    assert resp.status_code == 201
    assert resp.json()["description"] == text


@pytest.mark.parametrize("variant", ["lower", "padded", "empty", "unknown"])
def test_d4_category_must_match_exactly(world, variant):
    first = settings.REQUEST_CATEGORIES[0]
    category = {"lower": first.lower() if first.lower() != first else first.upper(),
                "padded": f" {first} ", "empty": "", "unknown": "No such category"}[variant]
    assert category not in settings.REQUEST_CATEGORIES
    resp = world.submit("R1", "MR", category=category)
    assert resp.status_code == 422
    assert resp.json() == {"detail": "Unknown category"}


def test_d5_created_at_format_and_requestout_shape(world):
    resp = world.submit("R1", "MR")
    body = resp.json()
    assert set(body) == {"id", "community_id", "unit_id", "category", "description",
                         "status", "created_at"}
    assert TIME_FORMAT.match(body["created_at"])
    assert world.get(f"/requests/{body['id']}", "R1").json() == body  # D21


def test_d11_list_is_newest_first(world):
    first = world.submit("R1", "MR", description="one").json()["id"]
    second = world.submit("R1", "MR", description="two").json()["id"]
    third = world.submit("R1", "MR", description="three").json()["id"]
    assert ids(world.list_requests("R1", "MR")) == [third, second, first]


@pytest.mark.parametrize("viewer", ["M1", "B1", "ADMIN", "NOBODY", "R2"])
def test_d10_d19_list_for_non_residents_is_404(world, viewer):
    resp = world.list_requests(viewer, "MR")
    assert resp.status_code == 404
    assert resp.json() == NOT_FOUND


def test_d20_unit_comes_from_membership_and_extra_fields_ignored(world):
    resp = world.post(
        f"/communities/{world.communities['MR']}/requests", "R1",
        json={"category": settings.REQUEST_CATEGORIES[0], "description": "x",
              "unit_id": world.units["MR-20"], "status": "Resolved"},
    )
    assert resp.status_code == 201
    assert resp.json()["unit_id"] == world.units["MR-12"]
    assert resp.json()["status"] == "Open"


def test_d20_resident_with_no_requests_gets_empty_list(world):
    resp = world.list_requests("R3", "MR")
    assert resp.status_code == 200
    assert resp.json() == []


def test_d21_wrong_method_and_unknown_path(world):
    mr = world.communities["MR"]
    wrong = world.client.delete(f"/communities/{mr}/requests", headers=world.h("R1"))
    assert wrong.status_code == 405
    assert wrong.json() == {"detail": "Method Not Allowed"}
    unknown = world.get("/no-such-path", "R1")
    assert unknown.status_code == 404
    assert unknown.json() == NOT_FOUND


def test_d12_requests_survive_a_restart(world):
    from app.main import create_app

    rid = world.submit("R1", "MR").json()["id"]
    fresh = TestClient(create_app())
    resp = fresh.get(f"/requests/{rid}", headers=world.h("R1"))
    assert resp.status_code == 200


def test_d17_seed_rejects_resident_without_unit_in_same_community(world):
    from app import seed

    user = seed.create_user()
    with pytest.raises(ValueError):
        seed.add_membership(user, world.communities["MR"], "resident")
    with pytest.raises(ValueError):
        seed.add_membership(user, world.communities["MR"], "resident", world.units["PH-3"])
