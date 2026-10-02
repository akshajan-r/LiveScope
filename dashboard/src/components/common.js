import {html} from "npm:htl";
import * as Plot from "npm:@observablehq/plot";

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
  // An empty html`` is null, which display() would print as "null".
  if (meta.source === "twitch") return html`<span hidden></span>`;
  return html`<div class="banner">Synthetic demo data. These numbers come from livescope.demo, not from Twitch, and say nothing about real creators.</div>`;
}

export function skipped(meta, key) {
  const a = meta.analyses?.[key];
  if (!a || a.status === "ok") return null;
  return html`<p class="skipped">Not available yet: ${a.reason}. This fills in automatically once enough weeks of data have been collected.</p>`;
}

// Legend: [label, color] pairs; a third element "hollow" draws an outlined swatch.
export function key(items) {
  return html`<div>${items.map(([label, color, style]) => html`<span class="key"><i style=${style === "hollow"
    ? `background:none;border:1.5px solid ${color};box-sizing:border-box`
    : `background:${color}`}></i>${label}</span>`)}</div>`;
}

// Arrow/DuckDB timestamps can arrive as numbers or Dates; normalise to Date.
export const toDate = (d) => (d instanceof Date ? d : new Date(typeof d === "bigint" ? Number(d) : d));

// Categorical slots in fixed order. Colour follows the entity, never its rank.
export const SLOTS = Array.from({length: 8}, (_, i) => `var(--series-${i + 1})`);

// Fixed segment order so a segment keeps its colour across builds and pages.
const SEGMENT_ORDER = ["Rising stars", "Established", "Steady niche", "High-volume streamers",
  "Prime-time streamers", "Occasional", "At risk"];
export function segmentColors(names) {
  const known = SEGMENT_ORDER.filter((n) => names.includes(n));
  const extra = names.filter((n) => !SEGMENT_ORDER.includes(n)).sort();
  const domain = [...known, ...extra].slice(0, 8);
  return {domain, range: domain.map((_, i) => SLOTS[i])};
}

// Language groups in a fixed order with fixed slots.
export const LANGUAGE_GROUPS = ["English", "EU/EEA languages", "Spanish & Portuguese", "Other"];
export const languageColor = {domain: LANGUAGE_GROUPS, range: SLOTS.slice(0, 4)};

// Kaplan-Meier step curve with a 10% confidence band.
export function kmPlot(curves, groups, colors, {width, height = 300} = {}) {
  const rows = curves.filter((d) => groups.includes(d.group));
  return Plot.plot({
    width, height, marginLeft: 48,
    x: {label: "Weeks since entering the top list", ticks: Math.max(...rows.map((d) => d.time), 1), tickFormat: "d"},
    y: {domain: [0, 1], grid: true, label: "Still streaming", tickFormat: "%"},
    color: {domain: groups, range: colors, legend: false},
    marks: [
      Plot.areaY(rows, {x: "time", y1: "ci_low", y2: "ci_high", fill: "group", fillOpacity: 0.1, curve: "step-after"}),
      Plot.lineY(rows, {x: "time", y: "survival", stroke: "group", strokeWidth: 2, curve: "step-after"}),
      Plot.dot(rows, {x: "time", y: "survival", fill: "group", r: 4, stroke: "var(--theme-background)", strokeWidth: 2,
        tip: true, title: (d) => `${d.group}\nweek ${d.time}: ${(d.survival * 100).toFixed(0)}% still streaming\n95% CI ${(d.ci_low * 100).toFixed(0)}–${(d.ci_high * 100).toFixed(0)}%\n${d.at_risk} at risk`}),
      Plot.ruleY([0], {stroke: "var(--baseline)"})
    ]
  });
}

// Sequential blue ramp: the low end sits close to the surface in each mode,
// so "near zero" recedes and high values stand out.
export function sequentialRange() {
  const dark = typeof window !== "undefined" && window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  return dark ? ["#104281", "#86b6ef"] : ["#cde2fb", "#0d366b"];
}
