import type { DraftPreparationStatus, EditorialStatus as DraftStatus } from "../../domain/types.ts";
import { statusCopy } from "../../domain/editorial.ts";
import styles from "./ui.module.css";

const draftStatusLabels: Record<DraftStatus, string> = {
  draft: "Borrador",
  review: "En revisión",
  approved: "Aprobado",
};

function dotClass(tone: "draft" | "review" | "approved" | "alert") {
  return [styles.dot, tone === "review" && styles.dotReview, tone === "approved" && styles.dotApproved, tone === "alert" && styles.dotAlert]
    .filter(Boolean)
    .join(" ");
}

/** Status of a stored draft (list views). */
export function DraftStatusMark({ status }: { status: DraftStatus }) {
  return (
    <span className={styles.statusMark}>
      <span className={dotClass(status)} aria-hidden="true" />
      {draftStatusLabels[status]}
    </span>
  );
}

const studioTone: Record<DraftPreparationStatus, "draft" | "review" | "approved" | "alert"> = {
  "not-prepared": "draft",
  draft: "draft",
  "pending-review": "review",
  "brief-changed": "alert",
  "changes-requested": "alert",
  approved: "approved",
};

/** Live editorial state of the item open in Content Studio. */
export function StudioStatus({ status }: { status: DraftPreparationStatus }) {
  return (
    <div aria-live="polite">
      <span className={styles.statusMark}>
        <span className={dotClass(studioTone[status])} aria-hidden="true" />
        {statusCopy[status].label}
      </span>
    </div>
  );
}

const steps = ["Idea", "Borrador", "Revisión", "Aprobación"] as const;

function currentStep(status: DraftPreparationStatus): number {
  switch (status) {
    case "not-prepared": return 0;
    case "draft": return 1;
    case "approved": return 3;
    default: return 2;
  }
}

/** Four guided steps. Reaching step 4 is only possible through explicit approval. */
export function EditorialProgress({ status }: { status: DraftPreparationStatus }) {
  const current = currentStep(status);
  return (
    <ol className={styles.progress} aria-label="Progreso editorial">
      {steps.map((label, index) => {
        const state = index < current ? styles.stepDone : index === current ? styles.stepCurrent : "";
        return (
          <li key={label} className={`${styles.step} ${state}`} aria-current={index === current ? "step" : undefined}>
            <span className={styles.stepNum} aria-hidden="true">{index + 1}</span>
            {label}
          </li>
        );
      })}
    </ol>
  );
}
