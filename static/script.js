const grid = document.getElementById("cardGrid");
const worldFilter = document.getElementById("worldFilter");
const schoolFilter = document.getElementById("schoolFilter");
const tagFilter = document.getElementById("tagFilter");
const resetBtn = document.getElementById("resetBtn");
const resultCount = document.getElementById("resultCount");

const modal = document.getElementById("modal");
const closeModal = document.getElementById("closeModal");

// Small helper: build an element and set its text safely
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

async function loadSchools() {
  const res = await fetch("/api/schools");
  const schools = await res.json();
  schools.forEach(function (s) {
    const option = el("option", "", s.name);
    option.value = s.name;
    schoolFilter.appendChild(option);
  });
}

async function loadFigures() {
  const params = new URLSearchParams();
  if (worldFilter.value) params.append("world", worldFilter.value);
  if (schoolFilter.value) params.append("school", schoolFilter.value);
  if (tagFilter.value.trim()) params.append("tag", tagFilter.value.trim().toLowerCase());

  const res = await fetch("/api/figures?" + params.toString());
  const figures = await res.json();

  grid.innerHTML = "";
  resultCount.textContent = figures.length + " figure(s) found";

  figures.forEach(function (fig) {
    const card = el("div", "card");
    card.appendChild(el("h3", "", fig.name));
    card.appendChild(el("p", "meta", fig.world + " · " + fig.school));
    card.appendChild(el("p", "lesson", fig.life_lesson));

    const tagBox = el("div", "tags");
    fig.tags.forEach(function (t) {
      tagBox.appendChild(el("span", "tag", t));
    });
    card.appendChild(tagBox);

    card.addEventListener("click", function () {
      openFigure(fig.id);
    });
    grid.appendChild(card);
  });
}

async function openFigure(id) {
  const res = await fetch("/api/figures/" + id);
  const fig = await res.json();

  document.getElementById("modalName").textContent = fig.name;
  document.getElementById("modalMeta").textContent = fig.world + " · " + fig.school;
  document.getElementById("modalIdea").textContent = fig.core_idea;
  document.getElementById("modalLesson").textContent = fig.life_lesson;
  document.getElementById("modalComment").textContent = fig.thorfinn_comment;

  const tagBox = document.getElementById("modalTags");
  tagBox.innerHTML = "";
  fig.tags.forEach(function (t) {
    tagBox.appendChild(el("span", "tag", t));
  });

  modal.classList.remove("hidden");
}

closeModal.addEventListener("click", function () {
  modal.classList.add("hidden");
});

modal.addEventListener("click", function (e) {
  if (e.target === modal) modal.classList.add("hidden");
});

worldFilter.addEventListener("change", loadFigures);
schoolFilter.addEventListener("change", loadFigures);
tagFilter.addEventListener("input", loadFigures);

resetBtn.addEventListener("click", function () {
  worldFilter.value = "";
  schoolFilter.value = "";
  tagFilter.value = "";
  loadFigures();
});

loadSchools();
loadFigures();