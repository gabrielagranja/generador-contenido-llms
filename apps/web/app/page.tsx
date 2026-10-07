"use client";

import { useState } from "react";

type Platform = "Instagram" | "Facebook";
type Format = "Publicación" | "Carrusel" | "Reel";

const sampleCopy =
  "Hay planes que saben mejor cuando se comparten. En Panadería La Plaza horneamos cada mañana para que tu pausa tenga ese sabor de siempre. ¿Cuál es tu favorito?";

export default function Home() {
  const [platform, setPlatform] = useState<Platform>("Instagram");
  const [format, setFormat] = useState<Format>("Publicación");
  const [topic, setTopic] = useState("Nuestros panes recién horneados");
  const [goal, setGoal] = useState("Dar a conocer el producto");
  const [audience, setAudience] = useState("Personas del barrio que buscan desayunos artesanos");
  const [notes, setNotes] = useState("");
  const [generated, setGenerated] = useState(false);
  const [copy, setCopy] = useState(sampleCopy);
  const [copied, setCopied] = useState(false);

  function generateDraft() {
    setCopy(sampleCopy);
    setGenerated(true);
    setCopied(false);
  }

  async function copyDraft() {
    try {
      await navigator.clipboard.writeText(copy);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#" aria-label="Inicio de Estudio">
          <span className="brand-mark" aria-hidden="true">e.</span>
          <span>estudio<span className="brand-dot">.</span></span>
        </a>

        <div className="workspace-label">ESPACIO DE TRABAJO</div>
        <button className="business-switcher" type="button">
          <span className="business-avatar">P</span>
          <span className="business-name"><strong>Panadería La Plaza</strong><small>Perfil de negocio</small></span>
          <span className="switcher-chevron" aria-hidden="true">⌄</span>
        </button>

        <nav className="main-nav" aria-label="Navegación principal">
          <a className="nav-item active" href="#" aria-current="page"><span className="nav-icon">✳</span> Crear contenido</a>
          <a className="nav-item muted" href="#"><span className="nav-icon">▤</span> Borradores <span className="nav-count">3</span></a>
          <a className="nav-item muted" href="#"><span className="nav-icon">◷</span> Historial</a>
        </nav>

        <div className="sidebar-bottom">
          <div className="help-card">
            <span className="help-spark">✦</span>
            <strong>Tu criterio primero</strong>
            <p>La IA propone. Tú revisas, editas y decides qué publicar.</p>
          </div>
          <button className="profile-button" type="button">
            <span className="profile-avatar">GG</span>
            <span><strong>Gabriela</strong><small>Content manager</small></span>
            <span className="switcher-chevron">⌄</span>
          </button>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div className="breadcrumb">Contenido <span>/</span> <strong>Nuevo borrador</strong></div>
          <div className="topbar-right"><span className="prototype-pill"><span /> Prototipo</span><button className="icon-button" type="button" aria-label="Ayuda">?</button></div>
        </header>

        <div className="content">
          <div className="page-heading">
            <div>
              <p className="eyebrow">ESTUDIO DE CONTENIDO</p>
              <h1>¿Qué vamos a contar?</h1>
              <p className="subheading">Cuéntanos lo esencial. Prepararemos un borrador para que lo hagas tuyo.</p>
            </div>
            <div className="step-indicator"><span className="step-number">01</span><span>Brief <i /> Revisión</span></div>
          </div>

          <div className="editor-grid">
            <section className="brief-card" aria-labelledby="brief-title">
              <div className="card-heading">
                <div><span className="section-kicker">PASO 1 · BRIEF</span><h2 id="brief-title">Danos un poco de contexto</h2></div>
                <span className="required-note"><span>*</span> Obligatorio</span>
              </div>

              <label className="field-label" htmlFor="topic">¿Qué quieres comunicar? <span>*</span></label>
              <textarea id="topic" className="text-input topic-input" value={topic} onChange={(e) => setTopic(e.target.value)} rows={2} placeholder="Ej. Nuevo menú de temporada" />
              <p className="field-hint">Un tema, novedad u oferta para empezar.</p>

              <div className="form-row">
                <div className="field-group">
                  <label className="field-label" htmlFor="goal">Objetivo <span>*</span></label>
                  <select id="goal" className="text-input select-input" value={goal} onChange={(e) => setGoal(e.target.value)}>
                    <option>Dar a conocer el producto</option><option>Generar visitas al local</option><option>Crear comunidad</option><option>Resolver una duda frecuente</option>
                  </select>
                </div>
                <div className="field-group">
                  <label className="field-label" htmlFor="platform">Canal <span>*</span></label>
                  <select id="platform" className="text-input select-input" value={platform} onChange={(e) => setPlatform(e.target.value as Platform)}>
                    <option>Instagram</option><option>Facebook</option>
                  </select>
                </div>
              </div>

              <label className="field-label" htmlFor="audience">¿A quién hablamos?</label>
              <input id="audience" className="text-input" value={audience} onChange={(e) => setAudience(e.target.value)} placeholder="Ej. Clientes que vienen a desayunar" />
              <p className="field-hint">Puedes describir a las personas o dejarlo en blanco si aún no lo sabes.</p>

              <div className="form-row">
                <div className="field-group">
                  <label className="field-label" htmlFor="format">Formato</label>
                  <select id="format" className="text-input select-input" value={format} onChange={(e) => setFormat(e.target.value as Format)}>
                    <option>Publicación</option><option>Carrusel</option><option>Reel</option>
                  </select>
                </div>
                <div className="field-group">
                  <label className="field-label" htmlFor="notes">Detalle opcional</label>
                  <input id="notes" className="text-input" value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Dato, tono o límite a tener en cuenta" />
                </div>
              </div>

              <div className="context-note"><span className="note-icon">✦</span><p><strong>Contexto del negocio disponible</strong><br />Usaremos la información aprobada del perfil. Si falta un dato importante, te lo señalaremos.</p><span className="note-check">✓</span></div>

              <div className="form-footer"><span><span className="lock-icon">◇</span> Tus cambios se quedan en este prototipo</span><button className="primary-button" type="button" onClick={generateDraft} disabled={!topic.trim()}><span>Preparar borrador</span><span className="button-arrow">↗</span></button></div>
            </section>

            <section className="preview-card" aria-labelledby="preview-title">
              <div className="preview-topline"><span className="section-kicker">VISTA PREVIA</span><span className="preview-live"><span /> {generated ? "BORRADOR" : "EN ESPERA"}</span></div>
              <div className="preview-title-row"><h2 id="preview-title">{generated ? "Tu primera propuesta" : "Aquí empieza la idea"}</h2><span className="preview-menu">···</span></div>
              <div className="social-preview">
                <div className="social-head"><span className="social-avatar">P</span><span className="social-account"><strong>panaderialaplaza</strong><small>{platform} · Vista previa</small></span><span className="social-more">•••</span></div>
                <div className="visual-placeholder"><div className="visual-stamp">HECHO<br />CADA DÍA</div><span className="visual-sun" /><div className="bread-shape"><i /><i /><i /></div><div className="visual-caption">Un buen día<br /><em>empieza aquí.</em></div><span className="visual-label">{format.toUpperCase()}</span></div>
                <div className="social-actions"><span>♡</span><span>▢</span><span>➤</span><span className="social-save">♧</span></div>
                <div className="social-copy">{generated ? <><strong>panaderialaplaza</strong> <textarea className="draft-edit" aria-label="Editar texto del borrador" value={copy} onChange={(e) => setCopy(e.target.value)} rows={4} /><button className="copy-button" type="button" onClick={copyDraft}>{copied ? "Copiado" : "Copiar texto"}</button></> : <p className="placeholder-copy">Tu texto aparecerá aquí cuando prepares un borrador.</p>}</div>
              </div>
              <div className="preview-footnote"><span>✦</span><p>La vista visual es orientativa. Revisa el texto y los datos antes de usarlo.</p></div>
              {generated && <div className="assumption-tag"><span>i</span> Revisa que todos los detalles del negocio sean correctos</div>}
            </section>
          </div>
          <footer className="page-footer"><span>Hecho para crear con intención.</span><span>Los borradores necesitan tu revisión antes de compartirse.</span></footer>
        </div>
      </section>
    </main>
  );
}