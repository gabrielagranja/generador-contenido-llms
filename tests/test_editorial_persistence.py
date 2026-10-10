from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from apps.api.editorial_planning import EIGHTY_TWENTY, create_plan
from apps.api.editorial_review import EditorialReviewService
from apps.api.editorial_store import EditorialContentStore, EditorialPlanStore
from tests.test_editorial_planning import END, START, make_content


def test_content_survives_a_fresh_store_instance() -> None:
    with TemporaryDirectory() as directory:
        database_path = Path(directory) / "editorial.sqlite3"
        content = EditorialReviewService.approve(
            make_content(), reviewer_ref="reviewer-fixture"
        )

        EditorialContentStore(database_path).create(content)
        restored = EditorialContentStore(database_path).get(content.content_id)

    assert restored == content
    assert restored is not None
    assert restored.state == "approved_final"
    assert restored.review is not None
    assert restored.draft.evidence_provenance == content.draft.evidence_provenance


def test_plan_survives_a_fresh_store_instance() -> None:
    with TemporaryDirectory() as directory:
        database_path = Path(directory) / "editorial.sqlite3"
        plan = create_plan(EIGHTY_TWENTY, 4, starts_on=START, ends_on=END)
        first_store = EditorialPlanStore(database_path)
        plan_id = first_store.create_id()
        first_store.save(plan_id, plan)

        restored = EditorialPlanStore(database_path).get(plan_id)

    assert restored == plan
    assert restored is not None
    assert restored.strategy_version == EIGHTY_TWENTY.version
    assert restored.targets == plan.targets
