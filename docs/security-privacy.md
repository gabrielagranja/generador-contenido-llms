# Security and Privacy Boundaries

Authority: canonical security and privacy baseline.
Bootstrap issue: #37.

- Never commit API keys, OAuth tokens, environment files or personal access tokens.
- Persist OAuth tokens only through an approved encrypted server-side mechanism.
- Request only permissions needed for the selected Instagram action.
- Use synthetic or explicitly approved business data in provider free-tier evaluation.
- Treat generated content as a draft until human review.
- Do not publish to Instagram without explicit confirmation for that post.
- Log decisions and test evidence without exposing client secrets or unapproved business information.
- External API tests MUST use mocks by default; real smoke tests require an authorized test account.
- Any privacy or permission change requires a new Issue and approved OpenSpec contract.
