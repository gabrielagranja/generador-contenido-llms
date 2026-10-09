"use client";

import { useEffect, useMemo, useState } from "react";

type ReadinessState = "loading" | "ready" | "unavailable";
type ViewId = "dashboard" | "content-studio";
type BrandId = "panaderia" | "coll-amunt";
type CommerceId = "synthetic-a" | "synthetic-b";

type CommerceContext = {
  id: CommerceId;
  name: string;
  account: string;
  summary: string;
  sampleTopic: string;
  sampleAudience: string;
};

type BrandContext = {
  id: BrandId;
  name: string;
  account: string;
  avatar: string;
  summary: string;
  sampleTopic: string;
  sampleAudience: string;
  commerceOptions?: CommerceContext[];
};


type BriefForm = {
  objective: string;
  audience: string;
  platform: "Instagram" | "Facebook";
  format: "Reel" | "Carrusel" | "Publicación";
  campaign: string;
  restrictions: string;
};

type DraftPreparationStatus = "not-prepared" | "pending-review" | "brief-changed" | "changes-requested" | "approved";

type EditorialStatus = "draft" | "review" | "approved";

type DashboardItem = {
  id: string;
  title: string;
  date: string;
  platform: string;
  format: string;
  status?: EditorialStatus;
};

type DashboardActivity = {
  id: string;
  text: string;
  time: string;
};

type DashboardFixture = {
  drafts: number;
  review: number;
  approved: number;
  upcoming: DashboardItem[];
  activity: DashboardActivity[];
};

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const brandContexts: BrandContext[] = [
  {
    id: "panaderia",
    name: "Panadería La Plaza",
    account: "panaderialaplaza",
    avatar: "P",
    summary: "Marca independiente de panadería con producto artesano de elaboración diaria.",
    sampleTopic: "Nuestros panes recién horneados",
    sampleAudience: "Personas del barrio que buscan desayunos artesanos",
  },
  {
    id: "coll-amunt",
    name: "Coll Amunt!",
    account: "collamunt",
    avatar: "C",
    summary: "Marca de rutas y experiencias de montaña con contexto comercial seleccionable.",
    sampleTopic: "Planes de montaña para este fin de semana",
    sampleAudience: "Personas que disfrutan de rutas y naturaleza cerca de casa",
    commerceOptions: [
      {
        id: "synthetic-a",
        name: "Comercio sintético A",
        account: "collamunt_a",
        summary: "Contexto sintético A para demostrar una sede asociada a la marca.",
        sampleTopic: "Ruta de iniciación para este fin de semana",
        sampleAudience: "Personas que buscan una primera experiencia de montaña",
      },
      {
        id: "synthetic-b",
        name: "Comercio sintético B",
        account: "collamunt_b",
        summary: "Contexto sintético B para demostrar otra sede asociada a la marca.",
        sampleTopic: "Salida de grupo por caminos locales",
        sampleAudience: "Grupos que quieren descubrir rutas cercanas",
      },
    ],
  },
];

const dashboardFixtures: Record<string, DashboardFixture> = {
  panaderialaplaza: {
    drafts: 3,
    review: 2,
    approved: 5,
    upcoming: [
      { id: "plaza-1", title: "Pan del día: proceso artesano", date: "12 jun", platform: "Instagram", format: "Carrusel" },
      { id: "plaza-2", title: "Selección de desayunos", date: "14 jun", platform: "Facebook", format: "Publicación" },
    ],
    activity: [
      { id: "plaza-a1", text: "Borrador sintético actualizado: Pan del día", time: "Hoy, 09:40" },
      { id: "plaza-a2", text: "Contenido sintético aprobado para revisión final", time: "Ayer, 16:20" },
      { id: "plaza-a3", text: "Nuevo contenido añadido al calendario de ejemplo", time: "10 jun, 11:05" },
    ],
  },
  collamunt_a: {
    drafts: 2,
    review: 1,
    approved: 4,
    upcoming: [
      { id: "coll-a-1", title: "Ruta de iniciación: primeros pasos", date: "13 jun", platform: "Instagram", format: "Reel" },
    ],
    activity: [
      { id: "coll-a-a1", text: "Borrador sintético creado para el comercio A", time: "Hoy, 08:55" },
      { id: "coll-a-a2", text: "Contenido sintético enviado a revisión", time: "11 jun, 14:10" },
    ],
  },
  collamunt_b: {
    drafts: 1,
    review: 0,
    approved: 2,
    upcoming: [],
    activity: [],
  },
};

