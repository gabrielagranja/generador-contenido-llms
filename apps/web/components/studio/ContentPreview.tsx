import type { BrandTheme, BriefForm, DraftEvidence, DraftPreparationStatus } from "../../domain/types.ts";
import { dedupeEvidence } from "../../domain/draft-generation.ts";
import { PostArt } from "../ui/PostArt";
import styles from "./studio.module.css";

export function ContentPreview({
  contextName,
  handle,
  theme,
  brief,
  copy,
  status,
  evidenceProvenance,
  supportedClaims,
  unsupportedClaims,
  onCopyChange,
  onCopyBlur,
}: {
  contextName: string;
  handle: string;
  theme: BrandTheme;
  brief: BriefForm;
  copy: string;
  status: DraftPreparationStatus;
  evidenceProvenance: DraftEvidence[];
  supportedClaims: string[];
  unsupportedClaims: string[];
  onCopyChange: (value: string) => void;
  onCopyBlur: () => void | Promise<void>;
}) {
  const readOnly = status === "approved";
  const uniqueEvidence = dedupeEvidence(evidenceProvenance);
  const sourceName = (evidence: DraftEvidence) => evidence.source_file?.split(/[\\/]/).pop() || evidence.source_id || "Documento oficial";
  const headline = brief.campaign.trim() || brief.objective.trim() || "Sin título";
  const maxWidth = brief.format === "Reel" ? "17rem" : brief.platform === "Facebook" && brief.format === "Publicación" ? "34rem" : "24rem";

  return (
    <section className={styles.canvas} aria-labelledby="canvas-title">
      <h2 id="canvas-title" className={styles.colTitle}>2 · Publicación</h2>
      {status === "not-prepared" && (
        <p className={styles.emptyHint}>Aún no hay borrador. Prepáralo desde el brief y aparecerá aquí para tu revisión.</p>
      )}
      <div className={styles.stage}>
        <div className={styles.frame} style={{ maxWidth }}>
          <div className={styles.frameHead}>
            <strong>{contextName}</strong>
            <span>{brief.platform} · {brief.format}</span>
          </div>
          <PostArt theme={theme} headline={headline} handle={handle} platform={brief.platform} format={brief.format} />
        </div>
      </div>
      <div className={styles.captionBlock}>
        <label className={styles.label} htmlFor="preview-copy">
          {readOnly ? "Texto aprobado · solo lectura" : "Texto de la publicación · editable en local"}
        </label>
        <textarea
          id="preview-copy"
          className={styles.caption}
          value={copy}
          onChange={(event) => onCopyChange(event.target.value)}
          onBlur={onCopyBlur}
          placeholder="El borrador de la API aparecerá aquí al preparar el brief."
          readOnly={readOnly}
        />
        <p className={styles.note}>La imagen es una composición sintética de ejemplo, no un recurso real de la marca.</p>
      </div>
      {uniqueEvidence.length > 0 && (
        <section className={styles.evidence} aria-labelledby="sources-title">
          <h3 id="sources-title" className={styles.colTitle}>Fuentes utilizadas</h3>
          <ul className={styles.evidenceList}>
            {uniqueEvidence.map((evidence) => (
              <li key={`${evidence.business_id}-${evidence.source_id}-${evidence.page_number}`}>
                <strong>{sourceName(evidence)}</strong>
                {evidence.page_number ? <span>Página {evidence.page_number}</span> : null}
                <span>Comercio: {evidence.business_id}</span>
                {evidence.source_uri?.startsWith("http") ? <a href={evidence.source_uri} target="_blank" rel="noreferrer">Fuente oficial</a> : null}
              </li>
            ))}
          </ul>
        </section>
      )}
      {(uniqueEvidence.length > 0 || unsupportedClaims.length > 0) && (
        <section className={styles.grounding} aria-labelledby="grounding-title">
          <h3 id="grounding-title" className={styles.colTitle}>Verificación editorial</h3>
          {supportedClaims.length > 0 && (
            <ul className={styles.claimList} aria-label="Afirmaciones respaldadas">
              {supportedClaims.map((claim) => <li key={`supported-${claim}`} className={styles.supported}>SUPPORTED: {claim}</li>)}
            </ul>
          )}
          {unsupportedClaims.length > 0 && (
            <>
              <ul className={styles.claimList} aria-label="Afirmaciones no respaldadas">
                {unsupportedClaims.map((claim) => <li key={`unsupported-${claim}`} className={styles.unsupported}>UNSUPPORTED: {claim}</li>)}
              </ul>
              <p className={styles.warning} role="alert">Esta afirmación no está respaldada por las fuentes disponibles. Revísala antes de aprobar el contenido.</p>
            </>
          )}
        </section>
      )}
    </section>
  );
}
