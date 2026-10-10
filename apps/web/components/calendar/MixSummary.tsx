import {
  balance,
  engagementHints,
  formatHints,
  formatLabels,
  platformLabels,
  summarizeMix,
  type CalendarItem,
} from "../../domain/calendar-layout.ts";
import styles from "./calendar.module.css";

const bucketClass: Record<string, string> = {
  EDUCATIONAL: styles.bEdu,
  COMMUNITY: styles.bCom,
  PROMOTIONAL: styles.bPro,
  VALUE: styles.bCom,
};

/** Balance of the month against the strategy targets, plus what each kind of content tends to move. */
export function MixSummary({ items, monthLabel, targets }: { items: CalendarItem[]; monthLabel: string; targets: Record<string, number> }) {
  const { platforms, formats } = summarizeMix(items);
  const { total, rows, balanced, message } = balance(items, targets);
  if (!total) return null;
  const usedFormats = Object.keys(formats).filter((format) => formatHints[format]);
  let offset = 25;

  return (
    <section className={styles.mix} aria-labelledby="mix-title">
      <h2 id="mix-title" className={styles.mixTitle}>Balance de {monthLabel.toLowerCase()}</h2>
      <p className={styles.mixLead}>
        {total} {total === 1 ? "publicación" : "publicaciones"}:{" "}
        {Object.entries(platforms).map(([platform, count]) => `${count} en ${platformLabels[platform] ?? platform}`).join(" y ")}.
        {" "}Formatos: {Object.entries(formats).map(([format, count]) => `${count} ${formatLabels[format] ?? format}`).join(", ")}.
      </p>

      <div className={styles.balance}>
        <div className={styles.ring}>
          <svg viewBox="0 0 36 36" role="img" aria-label={`Reparto real: ${rows.filter((row) => row.actual > 0).map((row) => `${row.label} ${row.percent}%`).join(", ")}`}>
            <circle className={styles.ringTrack} cx="18" cy="18" r="15.9155" />
            {rows.filter((row) => row.actual > 0).map((row) => {
              const share = (row.actual / total) * 100;
              const segment = (
                <circle
                  key={row.bucket}
                  className={`${styles.ringSegment} ${bucketClass[row.bucket] ?? styles.bCom}`}
                  cx="18"
                  cy="18"
                  r="15.9155"
                  pathLength={100}
                  strokeDasharray={`${share} ${100 - share}`}
                  strokeDashoffset={offset}
                />
              );
              offset -= share;
              return segment;
            })}
          </svg>
          <div className={styles.ringCenter}><strong>{total}</strong><span>{total === 1 ? "publicación" : "publicaciones"}</span></div>
        </div>

        <div>
          <ul className={styles.balanceRows}>
            {rows.map((row) => {
              const hint = engagementHints[row.bucket];
              const state = row.diff < 0 ? styles.gapLow : row.diff > 0 ? styles.gapHigh : styles.gapOk;
              const gap = row.diff < 0 ? `Faltan ${-row.diff}` : row.diff > 0 ? `Sobran ${row.diff}` : "En objetivo";
              return (
                <li key={row.bucket} className={`${styles.balanceRow} ${bucketClass[row.bucket] ?? styles.bCom}`}>
                  <span className={styles.swatch} aria-hidden="true" />
                  <div>
                    <p className={styles.mixName}><strong>{row.label}</strong> <span className={styles.count}>{row.actual} de {row.target}</span></p>
                    {hint && <p className={styles.mixText}>Señal a mirar: {hint.signal}. {hint.expectation}</p>}
                  </div>
                  <span className={`${styles.gap} ${state}`}>{gap}</span>
                </li>
              );
            })}
          </ul>
          <p className={balanced ? styles.balanceOk : styles.balanceNote} role="status">{message}</p>
        </div>
      </div>

      {usedFormats.length > 0 && (
        <ul className={styles.formatHints}>
          {usedFormats.map((format) => <li key={format}>{formatHints[format]}</li>)}
        </ul>
      )}

      <p className={styles.banner}>
        Orientativo. El balance compara lo planificado con el objetivo de la estrategia. Todavía no hay métricas propias, así que no se calculan cifras de engagement: las pautas son generales y las sustituirán los resultados reales.
      </p>
    </section>
  );
}
