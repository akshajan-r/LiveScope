// Observable Framework config. The pipeline (`python -m livescope build`) writes
// the data files; the workflow copies them into src/data before building.
export default {
  title: "LiveScope",
  root: "src",
  theme: ["air", "near-midnight"],
  style: "style.css",
  pages: [
    {name: "Overview", path: "/"},
    {name: "Creators & segments", path: "/creators"},
    {name: "Growth model", path: "/models"},
    {name: "Experiments", path: "/experiments"},
    {name: "Data & methods", path: "/methods"}
  ],
  head: '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22><circle cx=%228%22 cy=%228%22 r=%226%22 fill=%22%232a78d6%22/></svg>">',
  footer: 'Built from hourly Twitch Helix snapshots. Code: <a href="https://github.com/akshajan-r/LiveScope">github.com/akshajan-r/LiveScope</a>.',
  search: false,
  // Tables ship as Arrow IPC, which DuckDB-wasm reads natively, so the json and
  // parquet extensions are not needed (and not self-hosted).
  duckdb: {extensions: {json: null, parquet: null}}
};
