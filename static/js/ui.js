// -----------------------------------------------------------------------------
//  ui.js – composants visuels et helpers DOM
// -----------------------------------------------------------------------------

// Palette Tailwind pour la barre de progression / select couleur
export const COLOR_CLASS = {
  slate: "bg-slate-500", gray: "bg-gray-500", zinc: "bg-zinc-500",
  red: "bg-red-500", orange: "bg-orange-500", amber: "bg-amber-500", yellow: "bg-yellow-500",
  green: "bg-green-500", teal: "bg-teal-500", cyan: "bg-cyan-500", blue: "bg-blue-500",
  indigo: "bg-indigo-500", violet: "bg-violet-500", purple: "bg-purple-500", pink: "bg-pink-500"
};
export const COLOR_KEYS = Object.keys(COLOR_CLASS);

export function elt(tag, cls = "", html = "") {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html) e.innerHTML = html;
  return e;
}

// Progress-bar helper (course)
export function progressClass(color) {
  return COLOR_CLASS[color] ?? "bg-gray-500";
}

// --------------------------- Voitures.html helpers ---------------------------
export function fillColorSelect(selectEl, carsCache, selected = null) {
  const used = new Set(carsCache.map(c => c.color));
  selectEl.innerHTML = "";
  COLOR_KEYS.forEach(col => {
    if (!used.has(col) || col === selected) {
      selectEl.appendChild(new Option(col, col));
    }
  });
  if (selected) selectEl.value = selected;
}

// --------------------------- Course (index.html) -----------------------------
export function createCarCard(data) {
  const card = elt("div", "bg-white rounded-2xl shadow p-4 space-y-2");
  card.innerHTML = `
    <h3 class="text-xl font-semibold">${data.pilot}</h3>
    <div class="h-2 bg-gray-200 rounded"><div class="progress h-full ${progressClass(data.color)} rounded"></div></div>
    <div class="text-sm"><span class="km"></span> | <span class="fuel"></span></div>
    <div class="text-sm text-gray-500 rank"></div>`;
  return card;
}
export function renderCarCard(card, data, distMax = 100) {
  card.querySelector(".km").textContent = `${data.km} km`;
  card.querySelector(".fuel").textContent = `${data.tank} L`;
  card.querySelector(".rank").textContent = `#${data.rank}`;
  card.querySelector(".progress").style.width = `${Math.min(100, data.km / distMax * 100)}%`;
  card.classList.toggle("opacity-50", !data.wheel_ok || data.tank === 0);
}