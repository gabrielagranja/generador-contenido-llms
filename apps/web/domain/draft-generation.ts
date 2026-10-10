export type GenerationState = "idle" | "loading" | "success" | "error";

export type DraftGenerationResult = {
  copy: string;
  reviewState: "pending_human_review";
};

type DraftApiResponse = {
  detail?: string;
  drafts?: Array<{ caption?: string }>;
  review_state?: string;
};

export const generationStateLabels: Record<GenerationState, string> = {
  idle: "Sin solicitar",
  loading: "Generando…",
  success: "Generado correctamente",
  error: "Error de generación",
};

export function canStartGeneration(state: GenerationState): boolean {
  return state !== "loading";
}

export async function parseDraftResponse(response: Pick<Response, "ok" | "status" | "json">): Promise<DraftGenerationResult> {
  let payload: DraftApiResponse;
  try {
    payload = (await response.json()) as DraftApiResponse;
  } catch {
    throw new Error("La API devolvió una respuesta no válida.");
  }

  if (!response.ok) {
    throw new Error(payload.detail || `La API respondió con estado ${response.status}.`);
  }
  if (payload.review_state !== "pending_human_review") {
    throw new Error("La API no confirmó que el borrador quede pendiente de revisión humana.");
  }

  const copy = payload.drafts?.[0]?.caption?.trim();
  if (!copy) {
    throw new Error("La API no devolvió un borrador editable.");
  }

  return { copy, reviewState: "pending_human_review" };
}
