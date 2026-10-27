const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector(".site-nav");
const digitalClock = document.querySelector(".digital-clock");
const clockDigits = [...document.querySelectorAll(".clock-digit")];
const visitCounter = document.querySelector(".visit-counter");
const visitCounterBadge = document.querySelector(".visit-counter-badge");
const visitCounterStatus = document.querySelector("#visit-counter-status");
const digitSegments = [
  "abcdef",
  "bc",
  "abged",
  "abgcd",
  "fgbc",
  "afgcd",
  "afgecd",
  "abc",
  "abcdefg",
  "abcdfg",
];

menuToggle.addEventListener("click", () => {
  const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";
  menuToggle.setAttribute("aria-expanded", String(!isExpanded));
  menuToggle.setAttribute("aria-label", isExpanded ? "Abrir menú" : "Cerrar menú");
  siteNav.classList.toggle("is-open", !isExpanded);
});

siteNav.addEventListener("click", (event) => {
  if (event.target instanceof HTMLAnchorElement) {
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Abrir menú");
    siteNav.classList.remove("is-open");
  }
});

document.querySelector("#year").textContent = new Date().getFullYear();

function updateDigitalClock() {
  const now = new Date();
  const time = `${String(now.getHours()).padStart(2, "0")}${String(now.getMinutes()).padStart(2, "0")}`;

  clockDigits.forEach((digit, index) => {
    const litSegments = digitSegments[Number(time[index])];
    digit.dataset.value = time[index];
    digit.querySelectorAll(".segment").forEach((segment) => {
      segment.classList.toggle("is-on", litSegments.includes(segment.classList[1].slice(-1)));
    });
  });
  digitalClock.setAttribute(
    "aria-label",
    `Reloj digital, ${now.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" })}`,
  );
}

updateDigitalClock();
setInterval(updateDigitalClock, 1000);

function showVisitCounterError() {
  visitCounter.dataset.state = "error";
  visitCounterBadge.hidden = true;
  visitCounterStatus.textContent = "No se pudo cargar el contador global.";
  visitCounterStatus.hidden = false;
}

if (visitCounterBadge.complete) {
  if (visitCounterBadge.naturalWidth === 0) {
    showVisitCounterError();
  } else {
    visitCounter.dataset.state = "ready";
  }
} else {
  visitCounterBadge.addEventListener("load", () => {
    visitCounter.dataset.state = "ready";
  });
  visitCounterBadge.addEventListener("error", showVisitCounterError);
}