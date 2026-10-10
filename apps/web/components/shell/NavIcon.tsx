import type { ViewId } from "../../domain/types.ts";

/** Minimal outline icons drawn inline (no icon dependency). Decorative: the label carries the meaning. */
const paths: Record<string, string[]> = {
  dashboard: ["M3 11.5 12 4l9 7.5", "M5 10v9.5h14V10", "M10 19.5v-5h4v5"],
  "content-studio": ["M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z", "M18.5 15.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"],
  drafts: ["M7 3h7l5 5v13H7z", "M14 3v5h5", "M10 13h6M10 17h6"],
  calendar: ["M4 6h16v14H4z", "M4 10h16", "M8 3v5M16 3v5"],
  history: ["M12 7v5l3 2", "M4 12a8 8 0 1 0 2.5-5.8", "M4 4v4h4"],
  library: ["M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"],
  analytics: ["M5 20V11M12 20V5M19 20v-7"],
  brands: ["M4 9l1.5-5h13L20 9", "M4 9h16v1.5a2.7 2.7 0 0 1-5.3 0 2.7 2.7 0 0 1-5.4 0A2.7 2.7 0 0 1 4 10.5z", "M5.5 13v7h13v-7"],
  settings: ["M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z", "M19 12a7 7 0 0 0-.1-1.2l2-1.5-2-3.4-2.3.9a7 7 0 0 0-2-1.2L14.3 3h-4l-.4 2.6a7 7 0 0 0-2 1.2l-2.3-.9-2 3.4 2 1.5a7 7 0 0 0 0 2.4l-2 1.5 2 3.4 2.3-.9a7 7 0 0 0 2 1.2l.4 2.6h4l.4-2.6a7 7 0 0 0 2-1.2l2.3.9 2-3.4-2-1.5c.1-.4.1-.8.1-1.2z"],
};

export function NavIcon({ id }: { id: ViewId }) {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      {(paths[id] ?? paths.dashboard).map((d) => <path key={d} d={d} />)}
    </svg>
  );
}
