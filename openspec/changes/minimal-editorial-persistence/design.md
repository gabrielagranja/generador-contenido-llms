# Design

Add a small SQLite repository behind the existing EditorialContentStore interface and introduce an EditorialPlanStore that serializes the existing Pydantic models as validated JSON. The configured database path defaults to an ignored local directory, creates its tables on first use and is replaced by a temporary file in tests.

Keep review transitions inside EditorialReviewService and plan validation inside editorial_planning. API routes continue to own validation; storage only preserves and restores validated objects. A subsequent calendar integration reads persisted plans through a narrow API without duplicating planning logic.
