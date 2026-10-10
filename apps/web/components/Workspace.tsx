Warning: truncated output (original token count: 5404)
Total output lines: 475

"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type {
  BrandId,
  BriefForm,
  CommerceId,
  DraftPreparationStatus,
  HistoryEntry,
  LocalDraft,
  DraftEvidence,
  ViewId,
} from "../domain/types.ts";
import { canStartGeneration, parseDraftResponse, type GenerationState } from "../domain/draft-generation.ts";
import { createDraft, getDraft, reviewDraft, updateDraft, mapBriefToApi, type ApiEditorialContent } from "../domain/review-api.ts";
import { brandContexts, dashboardFixtures, draftFixtures, getBriefDefaults, historyFixtures } from "../domain/fixtures.ts";
import {
  afterBriefChange,
  afterTextChange,
  approve,
  missingBriefFields,
  requestChanges,
  resubmit,
  missingReviewer,
  statusFromDraft,
} from "../domain/editorial.ts";
import { AppShell } from "./shell/AppShell";
import { BrandSwitcher } from "./shell/BrandSwitcher";
import { Dashboard } from "./dashboard/Dashboard";
import { DraftsView } from "./drafts/DraftsView";
import { HistoryView } from "./history/HistoryView";
import { ContentStudio } from "./studio/ContentStudio";
import { PlaceholderView } from "./ui/PlaceholderView";
import { CalendarView } from "./calendar/CalendarView";

type DraftApiResponse = { detail?: string; drafts?: Array<{ caption?: string; evidence_provenance?: unknown; supported_claims?: unknown; unsupported_claims?: unknown }>; review_state?: "pending_human_review" };

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
  const [generationState, setGenerationState] = useState<GenerationState>("idle");
  const [previewEvidence, setPreviewEvidence] = useState<DraftEvidence[]>([]);
  const [supportedClaims, setSupportedClaims] = useState<string[]>([]);
  const [unsupportedClaims, setUnsupportedClaims] = useState<string[]>([]);
  const [reviewerName, setReviewerName] = useState("");
  const [reviewMessage, setReviewMessage] = useState("");
  const [reviewFeedback, setReviewFeedback] = useState("");
  const [activeBackendId, setActiveBackendId] = useState<string | null>(null);
  const requestSequence = useRef(0);

  useEffect(() => {
    setBrief(getBriefDefaults(activeContext.account));
    setPreviewCopy("");
    setStatus("not-prepared");
    setValidationMessage("");
    setGenerationState("idle");
    setPreviewEvidence([]);
    setSupportedClaims([]);
    setUnsupportedClaims([]);
    setReviewerName("");
    setReviewMessage("");
    setReviewFeedback("");
    setActiveBackendId(null);
    setActiveSessionDraftId(null);
    requestSequence.current += 1;
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
      [activeContext.account]: (current[activeContext.accoun…2404 tokens truncated…sponse.status, json: async () => payload },
        ragBusinessId,
      );
      if (!response.ok) {
        throw new Error(payload.detail || `La API respondió con estado ${response.status}.`);
      }
      if (payload.review_state !== "pending_human_review") {
        throw new Error("La API no confirm\u00f3 que el borrador quede pendiente de revisi\u00f3n humana.");
      }
      const copy = parsed.copy;
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
        evidenceProvenance: parsed.evidenceProvenance,
        supportedClaims: parsed.supportedClaims,
        unsupportedClaims: parsed.unsupportedClaims,
      };
      setSessionDraftsByContext((current) => ({
        ...current,
        [activeContext.account]: [sessionDraft, ...(current[activeContext.account] ?? [])],
      }));
      setActiveSessionDraftId(sessionDraft.id);
      setPreviewCopy(copy);
      setPreviewEvidence(parsed.evidenceProvenance);
      setSupportedClaims(parsed.supportedClaims);
      setUnsupportedClaims(parsed.unsupportedClaims);
      setStatus("pending-review");
      setGenerationState("success");
      recordSessionHistory(sessionDraft.id, "review", "Se preparó el borrador con la API y quedó pendiente de revisión humana.");
    } catch (error) {
      setGenerationState("error");
      setValidationMessage(error instanceof Error ? error.message : "No se pudo conectar con la API de generación.");
    }
  }

  async function openDraft(draft: LocalDraft) {
    setBrief(draft.brief);
    setPreviewCopy(draft.copy);
    setPreviewEvidence(draft.evidenceProvenance ?? []);
    setSupportedClaims(draft.supportedClaims ?? []);
    setUnsupportedClaims(draft.unsupportedClaims ?? []);
    setReviewerName(draft.reviewer ?? "");
    setReviewFeedback("");
    setReviewMessage("");
    setStatus(statusFromDraft(draft.status));
    setActiveSessionDraftId(draft.id.startsWith("session-") ? draft.id : null);
    setActiveBackendId(draft.backendId ?? null);
    setValidationMessage("");
    setView("content-studio");
    if (draft.backendId) {
      const requestVersion = ++requestSequence.current;
      try {
        const content = await getDraft(draft.backendId);
        if (requestVersion === requestSequence.current) applyBackendContent(content);
      } catch (error) {
        if (requestVersion === requestSequence.current) setValidationMessage(error instanceof Error ? error.message : "No se pudo recuperar el borrador.");
      }
    }
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
          generationState={generationState}
          evidenceProvenance={previewEvidence}
          supportedClaims={supportedClaims}
          unsupportedClaims={unsupportedClaims}
          reviewerName={reviewerName}
          reviewMessage={reviewMessage}
           reviewFeedback={reviewFeedback}
           onReviewFeedbackChange={(value) => { setReviewFeedback(value); setReviewMessage(""); }}
          onReviewerChange={(value) => { setReviewerName(value); setReviewMessage(""); }}
          onBriefChange={updateBrief}
          onCopyChange={updateCopy}
           onCopyBlur={saveCurrentEdit}
          onPrepare={prepareDraft}
          isPreparing={generationState === "loading"}
          onApprove={approveCurrentDraft}
          onRequestChanges={requestCurrentChanges}
          onResubmit={resubmitCurrentDraft}
        />
      )}
      {view === "calendar" && <CalendarView />}
      {placeholders[view] && <PlaceholderView title={viewTitles[view]} description={placeholders[view]!} />}
    </AppShell>
  );
}
