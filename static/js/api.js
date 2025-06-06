// -----------------------------------------------------------------------------
//  api.js – Couche d'accès réseau (REST + WebSocket)
// -----------------------------------------------------------------------------

const JSON_HEADER = {"Content-Type": "application/json"};
const WS_URL = `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/race`;

// ------------------------------- Voitures ------------------------------------
export async function listCars() {
  return fetch("/cars").then(r => r.json());
}
export async function createCar(car) {
  return fetch("/cars", {
    method: "POST",
    headers: JSON_HEADER,
    body: JSON.stringify(car)
  }).then(r => r.json());
}
export async function updateCar(id, car) {
  return fetch(`/cars/${id}`, {
    method: "PUT",
    headers: JSON_HEADER,
    body: JSON.stringify(car)
  }).then(r => r.json());
}
export async function deleteCar(id) {
  return fetch(`/cars/${id}`, {method: "DELETE"});
}

// ------------------------------- Course --------------------------------------
export async function resetRace() {
  return fetch("/reset", {method: "POST"}).then(r => r.json());
}
export async function stepRace() {
  return fetch("/step", {method: "POST"}).then(r => r.json());
}
export function raceSocket(onMessage) {
  const ws = new WebSocket(WS_URL);
  ws.onmessage = ({data}) => onMessage(JSON.parse(data));
  return ws;
}

// ------------------------------- Règles --------------------------------------
export async function getRules() {
  return fetch("/rules").then(r => r.json());
}
export async function patchRules(partial) {
  return fetch("/rules", {
    method: "PATCH",
    headers: JSON_HEADER,
    body: JSON.stringify(partial)
  }).then(r => r.json());
}