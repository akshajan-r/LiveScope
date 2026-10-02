import {html} from "npm:htl";

export const fmt = {
  int: (d) => (d == null ? "–" : Math.round(d).toLocaleString("en-US")),
  compact: (d) => (d == null ? "–" : new Intl.NumberFormat("en-US", {notation: "compact", maximumFractionDigits: 1}).format(d)),
  pct: (d, digits = 1) => (d == null || Number.isNaN(d) ? "–" : `${(d * 100).toFixed(digits)}%`),
  signedPct: (d, digits = 1) => (d == null || Number.isNaN(d) ? "–" : `${d >= 0 ? "+" : "−"}${Math.abs(d * 100).toFixed(digits)}%`),
  num: (d, digits = 3) => (d == null || Number.isNaN(d) ? "–" : d.toFixed(digits)),
  date: (d) => (d == null ? "–" : new Date(d).toISOString().slice(0, 10))
};

// Shown on every page when the data store holds synthetic demo data.
export function sourceBanner(meta) {
  if (meta.source === "twitch") return html``;
  return html`<div class="banner">Synthetic demo data. These numbers come from livescope.demo, not from Twitch, and say nothing about real creators.</div>`;
}

export function skipped(meta, key) {
  const a = meta.analyses?.[key];
  if (!a || a.status === "ok") return null;
  return html`<p class="skipped">Not available yet: ${a.reason}. This fills in automatically once enough weeks of data have been collected.</p>`;
}

export function key(items) {
  return html`<div>${items.map(([label, color]) => html`<span class="key"><i style="background:${color}"></i>${label}</span>`)}</div>`;
}

// Arrow/DuckDB timestamps can arrive as numbers or Dates; normalise to Date.
export const toDate = (d) => (d instanceof Date ? d : new Date(typeof d === "bigint" ? Number(d) : d));
