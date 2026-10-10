"use client";

import { useEffect, useState } from "react";
import styles from "./calendar.module.css";
import { getPlans, type StoredPlan } from "../../domain/plans-api";

export function CalendarView() {
  const [plans, setPlans] = useState<StoredPlan[]>([]);
  const [error, setError] = useState("");
  useEffect(() => { getPlans().then(setPlans).catch((cause: Error) => setError(cause.message)); }, []);
  if (error) return <section className={styles.view}><h2 className={styles.title}>Calendario editorial</h2><p className={`${styles.state} ${styles.stateError}`} role="alert">No se pudieron cargar los planes: {error}</p></section>;
  if (!plans.length) return <section className={styles.view}><h2 className={styles.title}>Calendario editorial</h2><p className={styles.state}>No hay planes guardados todavía.</p></section>;
  return <section className={styles.view}><h2 className={styles.title}>Calendario editorial</h2>{plans.map(({ plan_id, plan }) => <article className={styles.plan} key={plan_id}><h3 className={styles.range}>{plan.starts_on} — {plan.ends_on}</h3>{plan.items.length ? <ul className={styles.items}>{plan.items.map((item, index) => <li key={`${plan_id}-${index}`}>{item.bucket_key} · {item.platform} · {item.format}{item.review_state ? ` · ${item.review_state}` : ""}</li>)}</ul> : <p className={styles.muted}>Plan guardado sin contenidos asignados.</p>}</article>)}</section>;
}
