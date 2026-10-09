import type { BriefForm, ContentFormat, DraftPreparationStatus, Platform } from "../../domain/types.ts";
import styles from "./studio.module.css";

const platforms: Platform[] = ["Instagram", "Facebook"];
const formats: ContentFormat[] = ["Reel", "Carrusel", "Publicación"];

function Choice<T extends string>({
  legend,
  name,
  options,
  value,
  onChange,
}: {
  legend: string;
  name: string;
  options: T[];
  value: T;
  onChange: (value: T) => void;
}) {
  return (
    <fieldset className={styles.choice}>
      <legend className={styles.legend}>{legend}</legend>
      <div className={styles.options}>
        {options.map((option) => (
          <label className={styles.option} key={option}>
            <input type="radio" name={name} value={option} checked={value === option} onChange={() => onChange(option)} />
            <span>{option}</span>
          </label>
        ))}
      </div>
    </fieldset>
  );
}

export function BriefEditor({
  brief,
  status,
  validationMessage,
  onChange,
  onPrepare,
}: {
  brief: BriefForm;
  status: DraftPreparationStatus;
  validationMessage: string;
  onChange: (field: keyof BriefForm, value: string) => void;
  onPrepare: () => void;
}) {
  const prepareLabel =
    status === "pending-review" ? "Preparar otro borrador" : status === "brief-changed" ? "Actualizar borrador" : "Preparar borrador";

  return (
    <section aria-labelledby="brief-title">
      <h2 id="brief-title" className={styles.colTitle}>1 · Brief</h2>
      <div className={styles.fields}>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="brief-objective">Objetivo</label>
          <textarea id="brief-objective" className={styles.input} rows={3} value={brief.objective} onChange={(e) => onChange("objective", e.target.value)} />
        </div>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="brief-audience">Audiencia</label>
          <input id="brief-audience" className={styles.input} value={brief.audience} onChange={(e) => onChange("audience", e.target.value)} />
        </div>
        <Choice legend="Canal" name="platform" options={platforms} value={brief.platform} onChange={(v) => onChange("platform", v)} />
        <Choice legend="Formato (MVP)" name="format" options={formats} value={brief.format} onChange={(v) => onChange("format", v)} />
        <div className={styles.field}>
          <label className={styles.label} htmlFor="brief-campaign">Campaña</label>
          <input id="brief-campaign" className={styles.input} value={brief.campaign} onChange={(e) => onChange("campaign", e.target.value)} />
        </div>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="brief-restrictions">Restricciones</label>
          <textarea id="brief-restrictions" className={styles.input} rows={3} value={brief.restrictions} onChange={(e) => onChange("restrictions", e.target.value)} />
        </div>
        <button type="button" className={styles.primary} onClick={onPrepare}>{prepareLabel}</button>
        {validationMessage && <p className={styles.alert} role="alert">{validationMessage}</p>}
        <p className={styles.note}>Marca y comercio se heredan del selector del espacio de trabajo.</p>
      </div>
    </section>
  );
}
