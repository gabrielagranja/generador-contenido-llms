import type { BriefForm, DraftPreparationStatus, EditorialStatus } from "./types.ts";

/**
 * Local editorial transitions of the frontend prototype.
 * Rules mirrored from openspec/changes/editorial-review-control:
 * - generating or editing never approves;
 * - approval is an explicit action taken from pending review only;
 * - invalid transitions are rejected (the state is returned unchanged).
 */

export function afterBriefChange(current: DraftPreparationStatus): DraftPreparationStatus {
  return current === "pending-review" || current === "approved" ? "brief-changed" : current;
}

/** Editing an approved text invalidates its local approval; pending edits stay pending. */
export function afterTextChange(current: DraftPreparationStatus): DraftPreparationStatus {
  return current === "approved" ? "brief-changed" : current;
}

export function approve(current: DraftPreparationStatus): DraftPreparationStatus {
  return current === "pending-review" ? "approved" : current;
}

export function requestChanges(current: DraftPreparationStatus): DraftPreparationStatus {
  return current === "pending-review" ? "changes-requested" : current;
}

export function resubmit(current: DraftPreparationStatus): DraftPreparationStatus {
  return current === "changes-requested" ? "pending-review" : current;
}

export function statusFromDraft(status: EditorialStatus): DraftPreparationStatus {
  if (status === "draft") return "draft";
  if (status === "review") return "pending-review";
  return "approved";
}

export function missingBriefFields(brief: BriefForm): boolean {
  return [brief.objective, brief.audience, brief.campaign].some((value) => !value.trim());
}

export function buildSyntheticCopy(contextName: string, brief: BriefForm): string {
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

export const statusCopy: Record<DraftPreparationStatus, { label: string; hint: string }> = {
  "not-prepared": { label: "Sin borrador", hint: "Completa el brief y prepara un borrador local." },
  draft: { label: "Borrador", hint: "Edítalo y envíalo a revisión humana cuando esté listo." },
  "pending-review": { label: "Pendiente de revisión humana", hint: "Una persona debe aprobar o pedir cambios." },
  "brief-changed": { label: "El brief ha cambiado", hint: "Actualiza el borrador antes de revisarlo." },
  "changes-requested": { label: "Cambios solicitados", hint: "Edita el texto y vuelve a enviarlo a revisión." },
  approved: { label: "Aprobado en el prototipo", hint: "Estado solo local. No habilita exportación ni publicación." },
};
