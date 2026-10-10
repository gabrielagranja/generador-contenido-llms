"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type {
  BrandId,
  BriefForm,
  CommerceId,
  DraftPreparationStatus,
  HistoryEntry,
  LocalDraft,
  ViewId,
} from "../domain/types.ts";
import { brandContexts, dashboardFixtures, draftFixtures, getBriefDefaults, historyFixtures } from "../domain/fixtures.ts";
import {
  afterBriefChange,
  afterTextChange,
  approve,
  missingBriefFields,
  requestChanges,
  resubmit,
  statusFromDraft,
} from "../domain/editorial.ts";
import { AppShell } from "./shell/AppShell";
import { BrandSwitcher } from "./shell/BrandSwitcher";
import { Dashboard } from "./dashboard/Dashboard";
import { DraftsView } from "./drafts/DraftsView";
import { HistoryView } from "./history/HistoryView";
import { ContentStudio } from "./studio/ContentStudio";
import { PlaceholderView } from "./ui/PlaceholderView";

const viewTitles: Record<ViewId, string> = {
  dashboard: "Dashboard",
  "content-studio": "Content Studio",
  drafts: "Borradores",
  history: "Historial",
  calendar: "Calendar",
  library: "Library",
  analytics: "Analytics",
  brands: "Brands & Stores",
  settings: "Settings",
};

const placeholders: Partial<Record<ViewId, string>> = {
  calendar: "Planificación de publicaciones por fecha y canal.",
  library: "Biblioteca de contenidos y materiales de la marca.",
  analytics: "Rendimiento real de las publicaciones. Requiere cuentas conectadas, que no existen en el MVP.",
  brands: "Gestión de marcas, comercios asociados y perfiles sociales.",
  settings: "Configuración de la plataforma y de cada marca, incluidos sus materiales y fuentes.",
};

