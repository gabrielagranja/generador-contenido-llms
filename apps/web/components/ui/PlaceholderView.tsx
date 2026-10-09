import { Kicker } from "./Kicker";
import styles from "./ui.module.css";

export function PlaceholderView({ title, description }: { title: string; description: string }) {
  return (
    <section className={styles.placeholder} aria-labelledby="view-title">
      <Kicker>No disponible en el MVP</Kicker>
      <h1 id="view-title">{title}</h1>
      <p>{description}</p>
      <p className={styles.placeholderNote}>
        Esta sección es un marcador de posición. No contiene datos ni funciones operativas.
      </p>
    </section>
  );
}
