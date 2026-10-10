import { apiBaseUrl, ReviewApiError } from "./review-api";

export type EditorialPlanItem = {
  source_ref: string;
  source_kind: "guided_brief" | "editorial_content";
  strategy_version: string;
  bucket_key: string;
  platform: "instagram" | "facebook";
  format: "single_image" | "carousel" | "reel";
  review_state?: string | null;
  evidence?: Record<string, unknown>;
};

export type EditorialPlan = {
  strategy_id: string;
  strategy_version: string;
  total_slots: number;
  starts_on: string;
  ends_on: string;
  targets: Record<string, number>;
  items: EditorialPlanItem[];
};

export type StoredPlan = { plan_id: string; plan: EditorialPlan };

export async function savePlan(plan: EditorialPlan): Promise<StoredPlan> {
  let response: Response;
  try {
    response = await fetch(`${apiBaseUrl()}/plans`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(plan),
      signal: AbortSignal.timeout(10000),
    });
  } catch {
    throw new ReviewApiError("No se pudo conectar con la API de planes.");
  }
  if (!response.ok) throw new ReviewApiError("El plan no se pudo guardar.", response.status);
  return response.json() as Promise<StoredPlan>;
}

export async function getPlans(): Promise<StoredPlan[]> {
  const response = await fetch(`${apiBaseUrl()}/plans`);
  if (!response.ok) throw new ReviewApiError("El calendario no está disponible.", response.status);
  return response.json() as Promise<StoredPlan[]>;
}
