import type { BrandTheme, BriefForm, DraftPreparationStatus } from "../../domain/types.ts";
import { PostArt } from "../ui/PostArt";
import styles from "./studio.module.css";

export function ContentPreview({
  contextName,
  handle,
  theme,
  brief,
  copy,
  status,
  onCopyChange,
}: {
  contextName: string;
  handle: string;
  theme: BrandTheme;
  brief: BriefForm;
  copy: string;
  status: DraftPreparationStatus;
  onCopyChange: (value: string) => void;
}) {
  const readOnly = status === "approved";
  const headline = brief.campaign.trim() || brief.objective.trim() || "Sin título";
  const maxWidth = brief.format === "Reel" ? "17rem" : brief.platform === "Facebook" && brief.format === "Publicación" ? "34rem" : "24rem";

  return (
    <section className={styles.canvas} aria-labelledby="canvas-title">
      <h2 id="canvas-title" className={styles.colTitle}>2 · Publicación</h2>
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
          placeholder="El borrador de la API aparecerá aquí al preparar el brief."
          readOnly={readOnly}
        />
        <p className={styles.note}>La imagen es una composición sintética de ejemplo, no un recurso real de la marca.</p>
      </div>
    </section>
  );
}
