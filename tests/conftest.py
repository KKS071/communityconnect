"""Shared fixtures for the S-1 and S-6 tests.

Sample data from docs/requirements/backlog.md: communities Mountain Ridge, Pine Hollow and
Elm Court. R1 lives in unit 12 and R3 in unit 20 of Mountain Ridge; R2 lives in Pine Hollow;
R4 lives in Elm Court. M1 manages Mountain Ridge and Pine Hollow; M2 manages only Elm Court.
B1 is a board member of Mountain Ridge. Data is created with app/seed.py (S-1 D13, D17).
Each test gets a new, empty PostgreSQL schema in the test database, dropped afterwards
(S-1 D12, D18).
"""

import os
import uuid

from dataclasses import dataclass, field

import pytest
from fastapi.testclient import TestClient


@dataclass
class World:
    client: TestClient
    users: dict = field(default_factory=dict)        # "R1" -> user id
    communities: dict = field(default_factory=dict)  # "MR" -> community id
    units: dict = field(default_factory=dict)        # "MR-12" -> unit id

    def h(self, user):
        """Headers for a signed-in user (S-1 D1)."""
        return {"X-User-Id": str(self.users[user])}

    def get(self, path, user):
        return self.client.get(path, headers=self.h(user))

    def post(self, path, user, json=None, **kw):
        return self.client.post(path, headers=self.h(user), json=json, **kw)

    def submit(self, user, community, category=None, description="Kitchen sink leaks"):
        from app import settings

        body = {
            "category": category if category is not None else settings.REQUEST_CATEGORIES[0],
            "description": description,
        }
        return self.post(f"/communities/{self.communities[community]}/requests", user, json=body)

    def list_requests(self, user, community):
        return self.get(f"/communities/{self.communities[community]}/requests", user)


TEST_DATABASE_URL = os.environ.get(
    "COMMUNITYCONNECT_TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/communityconnect_test",
)


@pytest.fixture
def db_schema(monkeypatch):
    """Point the app at a new schema in the test database; drop it after the test (D18)."""
    import psycopg

    from app import settings

    schema = f"test_{uuid.uuid4().hex}"
    try:
        admin = psycopg.connect(TEST_DATABASE_URL, autocommit=True, connect_timeout=5)
    except psycopg.OperationalError as exc:
        pytest.fail(f"PostgreSQL test database not reachable at {TEST_DATABASE_URL}: {exc}",
                    pytrace=False)
    monkeypatch.setattr(settings, "DATABASE_URL", TEST_DATABASE_URL)
    monkeypatch.setattr(settings, "DATABASE_SCHEMA", schema)
    try:
        yield schema
    finally:
        admin.execute(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE')
        admin.close()


@pytest.fixture
def world(db_schema):
    from app import seed
    from app.main import create_app

    client = TestClient(create_app())
    w = World(client=client)
    w.communities = {
        "MR": seed.create_community("Mountain Ridge"),
        "PH": seed.create_community("Pine Hollow"),
        "EC": seed.create_community("Elm Court"),
    }
    c = w.communities
    w.units = {
        "MR-12": seed.create_unit(c["MR"], "12"),
        "MR-20": seed.create_unit(c["MR"], "20"),
        "MR-14": seed.create_unit(c["MR"], "14"),
        "PH-3": seed.create_unit(c["PH"], "3"),
        "EC-5": seed.create_unit(c["EC"], "5"),
    }
    u = w.units
    for name in ["R1", "R2", "R3", "R4", "M1", "M2", "B1", "ADMIN", "NOBODY"]:
        w.users[name] = seed.create_user()
    seed.add_membership(w.users["R1"], c["MR"], "resident", u["MR-12"])
    seed.add_membership(w.users["R3"], c["MR"], "resident", u["MR-20"])
    seed.add_membership(w.users["R2"], c["PH"], "resident", u["PH-3"])
    seed.add_membership(w.users["R4"], c["EC"], "resident", u["EC-5"])
    seed.add_membership(w.users["M1"], c["MR"], "manager")
    seed.add_membership(w.users["M1"], c["PH"], "manager")
    seed.add_membership(w.users["M2"], c["EC"], "manager")
    seed.add_membership(w.users["B1"], c["MR"], "board_member")
    seed.add_membership(w.users["ADMIN"], c["MR"], "admin")
    # NOBODY exists as a user but has no membership anywhere.
    return w
