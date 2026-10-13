export type GenerationState = "idle" | "loading" | "success" | "error";

export type DraftGenerationResult = {
  copy: string;
  reviewState: "pending_human_review";
  evidenceProvenance: DraftEvidence[];
  supportedClaims: string[];
  unsupportedClaims: string[];
  copyApproach: CopyApproachInfo | null;
  contentIds: string[];
};

type DraftApiResponse = {
  detail?: string;
  error?: { code?: unknown; message?: unknown } | string;
  generation_status?: string;
  drafts?: Array<{
    caption?: string;
    evidence_provenance?: unknown;
    supported_claims?: unknown;
    unsupported_claims?: unknown;
    copy_approach?: unknown;
    copy_formula?: unknown;
    approach_rationale?: unknown;
  }>;
  review_state?: string;
  content_ids?: string[];
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

export async function parseDraftResponse(
  response: Pick<Response, "ok" | "status" | "json">,
  expectedBusinessId?: string,
  expectedBrandId?: string,
): Promise<DraftGenerationResult> {
  let payload: DraftApiResponse;
  try {
    payload = (await response.json()) as DraftApiResponse;
  } catch {
    throw new Error("La API devolvió una respuesta no válida.");
  }

  if (!response.ok) {
    throw new Error(payload.detail || `La API respondió con estado ${response.status}.`);
  }
  const generationError = typeof payload.error === "string"
    ? payload.error
    : payload.error && typeof payload.error.message === "string"
      ? payload.error.message
      : undefined;
  if (payload.generation_status === "error" || generationError) {
    throw new Error(generationError || "La generación falló en la API.");
  }
  if (payload.review_state !== "pending_human_review") {
    throw new Error("La API no confirmó que el borrador quede pendiente de revisión humana.");
  }

  const draft = payload.drafts?.[0];
  const copy = draft?.caption?.trim();
  if (!draft || !copy) {
    throw new Error("La API no devolvió un borrador editable.");
  }
  const internalMarker = ["copy approach", "scaffold", "safeguard", "retrieved evidence", "prompting instructions"]
    .find((marker) => copy.toLowerCase().includes(marker));
  if (internalMarker) {
    throw new Error("La API devolvió instrucciones internas en lugar de contenido editorial.");
  }

  const evidenceProvenance = Array.isArray(draft.evidence_provenance)
    ? draft.evidence_provenance.flatMap((item) => normalizeEvidence(item, expectedBusinessId, expectedBrandId))
    : [];
  const supportedClaims = Array.isArray(draft.supported_claims)
    ? draft.supported_claims.filter((claim): claim is string => typeof claim === "string" && claim.trim().length > 0)
    : [];
  const unsupportedClaims = Array.isArray(draft.unsupported_claims)
    ? draft.unsupported_claims.filter((claim): claim is string => typeof claim === "string" && claim.trim().length > 0)
    : [];

  const contentIds = Array.isArray(payload.content_ids) ? payload.content_ids.filter((id): id is string => typeof id === "string" && id.trim().length > 0) : [];
  if (contentIds.length !== (payload.drafts?.length ?? 0)) {
    throw new Error("La API no devolvió identificadores para todos los borradores.");
  }
  return { copy, reviewState: "pending_human_review", evidenceProvenance, supportedClaims, unsupportedClaims, copyApproach: parseCopyApproach(draft), contentIds };
}

function normalizeEvidence(item: unknown, expectedBusinessId?: string, expectedBrandId?: string): DraftEvidence[] {
  if (!item || typeof item !== "object") return [];
  const value = item as Record<string, unknown>;
  if (typeof value.business_id !== "string" || !expectedBusinessId || value.business_id !== expectedBusinessId) return [];
  if (expectedBrandId && value.brand_id !== expectedBrandId) return [];
  return [{
    business_id: value.business_id,
    ...(typeof value.brand_id === "string" ? { brand_id: value.brand_id } : {}),
    ...(typeof value.source_type === "string" ? { source_type: value.source_type } : {}),
    ...(typeof value.source_id === "string" ? { source_id: value.source_id } : {}),
    ...(typeof value.source_version === "string" ? { source_version: value.source_version } : {}),
    ...(typeof value.source_name === "string" ? { source_name: value.source_name } : {}),
    ...(typeof value.source_file === "string" ? { source_file: value.source_file } : {}),
    ...(typeof value.page_number === "number" ? { page_number: value.page_number } : {}),
    ...(typeof value.source_uri === "string" ? { source_uri: value.source_uri } : {}),
    ...(typeof value.source_url === "string" ? { source_url: value.source_url } : {}),
    ...(typeof value.language === "string" ? { language: value.language } : {}),
    ...(typeof value.retrieved_at === "string" ? { retrieved_at: value.retrieved_at } : {}),
  }];
}
import type { CopyApproachInfo, DraftEvidence } from "./types.ts";


export function dedupeEvidence(evidence: DraftEvidence[]): DraftEvidence[] {
  return Array.from(
    new Map(
      evidence.map((item) => [
        `${item.business_id}|${item.source_id ?? ""}|${item.source_file ?? ""}|${item.page_number ?? ""}`,
        item,
      ]),
    ).values(),
  );
}

export function parseCopyApproach(draft: { copy_approach?: unknown; copy_formula?: unknown; approach_rationale?: unknown }): CopyApproachInfo | null {
  const text = (value: unknown) => (typeof value === "string" ? value.trim() : "");
  const approach = text(draft.copy_approach);
  if (!approach) return null;
  return { approach, formula: text(draft.copy_formula), rationale: text(draft.approach_rationale) };
}
