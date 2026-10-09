"use client";

import { useEffect, useMemo, useState } from "react";

type ReadinessState = "loading" | "ready" | "unavailable";
type ViewId = "dashboard" | "content-studio";
type BrandId = "panaderia" | "coll-amunt";
type CommerceId = "plaza" | "coll-amunt";

type BrandContext = {
  id: BrandId;
  commerceId: CommerceId;
  name: string;
  account: string;
  avatar: string;
  summary: string;
  sampleTopic: string;
  sampleAudience: string;
};

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const brandContexts: BrandContext[] = [
  {
    id: "panaderia",
    commerceId: "plaza",
    name: "Panadería La Plaza",
    account: "panaderialaplaza",
    avatar: "P",
    summary: "Panadería de barrio con producto artesano de elaboración diaria.",
    sampleTopic: "Nuestros panes recién horneados",
    sampleAudience: "Personas del barrio que buscan desayunos artesanos",
  },
  {
    id: "coll-amunt",
    commerceId: "coll-amunt",
    name: "Coll Amunt!",
    account: "collamunt",
    avatar: "C",
    summary: "Proyecto local de rutas y experiencias para disfrutar la montaña.",
    sampleTopic: "Planes de montaña para este fin de semana",
    sampleAudience: "Personas que disfrutan de rutas y naturaleza cerca de casa",
  },
];

const commerceNames: Record<CommerceId, string> = {
  plaza: "Panadería La Plaza",
  "coll-amunt": "Coll Amunt!",
};

