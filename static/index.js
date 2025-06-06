"use strict";

const DIST_MAX = 100;
const PAGE = {size: 0, index: 0};

const COLOR_CLASS = {
	slate: "bg-slate-500", gray: "bg-gray-500", zinc: "bg-zinc-500",
	red: "bg-red-500", orange: "bg-orange-500", amber: "bg-amber-500", yellow: "bg-yellow-500",
	green: "bg-green-500", teal: "bg-teal-500", cyan: "bg-cyan-500", blue: "bg-blue-500",
	indigo: "bg-indigo-500", violet: "bg-violet-500", purple: "bg-purple-500", pink: "bg-pink-500"
};

const carsDiv = document.getElementById("cars");
const logBox = document.getElementById("logBox");
const fullBtn = document.getElementById("fullBtn");
const stepBtn = document.getElementById("stepBtn");
const resetBtn = document.getElementById("resetBtn");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");
const filterSel = document.getElementById("filter");

let ws = null;
let logs = [];
let cards = {};
let filter = "";

const pagerDiv = (() => {
	const d = document.createElement("div");
	d.className = "flex flex-wrap gap-1 justify-center flex-1";
	prevBtn.parentNode.insertBefore(d, nextBtn);
	return d;
})();

function computePageSize() {
	const lh = parseInt(getComputedStyle(logBox).lineHeight || 16, 10);
	PAGE.size = Math.max(1, Math.floor(logBox.clientHeight / lh) - 1);
}

window.addEventListener("resize", () => {
	computePageSize();
	renderPage();
});

function progressClass(c) {
	return COLOR_CLASS[c] ?? "bg-gray-500";
}

function createCard(d) {
	const div = document.createElement("div");
	div.className = "bg-white rounded-2xl shadow p-4 space-y-2";
	div.innerHTML = `
    <h3 class="text-xl font-semibold">${d.pilot}</h3>
    <div class="h-2 bg-gray-200 rounded">
      <div class="progress h-full ${progressClass(d.color)} rounded"></div>
    </div>
    <div class="text-sm"><span class="km"></span> | <span class="essence"></span></div>
    <div class="text-sm text-gray-500 rank"></div>`;
	return div;
}

function renderCard(card, d) {
	card.querySelector(".km").textContent = `${d.km} km`;
	card.querySelector(".essence").textContent = `${d.tank} L`;
	card.querySelector(".rank").textContent = `#${d.rank}`;
	card.querySelector(".progress").style.width = Math.min(100, d.km / DIST_MAX * 100) + "%";
	card.classList.toggle("opacity-50", !d.wheel_ok || d.tank === 0);
}

function updateCars(cars) {
	cars.sort((a, b) => a.rank - b.rank);
	const pilots = [...new Set(cars.map(c => c.pilot))].sort();
	filterSel.innerHTML = `<option value="">Toutes</option>` + pilots.map(p => `<option value="${p.toLowerCase()}">${p}</option>`).join("");
	carsDiv.innerHTML = "";
	cars.forEach(c => {
		const card = cards[c.id] ?? createCard(c);
		renderCard(card, c);
		carsDiv.appendChild(card);
		cards[c.id] = card;
	});
}

function filteredLogs() {
	return filter ? logs.filter(l => l.toLowerCase().includes(filter)) : logs;
}

function buildPager(pages) {
	pagerDiv.innerHTML = "";
	for (let i = 0; i < pages; i++) {
		const b = document.createElement("button");
		b.textContent = i + 1;
		b.className = `px-2 py-1 rounded ${i === PAGE.index ? "bg-indigo-600 text-white" : "bg-white border"}`;
		b.onclick = () => {
			PAGE.index = i;
			renderPage();
		};
		pagerDiv.appendChild(b);
	}
}

