import type { CSSProperties } from "react";
import type { BrandTheme, ContentFormat, Platform } from "../../domain/types.ts";
import styles from "./ui.module.css";

function seedOf(text: string): number {
  let hash = 7;
  for (let i = 0; i < text.length; i += 1) hash = (hash * 31 + text.charCodeAt(i)) >>> 0;
  return hash;
}

export function aspectFor(platform: Platform, format: ContentFormat): string {
  if (format === "Reel") return "9 / 16";
  if (format === "Carrusel") return "4 / 5";
  return platform === "Facebook" ? "1.91 / 1" : "1 / 1";
}

/**
 * Deterministic, art-directed placeholder for a publication image.
 * It is generated from the brand tokens and the headline and is always labelled
 * as synthetic; it never stands in for real photography or real assets.
 */
export function PostArt({
  theme,
  headline,
  handle,
  platform,
  format,
  maxWidth,
}: {
  theme: BrandTheme;
  headline: string;
  handle: string;
  platform: Platform;
  format: ContentFormat;
  maxWidth?: string;
}) {
  const layout = seedOf(headline) % 3;
  const style = {
    "--art-accent": theme.accent,
    "--art-ink": theme.ink,
    "--art-tint": theme.tint,
    aspectRatio: aspectFor(platform, format),
    maxWidth,
  } as CSSProperties;

  return (
    <figure
      className={`${styles.art} ${styles["layout" + layout]}`}
      style={style}
      role="img"
      aria-label={`Imagen sintética para ${platform}, formato ${format}: ${headline}`}
    >
      <span className={styles.artShapeA} />
      <span className={styles.artShapeB} />
      <span className={styles.artHandle}>@{handle}</span>
      <span className={styles.artLabel}>Imagen sintética</span>
      <span className={styles.artText}>{headline}</span>
    </figure>
  );
}
