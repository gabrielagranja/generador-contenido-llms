import type {
  BrandContext,
  BriefForm,
  DashboardFixture,
  HistoryEntry,
  LocalDraft,
} from "./types.ts";

/**
 * Deterministic UI fixtures. The independent bakery remains synthetic; Coll
 * Amunt! commerce contexts carry only official names and real business IDs.
 * Factual content for those businesses is retrieved by the API RAG boundary.
 */

export const brandContexts: BrandContext[] = [
  {
    id: "panaderia",
    name: "Panadería La Plaza",
    account: "panaderialaplaza",
    kind: "Marca independiente",
    summary: "Marca independiente de panadería con producto artesano de elaboración diaria. Ficha sintética de ejemplo.",
    theme: { accent: "#9a5b13", ink: "#3b2a14", tint: "#f3e4c8" },
  },
  {
    id: "coll-amunt",
    name: "Coll Amunt!",
    account: "collamunt",
    kind: "Asociación de comercio local · Barcelona",
    summary: "Asociación de comercios locales de Barcelona. El contexto factual se recupera del PDF oficial de Coll Amunt!.",
    theme: { accent: "#a3283d", ink: "#3a1119", tint: "#f4d9dc" },
    commerceOptions: [
      {
        id: "pelu-sonia",
        name: "Pelu Sonia",
        account: "coll-amunt-pelu-sonia",
        businessId: "coll-amunt-pelu-sonia",
        sector: "Comercio asociado",
        summary: "Contexto oficial recuperable desde el PDF de Coll Amunt!.",
      },
      {
        id: "centre-d-estetica-alma",
        name: "Centre d\u2019Est\u00e8tica Alma",
        account: "coll-amunt-centre-d-estetica-alma",
        businessId: "coll-amunt-centre-d-estetica-alma",
        sector: "Comercio asociado",
        summary: "Contexto oficial recuperable desde el PDF de Coll Amunt!.",
      },
    ],
  },
];

export const dashboardFixtures: Record<string, DashboardFixture> = {
  panaderialaplaza: {
    drafts: 3,
    review: 2,
    approved: 5,
    upcoming: [
      { id: "plaza-1", title: "Pan del día: proceso artesano", date: "12 jun", platform: "Instagram", format: "Carrusel", campaign: "Mañanas de barrio" },
      { id: "plaza-2", title: "Selección de desayunos", date: "14 jun", platform: "Facebook", format: "Publicación", campaign: "Sabores del barrio" },
    ],
    activity: [
      { id: "plaza-a1", text: "Borrador sintético actualizado: Pan del día", time: "Hoy, 09:40" },
      { id: "plaza-a2", text: "Contenido sintético aprobado para revisión final", time: "Ayer, 16:20" },
      { id: "plaza-a3", text: "Nuevo contenido añadido al calendario de ejemplo", time: "10 jun, 11:05" },
    ],
  },
  "coll-amunt-pelu-sonia": {
    drafts: 0,
    review: 0,
    approved: 0,
    upcoming: [],
    activity: [],
  },
  "coll-amunt-centre-d-estetica-alma": {
    drafts: 0,
    review: 0,
    approved: 0,
    upcoming: [],
    activity: [],
  },
};

export const briefDefaults: Record<string, BriefForm> = {
  panaderialaplaza: {
    objective: "Presentar una novedad de producto artesano",
    audience: "Personas del barrio interesadas en desayunos artesanos",
    platform: "Instagram",
    format: "Carrusel",
    campaign: "Mañanas de barrio",
    restrictions: "Mantener un tono cercano y no prometer disponibilidad futura.",
  },
  "coll-amunt-pelu-sonia": {
    objective: "Dar a conocer el comercio seleccionado",
    audience: "Vecinas y vecinos del barrio",
    platform: "Instagram",
    format: "Carrusel",
    campaign: "Comercio de proximidad",
    restrictions: "Usar únicamente información respaldada por el PDF oficial y mantener el contenido pendiente de revisión humana.",
  },
  "coll-amunt-centre-d-estetica-alma": {
    objective: "Dar a conocer el comercio seleccionado",
    audience: "Vecinas y vecinos del barrio",
    platform: "Facebook",
    format: "Publicación",
    campaign: "Comercio de proximidad",
    restrictions: "Usar únicamente información respaldada por el PDF oficial y mantener el contenido pendiente de revisión humana.",
  },
};

export function getBriefDefaults(account: string): BriefForm {
  return briefDefaults[account] ?? briefDefaults.panaderialaplaza;
}

export const draftFixtures: Record<string, LocalDraft[]> = {
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
  "coll-amunt-pelu-sonia": [],
  "coll-amunt-centre-d-estetica-alma": [],
};

/** Synthetic editorial activity retained from the existing History screen. */
export const historyFixtures: Record<string, HistoryEntry[]> = {
  panaderialaplaza: [
    { id: "plaza-history-1", text: "Se editó un borrador local.", time: "Hoy · 09:40", status: "draft", draftId: "plaza-draft-pan-artesano" },
    { id: "plaza-history-2", text: "El contenido se envió a revisión humana.", time: "Ayer · 16:20", status: "review", draftId: "plaza-review-desayunos" },
    { id: "plaza-history-3", text: "Se marcó como aprobado en el prototipo.", time: "8 oct · 12:15", status: "approved", draftId: "plaza-approved-temporada" },
  ],
  "coll-amunt-pelu-sonia": [],
  "coll-amunt-centre-d-estetica-alma": [],
};
