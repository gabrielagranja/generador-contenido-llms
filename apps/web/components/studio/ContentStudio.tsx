import type { BrandTheme, BriefForm, DraftEvidence, DraftPreparationStatus } from "../../domain/types.ts";
import { generationStateLabels, type GenerationState } from "../../domain/draft-generation.ts";
import { statusCopy } from "../../domain/editorial.ts";
import { Kicker, SyntheticNotice } from "../ui/Kicker";
import { EditorialProgress, StudioStatus } from "../ui/EditorialStatus";
import { BriefEditor } from "./BriefEditor";
import { ContentPreview } from "./ContentPreview";
import { ReviewActions } from "./ReviewActions";
import styles from "./studio.module.css";

export function ContentStudio({
  contextName,
  contextSummary,
  contextSector,
  handle,
  theme,
  brief,
  previewCopy,
  status,
  validationMessage,
  generationState,
  evidenceProvenance,
  supportedClaims,
  unsupportedClaims,
  onBriefChange,
  onCopyChange,
  onPrepare,
  isPreparing,
  onApprove,
  onRequestChanges,
  onResubmit,
}: {
  contextName: string;
  contextSummary: string;
  contextSector?: string;
  handle: string;
  theme: BrandTheme;
  brief: BriefForm;
  previewCopy: string;
  status: DraftPreparationStatus;
  validationMessage: string;
  generationState: GenerationState;
  evidenceProvenance: DraftEvidence[];
  supportedClaims: string[];
  unsupportedClaims: string[];
  onBriefChange: (field: keyof BriefForm, value: string) => void;
  onCopyChange: (value: string) => void;
  onPrepare: () => void | Promise<void>;
  isPreparing: boolean;
  onApprove: () => void;
  onRequestChanges: () => void;
  onResubmit: () => void;
}) {
  return (
    <section aria-labelledby="view-title">
      <header className={styles.head}>
        <div>
          <Kicker>Content Studio</Kicker>
          <h1 id="view-title" className={styles.title}>Prepara una idea de contenido</h1>
          <p className={styles.context}>Trabajando en <strong>{contextName}</strong></p>
        </div>
        <SyntheticNotice>API local · revisión humana · sin persistencia</SyntheticNotice>
      </header>

      <div className={styles.grid}>
        <BriefEditor
          brief={brief}
          status={status}
          validationMessage={validationMessage}
          onChange={onBriefChange}
          onPrepare={onPrepare}
          isPreparing={isPreparing}
        />

        <ContentPreview
          contextName={contextName}
          handle={handle}
          theme={theme}
          brief={brief}
          copy={previewCopy}
          status={status}
          evidenceProvenance={evidenceProvenance}
          supportedClaims={supportedClaims}
          unsupportedClaims={unsupportedClaims}
          onCopyChange={onCopyChange}
        />

        <aside className={styles.side} aria-label="Estado editorial y contexto">
          <section aria-labelledby="state-title">
            <h2 id="state-title" className={styles.colTitle}>3 · Revisión</h2>
            <div className={styles.statusBlock}>
              <EditorialProgress status={status} />
              <StudioStatus status={status} />
              <p className={styles.generationState} aria-live="polite">
                Generación: {generationStateLabels[generationState]}
              </p>
              <p className={styles.hint}>{statusCopy[status].hint}</p>
            </div>
            <ReviewActions status={status} onApprove={onApprove} onRequestChanges={onRequestChanges} onResubmit={onResubmit} />
            <p className={styles.note}>
              Aprobar solo cambia el estado local del prototipo. No habilita copia, exportación ni publicación.
            </p>
          </section>

          <section className={styles.details} aria-label="Variantes">
            <p><strong>Variantes</strong></p>
            <p className={styles.note}>
              El prototipo local prepara un borrador. Las variantes y la regeneración no forman parte de esta vista todavía.
            </p>
          </section>

          <details className={styles.details}>
            <summary>Contexto de marca</summary>
            <p>{contextSummary}</p>
            <dl>
              {contextSector && (<><dt>Sector</dt><dd>{contextSector}</dd></>)}
              <dt>Restricciones del brief</dt>
              <dd>{brief.restrictions || "Sin restricciones indicadas"}</dd>
            </dl>
            <p className={styles.note}>
              El contexto de marca se aplica en segundo plano; esta vista mantiene la atención en el brief y la revisión.
            </p>
          </details>
        </aside>
      </div>
    </section>
  );
}
