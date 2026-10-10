"use client";

import { useEffect, useState } from "react";
import { getPlans, type StoredPlan } from "../../domain/plans-api";

export function CalendarView() {
  const [plans, setPlans] = useState<StoredPlan[]>([]);
  const [error, setError] = useState("");
  useEffect(() => { getPlans().then(setPlans).catch((cause: Error) => setError(cause.message)); }, []);
  if (error) return <section><h2>Calendario editorial</h2><p>No se pudieron cargar los planes: {error}</p></section>;
  if (!plans.length) return <section><h2>Calendario editorial</h2><p>No hay planes guardados todavía.</p></section>;
  return <section><h2>Calendario editorial</h2>{plans.map(({ plan_id, plan }) => <article key={plan_id}><h3>{plan.starts_on} — {plan.ends_on}</h3>{plan.items.length ? <ul>{plan.items.map((item, index) => <li key={`${plan_id}-${index}`}>{item.bucket_key} · {item.platform} · {item.format}{item.review_state ? ` · ${item.review_state}` : ""}</li>)}</ul> : <p>Plan guardado sin contenidos asignados.</p>}</article>)}</section>;
}
