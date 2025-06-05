const DIST_MAX = 100;

function renderCar(card, data) {
  card.querySelector(".km").textContent = `${data.kmTraveled} km`;
  card.querySelector(".essence").textContent = `${data.tankCapacity} L`;
  card.querySelector(".rank").textContent = `#${data.rank}`;

  const percent = Math.min(100, (data.kmTraveled / DIST_MAX) * 100);
  card.querySelector(".progress").style.width = percent + "%";

  card.classList.toggle("opacity-50", !data.wheelOk || data.tankCapacity === 0);
}

function createCard(data) {
  const div = document.createElement("div");
  div.className = "bg-white rounded-2xl shadow p-4 space-y-2";
  div.innerHTML = `
    <h2 class="text-xl font-semibold capitalize">${data.color}</h2>
    <div class="h-2 bg-gray-200 rounded">
      <div class="progress h-full bg-${data.color}-500 rounded"></div>
    </div>
    <div class="text-sm"><span class="km"></span> | <span class="essence"></span></div>
    <div class="text-sm text-gray-500 rank"></div>
  `;
  renderCar(div, data);
  return div;
}

const container = document.getElementById("cars");
let cards = {};

const ws = new WebSocket(`ws://${location.host}/ws/race`);
ws.onmessage = (event) => {
  const cars = JSON.parse(event.data)

  cars.sort((a, b) => a.rank - b.rank)

  container.innerHTML = ""
  cars.forEach(car => {
    const card = cards[car.id] ?? createCard(car)
    renderCar(card, car)
    container.appendChild(card)
    cards[car.id] = card
  })
};

ws.onclose = () => {
  console.log("WebSocket fermé");
};
