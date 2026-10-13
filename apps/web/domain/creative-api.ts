import { authHeaders, handleUnauthorized } from "./auth.ts";
import { apiBaseUrl, ReviewApiError } from "./review-api.ts";

export type CreativeReviewState = "pending-review" | "approved-prototype" | "discarded";
export type ApiCreative = {
  id: string;
  image_url: string;
  prompt: string;
  brand_id: string;
  platform: string;
  placement: string;
  format: string;
  width: number;
  height: number;
  aspect_ratio: string;
  model: string;
  generated_at: string;
  review_state: CreativeReviewState;
  provenance: Array<{ business_id: string; brand_id?: string | null; source_name?: string | null; source_url?: string | null; source_type?: string | null; language?: string | null; retrieved_at?: string | null }>;
  source_creative_id?: string | null;
};

export type CreativeInput = {
  brand_id: string;
  brief: string;
  platform: "instagram" | "facebook";
  placement: "feed" | "reels";
  format: "single_image" | "carousel" | "reel";
  copy: string;
  style: string;
};

async function creativeRequest(path: string, init: RequestInit, requirePending = false): Promise<ApiCreative> {
  let response: Response;
  try {
    response = await fetch(`${apiBaseUrl()}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...authHeaders(), ...(init.headers as Record<string, string> | undefined) },
    });
  } catch {
    throw new ReviewApiError("No se pudo conectar con la API de creatividades.");
  }
  const payload = await response.json().catch(() => null) as { detail?: unknown } | null;
  if (response.status === 401) {
    handleUnauthorized();
    throw new ReviewApiError("Tu sesión ha caducado. Vuelve a iniciar sesión.", 401);
  }
  if (!response.ok) {
    const detail = typeof payload?.detail === "string" ? payload.detail : `La API respondió con estado ${response.status}.`;
    throw new ReviewApiError(detail, response.status);
  }
  const creative = payload as ApiCreative;
  if (!creative?.id || !creative.image_url || (requirePending && creative.review_state !== "pending-review")) {
    throw new ReviewApiError(requirePending ? "La API no devolvió una creatividad pendiente de revisión." : "La API no devolvió una creatividad válida.", response.status);
  }
  return creative;
}

export function createCreative(input: CreativeInput) {
  return creativeRequest("/creatives", { method: "POST", body: JSON.stringify(input) }, true);
}

export function regenerateCreative(id: string, input: CreativeInput) {
  return creativeRequest(`/creatives/${encodeURIComponent(id)}/regenerate`, { method: "POST", body: JSON.stringify(input) }, true);
}

export function discardCreative(id: string) {
  return creativeRequest(`/creatives/${encodeURIComponent(id)}/discard`, { method: "POST" });
}

export function approveCreative(id: string) {
  return creativeRequest(`/creatives/${encodeURIComponent(id)}/approve`, { method: "POST" });
}

export function creativeImageUrl(path: string): string {
  return path.startsWith("http") ? path : `${apiBaseUrl()}${path}`;
}
