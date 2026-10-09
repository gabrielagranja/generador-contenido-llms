import type { RefObject } from "react";
import styles from "./shell.module.css";

export function Topbar({
  trail,
  menuOpen,
  menuControls,
  menuButtonRef,
  onToggleMenu,
}: {
  trail: string[];
  menuOpen: boolean;
  menuControls: string;
  menuButtonRef: RefObject<HTMLButtonElement | null>;
  onToggleMenu: () => void;
}) {
  return (
    <header className={styles.topbar}>
      <button
        type="button"
        ref={menuButtonRef}
        className={styles.menuButton}
        aria-expanded={menuOpen}
        aria-controls={menuControls}
        onClick={onToggleMenu}
      >
        Menú
      </button>
      <nav className={styles.breadcrumb} aria-label="Ubicación">
        {trail.map((part, index) => (
          <span key={part + index}>
            {index > 0 && <span className={styles.crumbSep} aria-hidden="true">/ </span>}
            {index === trail.length - 1 ? <strong>{part}</strong> : part}
          </span>
        ))}
      </nav>
    </header>
  );
}
