import type {
  BrandContext,
  BriefForm,
  DashboardFixture,
  HistoryEntry,
  LocalDraft,
} from "./types.ts";

/**
 * Deterministic, clearly synthetic fixtures. No real business identities, claims
 * or metrics. Coll Amunt! is a local business association in Barcelona; its
 * associated businesses are placeholders ("Comercio sintético A/B").
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
    summary: "Asociación de comercios locales de Barcelona. Cada comercio asociado se trabaja como un contexto propio. Ficha sintética de ejemplo.",
    theme: { accent: "#a3283d", ink: "#3a1119", tint: "#f4d9dc" },
    commerceOptions: [
      {
        id: "synthetic-a",
        name: "Comercio sintético A",
        account: "collamunt_a",
        sector: "Alimentación de proximidad",
        summary: "Comercio asociado de ejemplo del sector de alimentación de proximidad. No representa un negocio real.",
      },
      {
        id: "synthetic-b",
        name: "Comercio sintético B",
        account: "collamunt_b",
        sector: "Servicios y artesanía",
        summary: "Comercio asociado de ejemplo del sector de servicios y artesanía. No representa un negocio real.",
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
  collamunt_a: {
    drafts: 2,
    review: 1,
    approved: 4,
    upcoming: [
      { id: "coll-a-1", title: "Compra de proximidad: producto de temporada", date: "13 jun", platform: "Instagram", format: "Carrusel", campaign: "Compra en el barrio" },
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

export const briefDefaults: Record<string, BriefForm> = {
  panaderialaplaza: {
    objective: "Presentar una novedad de producto artesano",
    audience: "Personas del barrio interesadas en desayunos artesanos",
    platform: "Instagram",
    format: "Carrusel",
    campaign: "Mañanas de barrio",
    restrictions: "Mantener un tono cercano y no prometer disponibilidad futura.",
  },
  collamunt_a: {
    objective: "Dar a conocer un producto de temporada del comercio",
    audience: "Vecinas y vecinos que prefieren comprar en el comercio de su barrio",
    platform: "Instagram",
    format: "Carrusel",
    campaign: "Compra en el barrio",
    restrictions: "No incluir precios, horarios ni datos de contacto reales; mantener el contenido como ejemplo.",
  },
  collamunt_b: {
    objective: "Invitar a conocer un servicio del comercio asociado",
    audience: "Personas que buscan servicios y artesanía cerca de casa",
    platform: "Facebook",
    format: "Publicación",
    campaign: "Servicios de proximidad",
    restrictions: "Usar referencias genéricas, sin afirmaciones verificables, y mantener el contenido como ejemplo.",
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
  collamunt_a: [
    {
      id: "coll-a-draft-temporada",
      title: "Producto de temporada, comprado en el barrio",
      platform: "Instagram",
      format: "Carrusel",
      status: "draft",
      updatedAt: "Hoy · 08:55",
      brief: { ...briefDefaults.collamunt_a },
      copy: `Borrador sintético · Coll Amunt! · Comercio sintético A\n\nUna invitación genérica a descubrir un producto de temporada en el comercio del barrio.\n\nSin precios, horarios ni datos reales.`,
    },
    {
      id: "coll-a-review-vecindario",
      title: "Cinco motivos para comprar cerca de casa",
      platform: "Facebook",
      format: "Publicación",
      status: "review",
      updatedAt: "11 jun · 14:10",
      brief: { ...briefDefaults.collamunt_a, platform: "Facebook", format: "Publicación", campaign: "Compra en el barrio" },
      copy: `Borrador sintético · Coll Amunt! · Comercio sintético A\n\nUna propuesta genérica sobre el valor del comercio de proximidad.\n\nPendiente de revisión humana.`,
    },
  ],
  collamunt_b: [
    {
      id: "coll-b-draft-servicio",
      title: "Conoce un servicio de tu barrio",
      platform: "Facebook",
      format: "Publicación",
      status: "draft",
      updatedAt: "10 jun · 10:30",
      brief: { ...briefDefaults.collamunt_b },
      copy: `Borrador sintético · Coll Amunt! · Comercio sintético B\n\nUna presentación genérica de un servicio de proximidad.`,
    },
  ],
};

/** Synthetic editorial activity retained from the existing History screen. */
export const historyFixtures: Record<string, HistoryEntry[]> = {
  panaderialaplaza: [
    { id: "plaza-history-1", text: "Se editó un borrador local.", time: "Hoy · 09:40", status: "draft", draftId: "plaza-draft-pan-artesano" },
    { id: "plaza-history-2", text: "El contenido se envió a revisión humana.", time: "Ayer · 16:20", status: "review", draftId: "plaza-review-desayunos" },
    { id: "plaza-history-3", text: "Se marcó como aprobado en el prototipo.", time: "8 oct · 12:15", status: "approved", draftId: "plaza-approved-temporada" },
  ],
  collamunt_a: [
    { id: "coll-a-history-1", text: "Se preparó un borrador local.", time: "Hoy · 08:55", status: "draft", draftId: "coll-a-draft-temporada" },
    { id: "coll-a-history-2", text: "El contenido se envió a revisión humana.", time: "11 jun · 14:10", status: "review", draftId: "coll-a-review-vecindario" },
  ],
  collamunt_b: [
    { id: "coll-b-history-1", text: "Se creó un borrador de ejemplo.", time: "10 jun · 10:30", status: "draft", draftId: "coll-b-draft-servicio" },
  ],
};
