"use client";

import { useState } from "react";
import { approveCreative, createCreative, creativeImageUrl, discardCreative, regenerateCreative, type ApiCreative, type CreativeInput } from "../../domain/creative-api.ts";
import type { BriefForm } from "../../domain/types.ts";
import styles from "./studio.module.css";

function toInput(brandId: string, brief: BriefForm, copy: string, style: string): CreativeInput {
  const format = brief.format === "Reel" ? "reel" : brief.format === "Carrusel" ? "carousel" : "single_image";
  return {
    brand_id: brandId,
    brief: `${brief.objective}. Audiencia: ${brief.audience}. Campaña: ${brief.campaign}. Restricciones: ${brief.restrictions}`,
    platform: brief.platform === "Facebook" ? "facebook" : "instagram",
    placement: format === "reel" ? "reels" : "feed",
    format,
    copy,
    style,
  };
}

export function CreativePanel({ brandId, brief, copy }: { brandId: string; brief: BriefForm; copy: string }) {
  const [creative, setCreative] = useState<ApiCreative | null>(null);
  const [style, setStyle] = useState("editorial, limpio y sin texto integrado");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function generate(regenerate = false) {
    if (!copy.trim()) { setMessage("Genera o escribe primero un copy para orientar la creatividad."); return; }
    setLoading(true); setMessage("");
    try {
      const input = toInput(brandId, brief, copy, style);
      const result = regenerate && creative ? await regenerateCreative(creative.id, input) : await createCreative(input);
      setCreative(result);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "No se pudo generar la creatividad.");
    } finally { setLoading(false); }
  }

  async function discard() {
    if (!creative) return;
    setLoading(true); setMessage("");
    try { setCreative(await discardCreative(creative.id)); }
    catch (error) { setMessage(error instanceof Error ? error.message : "No se pudo descartar la creatividad."); }
    finally { setLoading(false); }
  }

  async function approve() {
    if (!creative) return;
    setLoading(true); setMessage("");
    try { setCreative(await approveCreative(creative.id)); }
    catch (error) { setMessage(error instanceof Error ? error.message : "No se pudo aprobar la creatividad."); }
    finally { setLoading(false); }
  }

  const target = toInput(brandId, brief, copy, style);
  return (
    <section className={styles.creative} aria-labelledby="creative-title">
      <h2 id="creative-title" className={styles.colTitle}>Creatividad visual</h2>
      <p className={styles.note}>Formato Meta: {target.platform} · {target.placement} · {target.format}. La imagen queda pendiente de revisión y no se publica ni exporta.</p>
      <label className={styles.label} htmlFor="creative-style">Estilo visual</label>
      <input id="creative-style" className={styles.input} value={style} onChange={(event) => setStyle(event.target.value)} />
      <button type="button" className={styles.action} onClick={() => generate()} disabled={loading}>{loading ? "Generando creatividad…" : "Generar creatividad"}</button>
      {message && <p className={styles.alert} role="alert">{message}</p>}
      {creative && (
        <div className={styles.creativeResult}>
          {creative.review_state !== "discarded" && <img src={creativeImageUrl(creative.image_url)} width={creative.width} height={creative.height} alt={`Creatividad pendiente para ${creative.brand_id}`} className={styles.creativeImage} />}
          <p className={styles.note}>{creative.width} × {creative.height} · {creative.aspect_ratio} · {creative.review_state}</p>
          <div className={styles.creativeActions}>
            <button type="button" className={styles.action} onClick={() => generate(true)} disabled={loading || creative.review_state === "discarded"}>Regenerar</button>
            <button type="button" className={styles.action} onClick={discard} disabled={loading || creative.review_state !== "pending-review"}>Descartar</button>
            <button type="button" className={styles.action} onClick={approve} disabled={loading || creative.review_state !== "pending-review"}>Aprobar en prototipo</button>
          </div>
        </div>
      )}
    </section>
  );
}
