"use client";

import { useEffect, useMemo, useState } from "react";

type ReadinessState = "loading" | "ready" | "unavailable";
type ViewId = "dashboard" | "drafts" | "history" | "content-studio";
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

type DraftPreparationStatus = "not-prepared" | "draft" | "pending-review" | "brief-changed" | "changes-requested" | "approved";

type EditorialStatus = "draft" | "review" | "approved";

type DashboardItem = {
  id: string;
  title: string;
  date: string;
  platform: string;
  format: string;
  status?: EditorialStatus;
};

type LocalDraft = {
  id: string;
  title: string;
  platform: BriefForm["platform"];
  format: BriefForm["format"];
  status: EditorialStatus;
  updatedAt: string;
  brief: BriefForm;
  copy: string;
};

type DraftFilter = "all" | EditorialStatus;

type HistoryEntry = {
  id: string;
  text: string;
  time: string;
  status: EditorialStatus;
  draftId: string;
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

const draftFixtures: Record<string, LocalDraft[]> = {
  panaderialaplaza: [
    {
      id: "plaza-draft-pan-artesano",
      title: "Una mañana de pan artesano",
      platform: "Instagram",
      format: "Carrusel",
      status: "draft",
      updatedAt: "Hoy · 09:40",
      brief: { ...briefDefaults.panaderialaplaza, objective: "Presentar una idea de desayuno artesano" },
      copy: `Borrador sintético · Panadería La Plaza\n\nUna idea de desayuno artesano para compartir con el barrio.\n\nContenido de ejemplo, pendiente de edición.`,
    },
    {
      id: "plaza-review-desayunos",
      title: "Ideas para empezar el día",
      platform: "Facebook",
      format: "Publicación",
      status: "review",
      updatedAt: "Ayer · 16:20",
      brief: { ...briefDefaults.panaderialaplaza, platform: "Facebook", format: "Publicación", campaign: "Mañanas de barrio" },
      copy: `Borrador sintético · Panadería La Plaza\n\nDescubre una propuesta de desayuno para disfrutar con calma.\n\nContenido de ejemplo, pendiente de revisión humana.`,
    },
    {
      id: "plaza-approved-temporada",
      title: "Sabores de temporada",
      platform: "Instagram",
      format: "Publicación",
      status: "approved",
      updatedAt: "8 oct · 12:15",
      brief: { ...briefDefaults.panaderialaplaza, format: "Publicación", campaign: "Sabores del barrio" },
      copy: `Texto sintético aprobado en el prototipo para ilustrar el estado editorial.`,
    },
  ],
  collamunt_a: [
    {
      id: "coll-a-draft-inicio",
      title: "Primeros pasos en la montaña",
      platform: "Instagram",
      format: "Reel",
      status: "draft",
      updatedAt: "Hoy · 08:55",
      brief: { ...briefDefaults.collamunt_a },
      copy: `Borrador sintético · Coll Amunt! · Comercio A\n\nUna invitación genérica a descubrir una primera experiencia de montaña.\n\nSin rutas ni ubicaciones reales.`,
    },
    {
      id: "coll-a-review-grupo",
      title: "Una salida para compartir",
      platform: "Facebook",
      format: "Publicación",
      status: "review",
      updatedAt: "11 jun · 14:10",
      brief: { ...briefDefaults.collamunt_a, platform: "Facebook", format: "Publicación", campaign: "Salidas en compañía" },
      copy: `Borrador sintético · Coll Amunt! · Comercio A\n\nUna propuesta genérica para organizar una salida en grupo.\n\nPendiente de revisión humana.`,
    },
  ],
  collamunt_b: [
    {
      id: "coll-b-draft-group",
      title: "Planifica tu próxima salida",
      platform: "Facebook",
      format: "Publicación",
      status: "draft",
      updatedAt: "10 jun · 10:30",
      brief: { ...briefDefaults.collamunt_b },
      copy: `Borrador sintético · Coll Amunt! · Comercio B\n\nUna propuesta genérica para planificar una salida en grupo.`,
    },
  ],
};

const historyFixtures: Record<string, HistoryEntry[]> = {
  panaderialaplaza: [
    { id: "plaza-history-1", text: "Se editó un borrador local.", time: "Hoy · 09:40", status: "draft", draftId: "plaza-draft-pan-artesano" },
    { id: "plaza-history-2", text: "El contenido se envió a revisión humana.", time: "Ayer · 16:20", status: "review", draftId: "plaza-review-desayunos" },
    { id: "plaza-history-3", text: "Se marcó como aprobado en el prototipo.", time: "8 oct · 12:15", status: "approved", draftId: "plaza-approved-temporada" },
  ],
  collamunt_a: [
    { id: "coll-a-history-1", text: "Se preparó un borrador local.", time: "Hoy · 08:55", status: "draft", draftId: "coll-a-draft-inicio" },
    { id: "coll-a-history-2", text: "El contenido se envió a revisión humana.", time: "11 jun · 14:10", status: "review", draftId: "coll-a-review-grupo" },
  ],
  collamunt_b: [
    { id: "coll-b-history-1", text: "Se creó un borrador de ejemplo.", time: "10 jun · 10:30", status: "draft", draftId: "coll-b-draft-group" },
  ],
};

function HistorySection({
  contextName,
  entries,
  drafts,
  onOpenDraft,
}: {
  contextName: string;
  entries: HistoryEntry[];
  drafts: LocalDraft[];
  onOpenDraft: (draft: LocalDraft) => void;
}) {
  const [filter, setFilter] = useState<DraftFilter>("all");
  const visibleEntries = filter === "all" ? entries : entries.filter((entry) => entry.status === filter);
  const filterOptions: { id: DraftFilter; label: string }[] = [
    { id: "all", label: "Todos" },
    { id: "draft", label: "Borradores" },
    { id: "review", label: "En revisión" },
    { id: "approved", label: "Aprobados" },
  ];
  const statusLabels: Record<EditorialStatus, string> = {
    draft: "Borrador",
    review: "En revisión",
    approved: "Aprobado en prototipo",
  };

  return (
    <section className="history-section" aria-label={"Historial de " + contextName}>
      <div className="history-heading">
        <div>
          <div className="card-kicker">ACTIVIDAD EDITORIAL · EJEMPLOS</div>
          <h2>Historial de {contextName}</h2>
          <p>Actividad sintética del contexto seleccionado, sin conexiones externas ni persistencia.</p>
        </div>
        <span className="synthetic-label">Datos de ejemplo</span>
      </div>

      <div className="history-filters" role="group" aria-label="Filtrar actividad por estado">
        {filterOptions.map((option) => (
          <button
            key={option.id}
            className={`history-filter ${filter === option.id ? "active" : ""}`}
            type="button"
            aria-pressed={filter === option.id}
            onClick={() => setFilter(option.id)}
          >
            {option.label}
          </button>
        ))}
      </div>

      {visibleEntries.length > 0 ? (
        <ol className="history-list">
          {visibleEntries.map((entry) => {
            const relatedDraft = drafts.find((draft) => draft.id === entry.draftId);
            return (
              <li className="history-entry" key={entry.id}>
                <div className="history-entry-marker" aria-hidden="true" />
                <div className="history-entry-content">
                  <div className="history-entry-top">
                    <time>{entry.time} · ejemplo</time>
                    <span className={`draft-status draft-status-${entry.status}`}>{statusLabels[entry.status]}</span>
                  </div>
                  <p>{entry.text}</p>
                  {relatedDraft && (
                    <button className="history-open-button" type="button" onClick={() => onOpenDraft(relatedDraft)}>
                      Abrir “{relatedDraft.title}” en Content Studio <span aria-hidden="true">→</span>
                    </button>
                  )}
                </div>
              </li>
            );
          })}
        </ol>
      ) : (
        <div className="history-empty" role="status">
          <strong>{entries.length === 0 ? "Todavía no hay actividad" : "No hay actividad con este estado"}</strong>
          <span>
            {entries.length === 0
              ? "Los cambios de ejemplo para este contexto aparecerán aquí."
              : "Prueba otro filtro para consultar la actividad disponible."}
          </span>
        </div>
      )}
    </section>
  );
}

function DraftsSection({
  contextName,
  drafts,
  onOpenDraft,
}: {
  contextName: string;
  drafts: LocalDraft[];
  onOpenDraft: (draft: LocalDraft) => void;
}) {
  const [filter, setFilter] = useState<DraftFilter>("all");
  const visibleDrafts = filter === "all" ? drafts : drafts.filter((draft) => draft.status === filter);
  const filterOptions: { id: DraftFilter; label: string }[] = [
    { id: "all", label: "Todos" },
    { id: "draft", label: "Borrador" },
    { id: "review", label: "En revisión" },
    { id: "approved", label: "Aprobado" },
  ];
  const statusLabels: Record<EditorialStatus, string> = {
    draft: "Borrador",
    review: "En revisión",
    approved: "Aprobado",
  };

  return (
    <section className="drafts-section" aria-label={"Borradores de " + contextName}>
      <div className="drafts-heading">
        <div>
          <div className="card-kicker">CONTENIDO LOCAL · DATOS SINTÉTICOS</div>
          <h2>Borradores de {contextName}</h2>
          <p>Revisa ejemplos por estado editorial y abre cualquiera en Content Studio.</p>
        </div>
        <span className="synthetic-label">Sin persistencia</span>
      </div>

      <div className="draft-filters" role="group" aria-label="Filtrar borradores por estado">
        {filterOptions.map((option) => (
          <button
            key={option.id}
            className={`draft-filter ${filter === option.id ? "active" : ""}`}
            type="button"
            aria-pressed={filter === option.id}
            onClick={() => setFilter(option.id)}
          >
            {option.label}
          </button>
        ))}
      </div>

      {visibleDrafts.length > 0 ? (
        <div className="draft-list">
          {visibleDrafts.map((draft) => (
            <article className="draft-list-card" key={draft.id}>
              <div className="draft-list-card-top">
                <span className={`draft-status draft-status-${draft.status}`}>{statusLabels[draft.status]}</span>
                <span className="draft-updated">{draft.updatedAt} · ejemplo</span>
              </div>
              <h3>{draft.title}</h3>
              <p className="draft-meta">{draft.platform} · {draft.format}</p>
              <p className="draft-excerpt">{draft.copy.replace(/\s+/g, " ").slice(0, 150)}</p>
              <button className="draft-open-button" type="button" onClick={() => onOpenDraft(draft)}>
                Abrir en Content Studio <span aria-hidden="true">→</span>
              </button>
            </article>
          ))}
        </div>
      ) : (
        <div className="drafts-empty" role="status">
          <strong>{drafts.length === 0 ? "Todavía no hay borradores" : "No hay borradores con este estado"}</strong>
          <span>
            {drafts.length === 0
              ? "Cuando prepares contenido para este contexto, aparecerá aquí."
              : "Prueba otro filtro o prepara un borrador nuevo desde Content Studio."}
          </span>
        </div>
      )}
      <p className="drafts-boundary">La lista es de ejemplo y no guarda cambios. Los estados no representan aprobaciones fuera del prototipo.</p>
    </section>
  );
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
              : preparationStatus === "draft"
                ? "Borrador local · edítalo o prepáralo para revisión"
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
  const drafts = draftFixtures[activeContext.account] ?? [];
  const historyEntries = historyFixtures[activeContext.account] ?? [];
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

  function openDraft(draft: LocalDraft) {
    setBrief(draft.brief);
    setPreviewCopy(draft.copy);
    setPreparationStatus(draft.status === "draft" ? "draft" : draft.status === "review" ? "pending-review" : "approved");
    setValidationMessage("");
    setView("content-studio");
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
          <button
            className={`nav-item ${view === "drafts" ? "active" : ""}`}
            type="button"
            onClick={() => setView("drafts")}
          >
            <span className="nav-icon">▤</span>
            Borradores
            <span className="nav-count">{drafts.length}</span>
          </button>
          <button
            className={`nav-item ${view === "history" ? "active" : ""}`}
            type="button"
            onClick={() => setView("history")}
          >
            <span className="nav-icon">◷</span>
            Historial
            <span className="nav-count">{historyEntries.length}</span>
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
            Estudio <span>/</span> <strong>{view === "dashboard" ? "Dashboard" : view === "drafts" ? "Borradores" : view === "history" ? "Historial" : "Content Studio"}</strong>
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
            <h1 id="page-title">{view === "dashboard" ? "Tu espacio de trabajo" : view === "drafts" ? "Borradores" : view === "history" ? "Historial" : "Content Studio"}</h1>
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
          ) : view === "drafts" ? (
            <DraftsSection
              contextName={contextName}
              drafts={drafts}
              onOpenDraft={openDraft}
            />
          ) : view === "history" ? (
            <HistorySection
              contextName={contextName}
              entries={historyEntries}
              drafts={drafts}
              onOpenDraft={openDraft}
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
