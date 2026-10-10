# Design

Add a narrow plans API client in the web domain. Calendar renders persisted plan items grouped by plan and uses each plan range as its date context. Content Studio only invokes the existing save endpoint for an already validated EditorialPlan payload; plan construction rules remain in the backend domain. A failed fetch or save stays visible and cannot change review or publication state.
