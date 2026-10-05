"use client";

import { useEffect, useState } from "react";

type ReadinessState = "loading" | "ready" | "unavailable";

type ReadinessResponse = {
  status: "ready";
  service: "api";
};

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export default function Home() {
  const [state, setState] = useState<ReadinessState>("loading");

  useEffect(() => {
    const controller = new AbortController();

    async function checkReadiness() {
      try {
        const response = await fetch(`${apiBaseUrl}/readiness`, {
          signal: controller.signal,
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error("Readiness request failed");
        }

        const payload = (await response.json()) as ReadinessResponse;
        if (payload.status !== "ready" || payload.service !== "api") {
          throw new Error("Unexpected readiness response");
        }

        setState("ready");
      } catch {
        if (!controller.signal.aborted) {
          setState("unavailable");
        }
      }
    }

    void checkReadiness();
    return () => controller.abort();
  }, []);

  const statusLabel = {
    loading: "Comprobando API…",
    ready: "API lista",
    unavailable: "API no disponible",
  }[state];

  return (
    <main className="page-shell">
      <section className="card" aria-labelledby="page-title">
        <p className="eyebrow">Web foundation</p>
        <h1 id="page-title">Generador de contenido</h1>
        <p className="intro">
          Cliente base conectado al endpoint local de readiness de la API.
        </p>
        <div className={`status status-${state}`} role="status" aria-live="polite">
          <span className="status-dot" aria-hidden="true" />
          {statusLabel}
        </div>
        <p className="endpoint">
          API local: <code>{apiBaseUrl}/readiness</code>
        </p>
      </section>
    </main>
  );
}
