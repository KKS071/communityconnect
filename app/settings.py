"""Named settings for values the interviews have not settled (S-1 D8, D16).

Code reads these as ``settings.NAME`` when it uses them, never copies them at import, so tests
can override them. Never hard-code these values anywhere else (AGENTS.md)."""

import os

# Provisional defaults (S-1 D8); not settled by any interview.
REQUEST_CATEGORIES = ["Plumbing", "Electrical", "Landscaping", "Pool", "Other"]
MAX_DESCRIPTION_CHARS = 2000

# PostgreSQL connection and schema (S-1 D12, D16).
DATABASE_URL = os.environ.get(
    "COMMUNITYCONNECT_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/communityconnect",
)
DATABASE_SCHEMA = os.environ.get("COMMUNITYCONNECT_DB_SCHEMA", "public")