export default function Home() {
  const [readiness, setState] = useState<ReadinessState>("loading");
  const [view, setView] = useState<ViewId>("dashboard");
  const [brandId, setBrandId] = useState<BrandId>("panaderia");
  const [commerceId, setCommerceId] = useState<CommerceId>("plaza");
  const [commerceMenuOpen, setCommerceMenuOpen] = useState(false);

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

        const payload = (await response.json()) as {
          status: "ready";
          service: "api";
        };

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

  const brand = useMemo(
    () =>
      brandContexts.find(
        (context) => context.id === brandId && context.commerceId === commerceId,
      ) ?? brandContexts[0],
    [brandId, commerceId],
  );

  const statusLabel = {
    loading: "Comprobando API…",
    ready: "API lista",
    unavailable: "API no disponible",
  }[readiness];

  function selectBrand(nextBrandId: BrandId) {
    const nextBrand = brandContexts.find((context) => context.id === nextBrandId);
    if (!nextBrand) return;
    setBrandId(nextBrand.id);
    setCommerceId(nextBrand.commerceId);
  }

  function selectCommerce(nextCommerceId: CommerceId) {
    const nextBrand = brandContexts.find(
      (context) => context.commerceId === nextCommerceId,
    );
    if (!nextBrand) return;
    setCommerceId(nextCommerceId);
    setBrandId(nextBrand.id);
    setCommerceMenuOpen(false);
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand-lockup">
          <span className="brand-mark" aria-hidden="true">e.</span>
          <span>estudio<span className="brand-dot">.</span></span>
        </div>

        <p className="sidebar-label">ESPACIO DE TRABAJO</p>
        <div className="context-stack">
          <div className="context-field">
            <span className="context-label">Comercio</span>
            <div className="commerce-picker">
              <button
                className="commerce-trigger"
                type="button"
                aria-expanded={commerceMenuOpen}
                aria-haspopup="listbox"
                onClick={() => setCommerceMenuOpen((open) => !open)}
              >
                <span className="context-avatar">{brand.avatar}</span>
                <span className="context-copy">
                  <strong>{commerceNames[commerceId]}</strong>
                  <small>Contexto sintético</small>
                </span>
                <span aria-hidden="true">⌄</span>
              </button>
              {commerceMenuOpen && (
                <div className="commerce-menu" role="listbox" aria-label="Seleccionar comercio">
                  {(Object.entries(commerceNames) as [CommerceId, string][]).map(
                    ([id, name]) => (
                      <button
                        className="commerce-option"
                        type="button"
                        role="option"
                        aria-selected={id === commerceId}
                        key={id}
                        onClick={() => selectCommerce(id)}
                      >
                        <span className="context-avatar">{id === "plaza" ? "P" : "C"}</span>
                        <span className="context-copy">
                          <strong>{name}</strong>
                          <small>Comercio de ejemplo</small>
                        </span>
                      </button>
                    ),
                  )}
                </div>
              )}
            </div>
          </div>

          <div className="context-field">
            <label className="context-label" htmlFor="brand-select">Marca</label>
            <select
              id="brand-select"
              className="brand-select"
              value={brand.id}
              onChange={(event) => selectBrand(event.target.value as BrandId)}
            >
              {brandContexts.map((option) => (
                <option key={option.id} value={option.id}>
                  {option.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <nav className="main-nav" aria-label="Navegación principal">
          <button
            className={`nav-item ${view === "dashboard" ? "active" : ""}`}
            type="button"
            onClick={() => setView("dashboard")}
          >
            <span className="nav-icon">▦</span>
            Dashboard
          </button>
          <button
            className={`nav-item ${view === "content-studio" ? "active" : ""}`}
            type="button"
            onClick={() => setView("content-studio")}
          >
            <span className="nav-icon">✦</span>
            Content Studio
          </button>
          <button className="nav-item muted" type="button" onClick={() => setView("dashboard")}>
            <span className="nav-icon">▤</span>
            Borradores
            <span className="nav-count">—</span>
          </button>
          <button className="nav-item muted" type="button" onClick={() => setView("dashboard")}>
            <span className="nav-icon">◷</span>
            Historial
            <span className="nav-count">—</span>
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="boundary-card">
            <span className="boundary-icon">✦</span>
            <strong>Espacio de trabajo local</strong>
            <p>Las vistas de producto se incorporarán en próximas entregas.</p>
          </div>
          <div className="profile-row">
            <span className="profile-avatar">GG</span>
            <span className="context-copy"><strong>Gabriela</strong><small>Content manager</small></span>
          </div>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div className="breadcrumb">
            Estudio <span>/</span> <strong>{view === "dashboard" ? "Dashboard" : "Content Studio"}</strong>
          </div>
          <div className="topbar-actions">
            <span className={`readiness-pill readiness-${readiness}`}>
              <span aria-hidden="true" />
              {statusLabel}
            </span>
            <span className="prototype-pill">Shell · Iteración 0</span>
          </div>
        </header>

        <div className="content">
          <section className="hero-block" aria-labelledby="page-title">
            <p className="eyebrow">APP SHELL · MULTIBRAND</p>
            <h1 id="page-title">{view === "dashboard" ? "Tu espacio de trabajo" : "Content Studio"}</h1>
            <p className="subheading">
              Contexto activo: <strong>{brand.name}</strong>. Esta iteración valida la estructura,
              la navegación y el aislamiento visual de datos sintéticos.
            </p>
          </section>

          <section className="workspace-grid" aria-label="Estado del shell">
            <article className="context-card">
              <div className="card-kicker">CONTEXTO ACTIVO</div>
              <div className="card-heading">
                <span className="large-avatar">{brand.avatar}</span>
                <div>
                  <h2>{brand.name}</h2>
                  <p>@{brand.account}</p>
                </div>
              </div>
              <p className="context-summary">{brand.summary}</p>
              <dl className="context-details">
                <div><dt>Tema de ejemplo</dt><dd>{brand.sampleTopic}</dd></div>
                <div><dt>Audiencia</dt><dd>{brand.sampleAudience}</dd></div>
              </dl>
              <p className="synthetic-note">Datos sintéticos de interfaz · sin RAG ni servicios externos.</p>
            </article>

            <article className="placeholder-card" aria-label={`${view} pendiente`}>
              <div className="card-kicker">PRÓXIMA ENTREGA</div>
              <h2>{view === "dashboard" ? "Dashboard" : "Content Studio"}</h2>
              <p>Placeholder explícito: esta vista aún no implementa métricas, borradores ni generación de contenido.</p>
              <span className="status-badge">Pendiente</span>
            </article>
          </section>

          <footer className="page-footer">
            <span>RAG permanece fuera de la navegación principal.</span>
            <span>API local: <code>{apiBaseUrl}/readiness</code></span>
          </footer>
        </div>
      </section>
    </main>
  );
}
