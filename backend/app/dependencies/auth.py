"""
TEMPORARY stand-in for Person A's real Authentication module.

Right now this just returns a hardcoded fake user so Track C
(Roadmaps, Mock Hackathons, Workspace) can be built and tested
independently, without waiting on real Auth/JWT to exist.

Once Person A's real `get_current_user` (with real JWT decoding) is
ready, DELETE this file's body and import theirs instead — every
route below already calls this the same way real auth will be called,
so swapping it out later is a one-line change per route, not a rewrite.
"""
from typing import TypedDict


class CurrentUser(TypedDict):
    id: int
    email: str


def get_current_user() -> CurrentUser:
    # Fake logged-in user for local development only.
    return {"id": 1, "email": "dev-user@example.com"}