function renderPage() {
	if (!PAGE.size) {
		computePageSize();
	}
	const arr = filteredLogs();
	const pages = Math.max(1, Math.ceil(arr.length / PAGE.size));
	PAGE.index = Math.min(PAGE.index, pages - 1);
	const slice = arr.slice(PAGE.index * PAGE.size, (PAGE.index + 1) * PAGE.size);
	logBox.textContent = slice.join("\n");
	prevBtn.disabled = PAGE.index === 0;
	nextBtn.disabled = PAGE.index >= pages - 1;
	buildPager(pages);
}

function pushEvents(evts) {
	if (!evts.length) {
		return;
	}
	logs.push(...evts);
	if (evts.at(-1) === "[FIN]") {
		stepBtn.disabled = true;
	}
	const len = filteredLogs().length;
	const pages = Math.ceil(len / PAGE.size);
	PAGE.index = pages - 1;
	renderPage();
}

function clearState() {
	logs = [];
	cards = {};
	filter = "";
	PAGE.index = 0;
	carsDiv.innerHTML = "";
	logBox.textContent = "";
	pagerDiv.innerHTML = "";
	prevBtn.disabled = nextBtn.disabled = true;
}

function runFullRace() {
	ws = new WebSocket(`ws://${location.host}/ws/race`);
	fullBtn.disabled = stepBtn.disabled = true;
	ws.onmessage = ({data}) => {
		const {cars, events} = JSON.parse(data);
		updateCars(cars);
		pushEvents(events);
		if (events.includes("[FIN]")) {
			ws.close();
		}
	};
}

async function runOneTurn() {
	const r = await fetch("/step", {method: "POST"});
	const {cars, events, finished} = await r.json();
	updateCars(cars);
	pushEvents(events);
	if (finished) {
		fullBtn.disabled = stepBtn.disabled = true;
	}
}

resetBtn.onclick = async () => {
	fullBtn.disabled = stepBtn.disabled = true;
	await fetch("/reset", {method: "POST"});
	ws && ws.close();
	clearState();
	fullBtn.disabled = stepBtn.disabled = false;
};

fullBtn.onclick = () => {
	if (!ws || ws.readyState !== 1) {
		clearState();
		runFullRace();
	}
};
stepBtn.onclick = () => {
	fullBtn.disabled = true;
	runOneTurn();
};

prevBtn.onclick = () => {
	if (PAGE.index) {
		PAGE.index--;
		renderPage();
	}
};
nextBtn.onclick = () => {
	PAGE.index++;
	renderPage();
};
filterSel.onchange = () => {
	filter = filterSel.value.toLowerCase();
	PAGE.index = 0;
	renderPage();
};

const rulesModal = document.getElementById("rulesModal");
const rulesBtn = document.getElementById("rulesBtn");
const closeRulesModal = document.getElementById("closeRulesModal");
const rulesForm = document.getElementById("rulesForm");
const ruleTpl = document.getElementById("ruleInput").content;
const saveRules = document.getElementById("saveRules");

function show(el) {
	el.classList.remove("hidden");
	el.classList.add("flex");
}

function hide(el) {
	el.classList.add("hidden");
	el.classList.remove("flex");
}

rulesBtn.onclick = async () => {
	const data = await (await fetch("/rules")).json();
	rulesForm.innerHTML = "";
	Object.entries(data).forEach(([k, v]) => {
		const row = ruleTpl.cloneNode(true);
		row.querySelector(".rule-name").textContent = k;
		const inp = row.querySelector(".rule-value");
		inp.value = v;
		inp.dataset.key = k;
		rulesForm.appendChild(row);
	});
	show(rulesModal);
};
closeRulesModal.onclick = () => hide(rulesModal);

saveRules.onclick = async () => {
	const obj = {};
	rulesForm.querySelectorAll(".rule-value").forEach(inp => {
		const val = parseFloat(inp.value);
		if (!isNaN(val)) {
			obj[inp.dataset.key] = val;
		}
	});
	await fetch("/rules", {method: "PATCH", headers: {"Content-Type": "application/json"}, body: JSON.stringify(obj)});
	hide(rulesModal);
	await fetch("/reset", {method: "POST"});
};

computePageSize();
renderPage();
