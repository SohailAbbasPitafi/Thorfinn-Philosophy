(function () {
  const input = document.getElementById("situationText");
  const btn = document.getElementById("situationBtn");
  const result = document.getElementById("situationResult");
  const reply = document.getElementById("situationReply");
  const cards = document.getElementById("situationCards");
  if (!input || !btn) return;

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  async function ask() {
    const text = input.value.trim();
    btn.disabled = true;
    btn.textContent = "Thorfinn is thinking...";

    try {
      const res = await fetch("/api/match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
      });
      const data = await res.json();

      reply.textContent = data.reply || "I could not find the words. Try again.";
      cards.innerHTML = "";

      (data.matches || []).forEach(function (m) {
        const link = el("a", "match-card");
        link.href = "/figure/" + m.id;
        link.style.setProperty("--card-accent", m.highlight);
        link.appendChild(el("h3", "", m.name));
        link.appendChild(el("p", "meta", m.world + " · " + m.school));
        link.appendChild(el("p", "", m.life_lesson));
        cards.appendChild(link);
      });

      result.hidden = false;
    } catch (err) {
      reply.textContent = "Something went wrong. Please try again.";
      result.hidden = false;
    }

    btn.disabled = false;
    btn.textContent = "Ask Thorfinn";
  }

  btn.addEventListener("click", ask);
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) ask();
  });
})();