"use strict";

const COLOR_CLASS = {
	slate: "bg-slate-500", gray: "bg-gray-500", zinc: "bg-zinc-500",
	red: "bg-red-500", orange: "bg-orange-500", amber: "bg-amber-500", yellow: "bg-yellow-500",
	green: "bg-green-500", teal: "bg-teal-500", cyan: "bg-cyan-500", blue: "bg-blue-500",
	indigo: "bg-indigo-500", violet: "bg-violet-500", purple: "bg-purple-500", pink: "bg-pink-500"
};
const COLOR_KEYS = Object.keys(COLOR_CLASS);

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

function fillColorSelect(selected = null) {
	const used = new Set(carsCache.map(c => c.color));
	fColor.innerHTML = "";
	COLOR_KEYS.forEach(col => {
		if (!used.has(col) || col === selected) {
			const opt = document.createElement("option");
			opt.value = col;
			opt.textContent = col;
			fColor.appendChild(opt);
		}
	});
	if (selected) {
		fColor.value = selected;
	}
}

function clearForm() {
	fId.value = "";
	fPilot.value = "";
	fTank.value = "";
	fillColorSelect();
	btnCreate.classList.remove("hidden");
	btnUpdate.classList.add("hidden");
	btnDelete.classList.add("hidden");
	btnCancel.classList.add("hidden");
}

async function refresh() {
	carsCache = await (await fetch("/cars")).json();
	tbody.innerHTML = "";
	carsCache.forEach(c => {
		const tr = document.createElement("tr");
		tr.className = "cursor-pointer hover:bg-gray-100";
		tr.innerHTML = `
      <td class="border px-2 py-1">${c.id}</td>
      <td class="border px-2 py-1">${c.pilot}</td>
      <td class="border px-2 py-1">${c.color}</td>
      <td class="border px-2 py-1">${c.tank}</td>`;
		tr.onclick = () => selectCar(c);
		tbody.appendChild(tr);
	});
	fillColorSelect();
}

function selectCar(c) {
	fId.value = c.id;
	fPilot.value = c.pilot;
	fTank.value = c.tank;
	fillColorSelect(c.color);
	btnCreate.classList.add("hidden");
	btnUpdate.classList.remove("hidden");
	btnDelete.classList.remove("hidden");
	btnCancel.classList.remove("hidden");
}

btnCreate.onclick = async () => {
	const body = {pilot: fPilot.value, color: fColor.value, tank: +fTank.value};
	await fetch("/cars", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
	clearForm();
	await refresh();
};

btnUpdate.onclick = async () => {
	const id = fId.value;
	const body = {pilot: fPilot.value, color: fColor.value, tank: +fTank.value};
	await fetch(`/cars/${id}`, {
		method: "PUT",
		headers: {"Content-Type": "application/json"},
		body: JSON.stringify(body)
	});
	clearForm();
	await refresh();
};

btnDelete.onclick = async () => {
	const id = fId.value;
	await fetch(`/cars/${id}`, {method: "DELETE"});
	clearForm();
	await refresh();
};

btnCancel.onclick = clearForm;

refresh();
