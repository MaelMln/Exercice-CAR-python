// -----------------------------------------------------------------------------
//  main.js – point d'entrée unique, dispatch selon la page
// -----------------------------------------------------------------------------

import * as api from "./api.js";
import {
	elt, COLOR_CLASS, fillColorSelect,
	createCarCard, renderCarCard
} from "./ui.js";

// Détection de page :
if (document.getElementById("carsTbody")) {
	initCarsPage();
} else if (document.getElementById("cars")) {
	initRacePage();
}

// =============================================================================
//  Page cars.html  ------------------------------------------------------------
// =============================================================================
function initCarsPage() {
	const tbody = document.getElementById("carsTbody");
	const fId = document.getElementById("fId");
	const fPilot = document.getElementById("fPilot");
	const fColor = document.getElementById("fColor");
	const fTank = document.getElementById("fTank");
	const btnCreate = document.getElementById("btnCreate");
	const btnUpdate = document.getElementById("btnUpdate");
	const btnDelete = document.getElementById("btnDelete");
	const btnCancel = document.getElementById("btnCancel");

	let carsCache = [];

	function clearForm() {
		fId.value = "";
		fPilot.value = "";
		fTank.value = "";
		fillColorSelect(fColor, carsCache);
		btnCreate.classList.remove("hidden");
		btnUpdate.classList.add("hidden");
		btnDelete.classList.add("hidden");
		btnCancel.classList.add("hidden");
	}

	function selectCar(c) {
		fId.value = c.id;
		fPilot.value = c.pilot;
		fTank.value = c.tank;
		fillColorSelect(fColor, carsCache, c.color);
		btnCreate.classList.add("hidden");
		btnUpdate.classList.remove("hidden");
		btnDelete.classList.remove("hidden");
		btnCancel.classList.remove("hidden");
	}

	async function refresh() {
		carsCache = await api.listCars();
		tbody.innerHTML = "";
		carsCache.forEach(c => {
			const tr = elt("tr", "cursor-pointer hover:bg-gray-100");
			tr.innerHTML = `
        <td class="border px-2 py-1">${c.id}</td>
        <td class="border px-2 py-1">${c.pilot || ""}</td>
        <td class="border px-2 py-1">${c.color}</td>
        <td class="border px-2 py-1">${c.tank}</td>`;
			tr.onclick = () => selectCar(c);
			tbody.appendChild(tr);
		});
		fillColorSelect(fColor, carsCache);
	}

	// ----- Events
	btnCreate.onclick = async () => {
		await api.createCar({pilot: fPilot.value, color: fColor.value, tank: +fTank.value});
		clearForm();
		await refresh();
	};
	btnUpdate.onclick = async () => {
		await api.updateCar(fId.value, {pilot: fPilot.value, color: fColor.value, tank: +fTank.value});
		clearForm();
		await refresh();
	};
	btnDelete.onclick = async () => {
		await api.deleteCar(fId.value);
		clearForm();
		await refresh();
	};
	btnCancel.onclick = clearForm;

	// init
	refresh();
}

// =============================================================================
//  Page index.html  -----------------------------------------------------------
// =============================================================================
function initRacePage() {
	// Constantes & state
	const DIST_MAX = 100;
	const PAGE = {size: 0, index: 0};

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
		const d = elt("div", "flex flex-wrap gap-1 justify-center flex-1");
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

	function updateCars(cars) {
		cars.sort((a, b) => a.rank - b.rank);
		const pilots = [...new Set(cars.map(c => c.pilot))].sort();
		filterSel.innerHTML = `<option value="">Toutes</option>` + pilots.map(p => `<option value="${p.toLowerCase()}">${p}</option>`).join("");
		carsDiv.innerHTML = "";
		cars.forEach(c => {
			const card = cards[c.id] ?? createCarCard(c);
			renderCarCard(card, c, DIST_MAX);
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
			const b = elt("button", `px-2 py-1 rounded ${i === PAGE.index ? "bg-indigo-600 text-white" : "bg-white border"}`, i + 1);
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

	async function runOneTurn() {
		const {cars, events, finished} = await api.stepRace();
		updateCars(cars);
		pushEvents(events);
		if (finished) {
			fullBtn.disabled = stepBtn.disabled = true;
		}
	}

	function runFullRace() {
		ws = api.raceSocket(({cars, events}) => {
			updateCars(cars);
			pushEvents(events);
		});
		fullBtn.disabled = stepBtn.disabled = true;
	}

	async function clearState() {
		logs = [];
		cards = {};
		filter = "";
		PAGE.index = 0;
		carsDiv.innerHTML = "";
		logBox.textContent = "";
		pagerDiv.innerHTML = "";
		prevBtn.disabled = nextBtn.disabled = true;
	}

	// --------------------  EVENTS UI  --------------------
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
	resetBtn.onclick = async () => {
		fullBtn.disabled = stepBtn.disabled = true;
		await api.resetRace();
		ws && ws.close();
		await clearState();
		fullBtn.disabled = stepBtn.disabled = false;
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

	// --------------------  Modal règles  -----------------
	const rulesModal = document.getElementById("rulesModal");
	if (rulesModal) { // Page index.html uniquement
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
			const data = await api.getRules();
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
			await api.patchRules(obj);
			hide(rulesModal);
			await api.resetRace();
		};
	}

	// init
	computePageSize();
	renderPage();
}