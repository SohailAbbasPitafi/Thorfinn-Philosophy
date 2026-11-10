const lines = [
  "I once lived only for revenge. When it ended, I had nothing.",
  "So I started listening to others who asked what a life is for.",
  "Here you will find thinkers from Greece, from the modern world, and from stories I know.",
  "Open any card. I will tell you what I think of them."
];

const bubble = document.getElementById("mascot-bubble");
const text = document.getElementById("mascot-text");
const nextBtn = document.getElementById("mascot-next");
const skipBtn = document.getElementById("mascot-skip");
const avatar = document.getElementById("mascot-avatar");
let i = 0;

function show() {
  text.textContent = lines[i];
  nextBtn.textContent = i === lines.length - 1 ? "Begin" : "Next";
  bubble.classList.remove("hidden");
}

function close() {
  bubble.classList.add("hidden");
  localStorage.setItem("thorfinnSeen", "yes");
}

nextBtn.addEventListener("click", () => {
  i++;
  if (i < lines.length) show();
  else close();
});

skipBtn.addEventListener("click", close);

avatar.addEventListener("click", () => {
  i = 0;
  show();
});

if (!localStorage.getItem("thorfinnSeen")) show();