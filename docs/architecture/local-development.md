# Local development contract

This document describes the runnable foundation currently delivered by Issue #21.
It intentionally does not describe provider-backed generation or social publishing.

## Prerequisites

- Python 3.11 or newer;
- Node.js 22 and npm;
- Git.

The API uses FastAPI, Pydantic, Uvicorn and LangChain Core. The web client uses
Next.js, React and TypeScript. The supported application test command is
`python -m pytest -q` from the repository root.

## Clean local setup

From a checkout of the repository:

```text
python -m venv .venv
```

Activate the virtual environment, then install the Python dependencies:

```text
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create the local environment file from the safe template:

```text
copy .env.example .env
```

`.env` is local-only and ignored by Git. The foundation defaults need no provider
credentials. Do not add API keys or tokens to `.env.example`, the browser bundle,
or the repository.

## Run the foundation

Use two terminals from the repository root.

Terminal 1 — API:

```text
python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
```

The API exposes `/readiness`, `/docs`, `/redoc` and `/openapi.json`.

Terminal 2 — web client:

```text
npm --prefix apps/web ci
npm --prefix apps/web run dev
```

Open `http://localhost:3000`. The client reads `NEXT_PUBLIC_API_BASE_URL`, which
defaults to `http://127.0.0.1:8000` when it is not set.

## Tests and build

```text
python -m pytest -q
python scripts/validate_sdd_contract.py
npm --prefix apps/web run build
```

The SDD harness installs `requirements.txt`, validates OpenSpec governance, and
uses `python -m pytest -q` as its configured application-test command.

## Repository structure

- `apps/api/`: FastAPI app, environment settings and the provider-neutral LangChain boundary;
- `apps/web/`: Next.js client and the readiness connection;
- `tests/`: governance, API, environment and boundary tests;
- `docs/architecture/`: system and local-development documentation;
- `openspec/changes/web-foundation/`: approved contract and task evidence;
- `.env.example`: safe, non-secret local configuration template.

## Current foundation boundary

The foundation provides local API readiness, OpenAPI documentation, safe
environment defaults, the LangChain Core boundary and a deterministic offline
mock adapter. Baseline tests use synthetic data and make no external provider
calls.

The following are not part of this phase: Groq or Gemini calls, RAG, content
generation, model comparison, OAuth, Instagram/Facebook publishing, images,
voice, LinkedIn, production hosting, multi-tenant behavior and Docker adoption.
