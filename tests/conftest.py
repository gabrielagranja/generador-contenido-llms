import pytest

from apps.api.auth import require_session
from apps.api.main import app


@pytest.fixture(autouse=True)
def signed_in_session(monkeypatch: pytest.MonkeyPatch):
    """Existing API tests exercise editorial behaviour, not sign-in: provide a session.

    Authentication itself is covered in ``test_auth.py``, which removes this override.
    """

    # Provider-specific tests replace or clear this value explicitly. Every
    # other test runs against the deterministic local adapter, independent of
    # a developer's .env configuration.
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    app.dependency_overrides[require_session] = lambda: "test-user"
    yield
    app.dependency_overrides.pop(require_session, None)
