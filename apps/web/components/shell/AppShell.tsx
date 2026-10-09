"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";
import type { BrandTheme, ViewId } from "../../domain/types.ts";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import styles from "./shell.module.css";
import type { CSSProperties } from "react";

const SIDEBAR_ID = "app-sidebar";

export function AppShell({
  view,
  onNavigate,
  draftCount,
  switcher,
  trail,
  theme,
  children,
}: {
  view: ViewId;
  onNavigate: (view: ViewId) => void;
  draftCount: number;
  switcher: ReactNode;
  trail: string[];
  theme: BrandTheme;
  children: ReactNode;
}) {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuButtonRef = useRef<HTMLButtonElement>(null);
  const sidebarRef = useRef<HTMLElement>(null);
  const mainContentRef = useRef<HTMLElement>(null);

  useEffect(() => {
    if (!menuOpen) return;
    sidebarRef.current?.querySelector<HTMLElement>("select, button, a, input, textarea")?.focus();
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setMenuOpen(false);
        menuButtonRef.current?.focus();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [menuOpen]);

  const brandVars = {
    "--brand-accent": theme.accent,
    "--brand-ink": theme.ink,
    "--brand-tint": theme.tint,
  } as CSSProperties;

  return (
    <div className={styles.shell} style={brandVars}>
      <a className="skip-link" href="#main-content">Saltar al contenido</a>
      <Sidebar
        id={SIDEBAR_ID}
        view={view}
        draftCount={draftCount}
        switcher={switcher}
        open={menuOpen}
        sidebarRef={sidebarRef}
        onNavigate={(next) => {
          setMenuOpen(false);
          onNavigate(next);
          mainContentRef.current?.focus();
        }}
      />
      <div className={styles.main}>
        <Topbar
          trail={trail}
          menuButtonRef={menuButtonRef}
          menuOpen={menuOpen}
          menuControls={SIDEBAR_ID}
          onToggleMenu={() => setMenuOpen((open) => !open)}
        />
        <main id="main-content" ref={mainContentRef} className={styles.content} tabIndex={-1}>
          {children}
        </main>
        <footer className={styles.footer}>
          <span>Prototipo local · datos sintéticos · sin publicación real</span>
        </footer>
      </div>
    </div>
  );
}
