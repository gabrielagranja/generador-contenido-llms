import type { ReactNode } from "react";
import styles from "./ui.module.css";

export function Kicker({ children }: { children: ReactNode }) {
  return <p className={styles.kicker}>{children}</p>;
}

export function SyntheticNotice({ children }: { children: ReactNode }) {
  return <p className={styles.notice}>{children}</p>;
}
