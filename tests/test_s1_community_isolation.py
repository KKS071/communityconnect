"""S-1 Community isolation: tests written from AC-1..AC-5 in docs/design/S-1.md
before any app code existed. Expected values come from the criteria, not from code."""

import pytest

from conftest import B_MARK, COMMUNITIES

B = COMMUNITIES["B"]
NOT_FOUND = {"detail": "Not found"}
NOT_AUTH = {"detail": "Not authenticated"}

# Outsiders to B, one per role (design doc D18): each holds that role in another community.
OUTSIDERS = ["res_a", "board_a", "mgr_ac"]

ITEM_PATHS = {
    "ticket": ("/tickets/{}", "ticket_b"),
    "document": ("/documents/{}", "doc_b"),
    "announcement": ("/announcements/{}", "ann_b"),
}
LIST_PATHS = [
    "/communities/{}/tickets",
    "/communities/{}/documents",
    "/communities/{}/announcements",
]


def assert_not_found_without_b_data(resp):
    assert resp.status_code == 404
    assert resp.json() == NOT_FOUND
    assert B_MARK not in resp.text


# AC-1
@pytest.mark.parametrize("user", OUTSIDERS)
@pytest.mark.parametrize("item_type", list(ITEM_PATHS))
def test_ac1_outsider_item_read_blocked(world, user, item_type):
    template, item_key = ITEM_PATHS[item_type]
    resp = world.get(template.format(world.items[item_key]), user)
    assert_not_found_without_b_data(resp)


# AC-1 (R3): blocked looks exactly like "does not exist"
@pytest.mark.parametrize("item_type", list(ITEM_PATHS))
def test_ac1_blocked_item_is_indistinguishable_from_missing(world, item_type):
    template, item_key = ITEM_PATHS[item_type]
    foreign = world.get(template.format(world.items[item_key]), "res_a")
    missing = world.get(template.format(999999), "res_a")
    assert foreign.status_code == missing.status_code == 404
    assert foreign.content == missing.content


# AC-2
@pytest.mark.parametrize("user", OUTSIDERS)
@pytest.mark.parametrize("template", LIST_PATHS)
def test_ac2_outsider_list_read_blocked(world, user, template):
    resp = world.get(template.format(B), user)
    assert_not_found_without_b_data(resp)


# AC-3
@pytest.mark.parametrize("user", ["res_a", "board_a", "mgr_ac"])
def test_ac3_member_lists_announcements_and_documents(world, user):
    a = COMMUNITIES["A"]
    anns = world.get(f"/communities/{a}/announcements", user)
    docs = world.get(f"/communities/{a}/documents", user)
    assert anns.status_code == 200 and docs.status_code == 200
    assert [x["id"] for x in anns.json()] == [world.items["ann_a"]]
    assert [x["id"] for x in docs.json()] == [world.items["doc_a"]]
    for item in anns.json() + docs.json():
        assert item["community_id"] == a
    assert B_MARK not in anns.text + docs.text


# AC-3
def test_ac3_resident_sees_own_ticket(world):
    a = COMMUNITIES["A"]
    resp = world.get(f"/communities/{a}/tickets", "res_a")
    assert resp.status_code == 200
    ids = [t["id"] for t in resp.json()]
    assert world.items["ticket_a_res"] in ids
    assert all(t["community_id"] == a for t in resp.json())
    one = world.get(f"/tickets/{world.items['ticket_a_res']}", "res_a")
    assert one.status_code == 200
    assert one.json()["title"] == "A leaky faucet"


# AC-3
def test_ac3_manager_sees_all_community_tickets(world):
    a = COMMUNITIES["A"]
    resp = world.get(f"/communities/{a}/tickets", "mgr_ac")
    assert resp.status_code == 200
    assert sorted(t["id"] for t in resp.json()) == sorted(
        [world.items["ticket_a_res"], world.items["ticket_a_res2"]]
    )


# AC-4
def test_ac4_manager_switches_communities_with_one_token(world):
    a, c = COMMUNITIES["A"], COMMUNITIES["C"]
    mine = world.get("/me/communities", "mgr_ac")
    assert mine.status_code == 200
    assert [x["id"] for x in mine.json()] == [a, c]

    a_tickets = world.get(f"/communities/{a}/tickets", "mgr_ac")
    c_tickets = world.get(f"/communities/{c}/tickets", "mgr_ac")
    assert a_tickets.status_code == c_tickets.status_code == 200
    assert {t["community_id"] for t in a_tickets.json()} == {a}
    assert [t["id"] for t in c_tickets.json()] == [world.items["ticket_c"]]


# AC-5
ALL_ENDPOINTS = [
    "/me/communities",
    "/communities/{B}/tickets",
    "/communities/{B}/documents",
    "/communities/{B}/announcements",
    "/tickets/{ticket_b}",
    "/documents/{doc_b}",
    "/announcements/{ann_b}",
]
BAD_HEADERS = {
    "missing": {},
    "unknown_token": {"Authorization": "Bearer " + "0" * 32},
    "wrong_scheme": {"Authorization": "Token TOKEN"},
    "lowercase_bearer": {"Authorization": "bearer TOKEN"},
    "empty_token": {"Authorization": "Bearer "},
}


@pytest.mark.parametrize("endpoint", ALL_ENDPOINTS)
@pytest.mark.parametrize("variant", list(BAD_HEADERS))
def test_ac5_unauthenticated_request_blocked(world, endpoint, variant):
    path = endpoint.format(B=B, **world.items)
    headers = {
        k: v.replace("TOKEN", world.tokens["res_b"]) for k, v in BAD_HEADERS[variant].items()
    }
    resp = world.get(path, headers=headers)
    assert resp.status_code == 401
    assert resp.json() == NOT_AUTH
    assert B_MARK not in resp.text


# --- Rule and edge-case tests from the design doc (not AC tests) ---

def test_r4_board_only_document_never_returned(world):
    a = COMMUNITIES["A"]
    for user in ["res_a", "board_a", "mgr_ac"]:
        listing = world.get(f"/communities/{a}/documents", user)
        assert world.items["doc_a_board"] not in [d["id"] for d in listing.json()]
        one = world.get(f"/documents/{world.items['doc_a_board']}", user)
        assert one.status_code == 404 and one.json() == NOT_FOUND


def test_r5_resident_cannot_read_neighbours_ticket(world):
    resp = world.get(f"/tickets/{world.items['ticket_a_res2']}", "res_a")
    assert resp.status_code == 404 and resp.json() == NOT_FOUND


def test_edge3_admin_without_membership(world):
    assert world.get("/me/communities", "admin").json() == []
    resp = world.get(f"/communities/{COMMUNITIES['A']}/tickets", "admin")
    assert resp.status_code == 404


@pytest.mark.parametrize("bad_id", [0, -1, 2**63])
def test_d10_out_of_range_ids_are_404(world, bad_id):
    resp = world.get(f"/tickets/{bad_id}", "mgr_ac")
    assert resp.status_code == 404 and resp.json() == NOT_FOUND


def test_d9_auth_checked_before_path_validation(world):
    resp = world.get("/tickets/abc")
    assert resp.status_code == 401


def test_d17_trailing_slash_is_404(world):
    resp = world.get("/me/communities/", "res_a")
    assert resp.status_code == 404