export function Workspace() {
  const [view, setView] = useState<ViewId>("dashboard");
  const [brandId, setBrandId] = useState<BrandId>("panaderia");
  const [commerceId, setCommerceId] = useState<CommerceId | null>(null);

  const brand = useMemo(
    () => brandContexts.find((context) => context.id === brandId) ?? brandContexts[0],
    [brandId],
  );
  const activeCommerce = useMemo(
    () => brand.commerceOptions?.find((commerce) => commerce.id === commerceId),
    [brand, commerceId],
  );
  const activeContext = activeCommerce ?? brand;
  const theme = activeCommerce?.theme ?? brand.theme;
  const dashboard = dashboardFixtures[activeContext.account] ?? dashboardFixtures.panaderialaplaza;
  const contextName = activeCommerce ? brand.name + " · " + activeCommerce.name : brand.name;
  const [sessionDraftsByContext, setSessionDraftsByContext] = useState<Record<string, LocalDraft[]>>({});
  const [sessionHistoryByContext, setSessionHistoryByContext] = useState<Record<string, HistoryEntry[]>>({});
  const [activeSessionDraftId, setActiveSessionDraftId] = useState<string | null>(null);
  const sessionDraftSequence = useRef(0);
  const sessionHistorySequence = useRef(0);
  const drafts = [
    ...(sessionDraftsByContext[activeContext.account] ?? []),
    ...(draftFixtures[activeContext.account] ?? []),
  ];
  const historyEntries = [
    ...(sessionHistoryByContext[activeContext.account] ?? []),
    ...(historyFixtures[activeContext.account] ?? []),
  ];
  const dashboardWithSessionState = {
    ...dashboard,
    drafts: dashboard.drafts + drafts.filter((draft) => draft.id.startsWith("session-") && draft.status === "draft").length,
    review: dashboard.review + drafts.filter((draft) => draft.id.startsWith("session-") && draft.status === "review").length,
    approved: dashboard.approved + drafts.filter((draft) => draft.id.startsWith("session-") && draft.status === "approved").length,
  };

  const [brief, setBrief] = useState<BriefForm>(() => getBriefDefaults(activeContext.account));
  const [previewCopy, setPreviewCopy] = useState("");
  const [status, setStatus] = useState<DraftPreparationStatus>("not-prepared");
  const [validationMessage, setValidationMessage] = useState("");
  const [isPreparing, setIsPreparing] = useState(false);

  useEffect(() => {
    setBrief(getBriefDefaults(activeContext.account));
    setPreviewCopy("");
    setStatus("not-prepared");
    setValidationMessage("");
    setActiveSessionDraftId(null);
  }, [activeContext.account, contextName]);

  function updateBrief(field: keyof BriefForm, value: string) {
    const nextBrief = { ...brief, [field]: value };
    setBrief(nextBrief);
    setStatus(afterBriefChange);
    updateSessionDraft({ brief: nextBrief, title: nextBrief.campaign.trim() || nextBrief.objective.trim(), status: "draft" });
    setValidationMessage("");
  }

  function updateSessionDraft(patch: Partial<LocalDraft>) {
    if (!activeSessionDraftId) return;
    setSessionDraftsByContext((current) => ({
      ...current,
      [activeContext.account]: (current[activeContext.account] ?? []).map((draft) =>
        draft.id === activeSessionDraftId ? { ...draft, ...patch } : draft,
      ),
    }));
  }

  function recordSessionHistory(draftId: string, eventStatus: HistoryEntry["status"], text: string) {
    if (!draftId.startsWith("session-")) return;
    const entry: HistoryEntry = {
      id: `session-history-${activeContext.account}-${++sessionHistorySequence.current}`,
      text,
      time: "Ahora",
      status: eventStatus,
      draftId,
      source: "session",
    };
    setSessionHistoryByContext((current) => ({
      ...current,
      [activeContext.account]: [entry, ...(current[activeContext.account] ?? [])],
    }));
  }

  function updateCopy(value: string) {
    setPreviewCopy(value);
    setStatus(afterTextChange);
    const nextStatus = status === "approved" ? "draft" : status === "pending-review" ? "review" : undefined;
    updateSessionDraft({ copy: value, ...(nextStatus ? { status: nextStatus } : {}) });
  }

  function approveCurrentDraft() {
    if (status !== "pending-review") return;
    setStatus(approve);
    updateSessionDraft({ status: "approved" });
    if (activeSessionDraftId) recordSessionHistory(activeSessionDraftId, "approved", "El borrador fue aprobado en esta sesión.");
  }

  function requestCurrentChanges() {
    if (status !== "pending-review") return;
    setStatus(requestChanges);
    updateSessionDraft({ status: "draft" });
    if (activeSessionDraftId) recordSessionHistory(activeSessionDraftId, "changes-requested", "Se solicitaron cambios para este borrador.");
  }

  function resubmitCurrentDraft() {
    if (status !== "changes-requested") return;
    setStatus(resubmit);
    updateSessionDraft({ status: "review" });
    if (activeSessionDraftId) recordSessionHistory(activeSessionDraftId, "review", "El borrador volvió a revisión humana.");
  }

  async function prepareDraft() {
    if (missingBriefFields(brief)) {
      setValidationMessage("Completa el objetivo, la audiencia y la campaña para preparar el borrador.");
      return;
    }
    setIsPreparing(true);
    setValidationMessage("");
    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";
    const format = brief.format === "Reel" ? "reel" : brief.format === "Carrusel" ? "carousel" : "single_image";

    try {
      const response = await fetch(`${apiBaseUrl}/drafts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          brief: {
            topic_or_offer: brief.campaign.trim(),
            objective: brief.objective.trim(),
            audience_context: brief.audience.trim(),
            business_context_refs: [activeContext.account],
            platforms: [brief.platform.toLowerCase()],
            format,
            brand_and_constraints: brief.restrictions.trim() || activeContext.summary,
            notes: "Generated from Content Studio local workspace.",
            facts: [],
          },
        }),
      });
      const payload = (await response.json()) as { detail?: string; drafts?: Array<{ caption?: string }> };
      if (!response.ok) {
        throw new Error(payload.detail || `La API respondió con estado ${response.status}.`);
      }
      const copy = payload.drafts?.[0]?.caption?.trim();
      if (!copy) throw new Error("La API no devolvió un borrador editable.");

      const sessionDraft: LocalDraft = {
        id: `session-${activeContext.account}-${++sessionDraftSequence.current}`,
        title: brief.campaign.trim() || brief.objective.trim(),
        platform: brief.platform,
        format: brief.format,
        status: "review",
        updatedAt: "Ahora · sesión actual",
        brief,
        copy,
      };
      setSessionDraftsByContext((current) => ({
        ...current,
        [activeContext.account]: [sessionDraft, ...(current[activeContext.account] ?? [])],
      }));
      setActiveSessionDraftId(sessionDraft.id);
      setPreviewCopy(copy);
      setStatus("pending-review");
      recordSessionHistory(sessionDraft.id, "review", "Se preparó el borrador con la API y quedó pendiente de revisión humana.");
    } catch (error) {
      setValidationMessage(error instanceof Error ? error.message : "No se pudo conectar con la API de generación.");
    } finally {
      setIsPreparing(false);
    }
  }

  function openDraft(draft: LocalDraft) {
    setBrief(draft.brief);
    setPreviewCopy(draft.copy);
    setStatus(statusFromDraft(draft.status));
    setActiveSessionDraftId(draft.id.startsWith("session-") ? draft.id : null);
    setValidationMessage("");
    setView("content-studio");
  }

  function selectBrand(nextBrandId: BrandId) {
    const next = brandContexts.find((context) => context.id === nextBrandId);
    if (!next) return;
    setBrandId(next.id);
    setCommerceId(next.commerceOptions?.[0]?.id ?? null);
  }

  function selectCommerce(nextCommerceId: CommerceId) {
    if (brand.commerceOptions?.some((commerce) => commerce.id === nextCommerceId)) {
      setCommerceId(nextCommerceId);
    }
  }

  const trail = [brand.name, ...(activeCommerce ? [activeCommerce.name] : []), viewTitles[view]];

  return (
    <AppShell
      view={view}
      onNavigate={setView}
      draftCount={drafts.length}
      theme={theme}
      trail={trail}
      switcher={
        <BrandSwitcher
          brands={brandContexts}
          brand={brand}
          commerceId={commerceId}
          onSelectBrand={selectBrand}
          onSelectCommerce={selectCommerce}
        />
      }
    >
      {view === "dashboard" && (
        <Dashboard
          contextName={contextName}
          kind={activeCommerce ? activeCommerce.sector : brand.kind}
          summary={activeContext.summary}
          handle={activeContext.account}
          theme={theme}
          fixture={dashboardWithSessionState}
          onCreate={() => setView("content-studio")}
        />
      )}
      {view === "drafts" && (
        <DraftsView
          contextName={contextName}
          handle={activeContext.account}
          theme={theme}
          drafts={drafts}
          onOpenDraft={openDraft}
        />
      )}
      {view === "history" && (
        <HistoryView
          contextName={contextName}
          entries={historyEntries}
          drafts={drafts}
          onOpenDraft={openDraft}
        />
      )}
      {view === "content-studio" && (
        <ContentStudio
          contextName={contextName}
          contextSummary={activeContext.summary}
          contextSector={activeCommerce?.sector}
          handle={activeContext.account}
          theme={theme}
          brief={brief}
          previewCopy={previewCopy}
          status={status}
          validationMessage={validationMessage}
          onBriefChange={updateBrief}
          onCopyChange={updateCopy}
          onPrepare={prepareDraft}
          isPreparing={isPreparing}
          onApprove={approveCurrentDraft}
          onRequestChanges={requestCurrentChanges}
          onResubmit={resubmitCurrentDraft}
        />
      )}
      {placeholders[view] && <PlaceholderView title={viewTitles[view]} description={placeholders[view]!} />}
    </AppShell>
  );
}
