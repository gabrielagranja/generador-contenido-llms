import { apiBaseUrl, ReviewApiError } from "./review-api";

export type StoredPlan = { plan_id: string; plan: { starts_on: string; ends_on: string; items: Array<{ bucket_key: string; platform: string; format: string; review_state?: string | null }> } };

export async function getPlans(): Promise<StoredPlan[]> {
  const response = await fetch(`${apiBaseUrl()}/plans`);
  if (!response.ok) throw new ReviewApiError("El calendario no está disponible.", response.status);
  return response.json() as Promise<StoredPlan[]>;
}