function DashboardSection({
  contextName,
  fixture,
  onOpenStudio,
}: {
  contextName: string;
  fixture: DashboardFixture;
  onOpenStudio: () => void;
}) {
  const editorialSummary = [
    { label: "Borradores", value: fixture.drafts, tone: "draft" },
    { label: "Pendientes de revisión", value: fixture.review, tone: "review" },
    { label: "Aprobados", value: fixture.approved, tone: "approved" },
  ];

  return (
    <section className="dashboard-section" aria-label={"Dashboard sintético de " + contextName}>
      <div className="dashboard-intro">
        <div>
          <div className="card-kicker">RESUMEN EDITORIAL</div>
          <h2>Estado del flujo de contenido</h2>
        </div>
        <span className="synthetic-label">Datos sintéticos · estado interno</span>
      </div>

      <div className="dashboard-summary">
        {editorialSummary.map((metric) => (
          <article className={"metric-card metric-" + metric.tone} key={metric.label}>
            <span className="metric-label">{metric.label}</span>
            <strong className="metric-value">{metric.value}</strong>
            <span className="metric-caption">Estado editorial interno</span>
          </article>
        ))}
      </div>

      <div className="dashboard-columns">
        <article className="dashboard-panel">
          <div className="panel-heading">
            <div>
              <div className="card-kicker">CALENDARIO DE EJEMPLO</div>
              <h3>Próximos contenidos</h3>
            </div>
            <span className="panel-note">Sin publicación automática</span>
          </div>
          {fixture.upcoming.length > 0 ? (
            <div className="dashboard-list">
              {fixture.upcoming.map((item) => (
                <div className="dashboard-row" key={item.id}>
                  <time className="dashboard-row-date">{item.date}</time>
                  <div className="dashboard-row-main">
                    <strong>{item.title}</strong>
                    <span>{item.platform} · {item.format}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="dashboard-empty">
              <strong>No hay próximos contenidos</strong>
              <span>Este contexto sintético todavía no tiene elementos en el calendario de ejemplo.</span>
            </div>
          )}
        </article>

        <article className="dashboard-panel">
          <div className="panel-heading">
            <div>
              <div className="card-kicker">TRAZA DE EJEMPLO</div>
              <h3>Actividad reciente</h3>
            </div>
            <span className="panel-note">Sin conexión externa</span>
          </div>
          {fixture.activity.length > 0 ? (
            <div className="activity-list">
              {fixture.activity.map((entry) => (
                <div className="activity-item" key={entry.id}>
                  <span className="activity-dot" aria-hidden="true" />
                  <div>
                    <strong>{entry.text}</strong>
                    <span>{entry.time} · actividad sintética</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="dashboard-empty">
              <strong>Sin actividad reciente</strong>
              <span>Este contexto sintético aún no registra cambios de ejemplo.</span>
            </div>
          )}
        </article>
      </div>

      <div className="dashboard-footer">
        <p className="social-boundary">
          Estas cifras representan estados internos del flujo editorial. No son métricas de redes, conexiones ni rendimiento social.
        </p>
        <button className="studio-access" type="button" onClick={onOpenStudio}>
          <span>
            <strong>Continuar en Content Studio</strong>
            <small>Acceso preparado · placeholder de próxima entrega</small>
          </span>
          <span aria-hidden="true">→</span>
        </button>
      </div>
    </section>
  );
}


const briefDefaults: Record<string, BriefForm> = {
  panaderialaplaza: {
    objective: "Presentar una novedad de producto artesano",
    audience: "Personas del barrio interesadas en desayunos artesanos",
    platform: "Instagram",
    format: "Carrusel",
    campaign: "Mañanas de barrio",
    restrictions: "Mantener un tono cercano y no prometer disponibilidad futura.",
  },
  collamunt_a: {
    objective: "Invitar a descubrir una ruta de iniciación",
    audience: "Personas que buscan una primera experiencia de montaña",
    platform: "Instagram",
    format: "Reel",
    campaign: "Primeros pasos",
    restrictions: "No presentar rutas reales ni datos de ubicación.",
  },
  collamunt_b: {
    objective: "Animar a planificar una salida de grupo",
    audience: "Grupos que quieren descubrir rutas cercanas",
    platform: "Facebook",
    format: "Publicación",
    campaign: "Salidas en compañía",
    restrictions: "Usar referencias genéricas y mantener el contenido como ejemplo.",
  },
};

function getBriefDefaults(account: string): BriefForm {
  return briefDefaults[account] ?? briefDefaults.panaderialaplaza;
}

function buildSyntheticCopy(contextName: string, brief: BriefForm): string {
  return [
    "Borrador de prototipo · datos sintéticos",
    "",
    brief.objective + " para " + contextName + ".",
    "",
    "Una idea para " + brief.audience.toLowerCase() + ": descubre una propuesta preparada para esta campaña de ejemplo.",
    "",
    "Campaña: " + brief.campaign,
    "Canal: " + brief.platform + " · Formato: " + brief.format,
  ].join("\n");
}

function ContentStudioSection({
  contextName,
  contextSummary,
  brief,
  previewCopy,
  preparationStatus,
  validationMessage,
  onBriefChange,
  onPreviewChange,
  onPrepareDraft,
  onApproveDraft,
  onRequestChanges,
  onResubmitDraft,
}: {
  contextName: string;
  contextSummary: string;
  brief: BriefForm;
  previewCopy: string;
  preparationStatus: DraftPreparationStatus;
  validationMessage: string;
  onBriefChange: (field: keyof BriefForm, value: string) => void;
  onPreviewChange: (value: string) => void;
  onPrepareDraft: () => void;
  onApproveDraft: () => void;
  onRequestChanges: () => void;
  onResubmitDraft: () => void;
}) {
  return (
    <section className="studio-section" aria-label={"Content Studio para " + contextName}>
      <div className="studio-heading">
        <div>
          <div className="card-kicker">BRIEF GUIADO · PROTOTIPO LOCAL</div>
          <h2>Prepara una idea de contenido</h2>
          <p>{contextSummary}</p>
        </div>
        <span className="synthetic-label">Sin LLM · sin persistencia</span>
      </div>

      <div className="studio-grid">
        <article className="brief-card">
          <div className="panel-heading">
            <div>
              <div className="card-kicker">PASO 1</div>
              <h3>Define el brief</h3>
            </div>
            <span className="panel-note">Contexto heredado</span>
          </div>
          <div className="brief-fields">
            <label>
              Objetivo
              <textarea value={brief.objective} onChange={(event) => onBriefChange("objective", event.target.value)} rows={3} />
            </label>
            <label>
              Audiencia
              <input value={brief.audience} onChange={(event) => onBriefChange("audience", event.target.value)} />
            </label>
            <div className="brief-field-row">
              <label>
                Canal
                <select value={brief.platform} onChange={(event) => onBriefChange("platform", event.target.value)}>
                  <option value="Instagram">Instagram</option>
                  <option value="Facebook">Facebook</option>
                </select>
              </label>
              <label>
                Formato MVP
                <select value={brief.format} onChange={(event) => onBriefChange("format", event.target.value)}>
                  <option value="Reel">Reel</option>
                  <option value="Carrusel">Carrusel</option>
                  <option value="Publicación">Publicación</option>
                </select>
              </label>
            </div>
            <label>
              Campaña
              <input value={brief.campaign} onChange={(event) => onBriefChange("campaign", event.target.value)} />
            </label>
            <label>
              Restricciones
              <textarea value={brief.restrictions} onChange={(event) => onBriefChange("restrictions", event.target.value)} rows={3} />
            </label>
          </div>
          <button className="prepare-draft-button" type="button" onClick={onPrepareDraft}>
            {preparationStatus === "pending-review" ? "Preparar otro borrador" : preparationStatus === "brief-changed" ? "Actualizar borrador" : "Preparar borrador"}
          </button>
          {validationMessage && <p className="brief-validation" role="alert">{validationMessage}</p>}
          <p className="studio-context-note">Marca y comercio se heredan del selector del App Shell; no hay selectores duplicados.</p>
        </article>

        <article className="preview-card">
          <div className="panel-heading">
            <div>
              <div className="card-kicker">PASO 2</div>
              <h3>Vista previa</h3>
            </div>
            <span className="prototype-pill">Borrador de prototipo</span>
          </div>
          <div className="preview-context">
            <strong>{contextName}</strong>
            <span>{brief.platform} · {brief.format} · contenido sintético</span>
          </div>
          <p className={`draft-review-status draft-review-${preparationStatus}`} aria-live="polite">
            {preparationStatus === "pending-review"
              ? "Pendiente de revisión humana"
              : preparationStatus === "brief-changed"
                ? "El brief cambió · actualiza el borrador antes de revisarlo"
                : preparationStatus === "changes-requested"
                  ? "Cambios solicitados · edita el copy y vuelve a enviarlo"
                  : preparationStatus === "approved"
                    ? "Aprobado en este prototipo · estado solo local"
                    : "Completa el brief y prepara un borrador local"}
          </p>
          {preparationStatus === "pending-review" && (
            <div className="review-actions" aria-label="Decisión de revisión">
              <button className="review-action-button" type="button" onClick={onRequestChanges}>Solicitar cambios</button>
              <button className="review-action-button review-approve-button" type="button" onClick={onApproveDraft}>Aprobar en prototipo</button>
            </div>
          )}
          {preparationStatus === "changes-requested" && (
            <button className="review-action-button review-resubmit-button" type="button" onClick={onResubmitDraft}>Enviar cambios a revisión</button>
          )}
          <label className="preview-label" htmlFor="preview-copy">
            {preparationStatus === "approved" ? "Copy aprobado · solo lectura" : "Copy editable localmente"}
          </label>
          <textarea
            id="preview-copy"
            className="preview-copy"
            value={previewCopy}
            onChange={(event) => onPreviewChange(event.target.value)}
            placeholder="El borrador sintético aparecerá aquí al preparar el brief."
            readOnly={preparationStatus === "approved"}
            rows={12}
          />
          <p className="preview-boundary">La aprobación solo cambia el estado local del prototipo. No habilita exportación ni publicación.</p>
        </article>
      </div>
    </section>
  );
}

export default function Home() {
  const [readiness, setState] = useState<ReadinessState>("loading");
  const [view, setView] = useState<ViewId>("dashboard");
  const [brandId, setBrandId] = useState<BrandId>("panaderia");
  const [commerceId, setCommerceId] = useState<CommerceId | null>(null);

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
    () => brandContexts.find((context) => context.id === brandId) ?? brandContexts[0],
    [brandId],
  );
  const activeCommerce = useMemo(
    () => brand.commerceOptions?.find((commerce) => commerce.id === commerceId),
    [brand, commerceId],
  );
  const activeContext = activeCommerce ?? brand;
  const dashboard = dashboardFixtures[activeContext.account] ?? dashboardFixtures.panaderialaplaza;
  const contextName = activeCommerce ? brand.name + " · " + activeCommerce.name : brand.name;
  const [brief, setBrief] = useState<BriefForm>(() => getBriefDefaults(activeContext.account));
  const [previewCopy, setPreviewCopy] = useState("");
  const [preparationStatus, setPreparationStatus] = useState<DraftPreparationStatus>("not-prepared");
  const [validationMessage, setValidationMessage] = useState("");

  useEffect(() => {
    const nextBrief = getBriefDefaults(activeContext.account);
    setBrief(nextBrief);
    setPreviewCopy("");
    setPreparationStatus("not-prepared");
    setValidationMessage("");
  }, [activeContext.account, contextName]);

  const statusLabel = {
    loading: "Comprobando API…",
    ready: "API lista",
    unavailable: "API no disponible",
  }[readiness];

  function updateBrief(field: keyof BriefForm, value: string) {
    setBrief((current) => ({ ...current, [field]: value }));
    setPreparationStatus((current) => current === "pending-review" || current === "approved" ? "brief-changed" : current);
    setValidationMessage("");
  }

  function prepareDraft() {
    const requiredFields = [brief.objective, brief.audience, brief.campaign];
    if (requiredFields.some((value) => !value.trim())) {
      setValidationMessage("Completa el objetivo, la audiencia y la campaña para preparar el borrador.");
      return;
    }

    setPreviewCopy(buildSyntheticCopy(contextName, brief));
    setPreparationStatus("pending-review");
    setValidationMessage("");
  }

  function approveDraft() {
    setPreparationStatus((current) => current === "pending-review" ? "approved" : current);
  }

  function requestDraftChanges() {
    setPreparationStatus((current) => current === "pending-review" ? "changes-requested" : current);
  }

  function resubmitDraftForReview() {
    setPreparationStatus((current) => current === "changes-requested" ? "pending-review" : current);
  }

  function selectBrand(nextBrandId: BrandId) {
    const nextBrand = brandContexts.find((context) => context.id === nextBrandId);
    if (!nextBrand) return;
    setBrandId(nextBrand.id);
    setCommerceId(nextBrand.commerceOptions?.[0]?.id ?? null);
  }

  function selectCommerce(nextCommerceId: CommerceId) {
    if (brand.commerceOptions?.some((commerce) => commerce.id === nextCommerceId)) {
      setCommerceId(nextCommerceId);
    }
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

          {brand.commerceOptions && (
            <div className="context-field">
              <label className="context-label" htmlFor="commerce-select">Comercio asociado</label>
              <select
                id="commerce-select"
                className="commerce-select"
                value={commerceId ?? ""}
                onChange={(event) => selectCommerce(event.target.value as CommerceId)}
              >
                {brand.commerceOptions.map((option) => (
                  <option key={option.id} value={option.id}>
                    {option.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {!brand.commerceOptions && (
            <p className="independent-brand-note">Marca independiente · sin comercio asociado</p>
          )}
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
              Contexto activo: <strong>{contextName}</strong>. El contenido de esta vista es local y sintético.
            </p>
          </section>

          {view === "dashboard" ? (
            <DashboardSection
              contextName={contextName}
              fixture={dashboard}
              onOpenStudio={() => setView("content-studio")}
            />
          ) : (
            <ContentStudioSection
              contextName={contextName}
              contextSummary={activeContext.summary}
              brief={brief}
              previewCopy={previewCopy}
              preparationStatus={preparationStatus}
              validationMessage={validationMessage}
              onBriefChange={updateBrief}
              onPreviewChange={setPreviewCopy}
              onPrepareDraft={prepareDraft}
              onApproveDraft={approveDraft}
              onRequestChanges={requestDraftChanges}
              onResubmitDraft={resubmitDraftForReview}
            />
          )}

          <footer className="page-footer">
            <span>RAG permanece fuera de la navegación principal.</span>
            <span>API local: <code>{apiBaseUrl}/readiness</code></span>
          </footer>
        </div>
      </section>
    </main>
  );
}
