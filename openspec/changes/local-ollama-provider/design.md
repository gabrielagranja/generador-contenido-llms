# Design

Extend LlmSettings with the optional local URL/model. Build an Ollama adapter using the already installed httpx dependency behind the existing TextGenerator application boundary. POST /api/chat with stream=false; forward the full existing prompt as user content and options.temperature/options.num_predict. Enforce the configured timeout and validate textual message.content.

Keep provider-neutral drafting and RAG intact. Normalize transport/protocol failures at the API boundary to a safe 503 response. Resolve provider/model metadata from the same configured selection. Retain deterministic mock as the credential-free default and Groq as an explicit supported choice. Never silently invoke a cloud provider after local failure.

Document that the server must run where the API can reach it and the user supplies an already installed model. Persistence and calendar reuse existing EditorialContentStore/editorial_planning in subsequent contracts.
