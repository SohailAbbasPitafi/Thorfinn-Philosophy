(function () {
  const root = document.getElementById("mascot");
  if (!root) return;

  const lines = JSON.parse(root.dataset.lines || "[]").map(function (l) {
    l = l.trim();
    return /[.!?…"”]$/.test(l) ? l : l + ".";
  });
  const store = root.dataset.store === "session" ? sessionStorage : localStorage;
  const storeKey = "thorfinn-" + (root.dataset.key || "page");

  const bubble = document.getElementById("mascot-bubble");
  const text = document.getElementById("mascot-text");
  const nextBtn = document.getElementById("mascot-next");
  const skipBtn = document.getElementById("mascot-skip");
  const avatar = document.getElementById("mascot-avatar");

  let i = 0;
  let timer = null;
  let typing = false;

  function type(msg) {
    clearInterval(timer);
    text.textContent = "";
    typing = true;
    let n = 0;
    timer = setInterval(function () {
      text.textContent += msg.charAt(n);
      n++;
      if (n >= msg.length) {
        clearInterval(timer);
        typing = false;
      }
    }, 22);
  }

  function show() {
    nextBtn.textContent = i === lines.length - 1 ? "Begin" : "Next";
    bubble.classList.remove("hidden");
    type(lines[i]);
  }

  function close() {
    clearInterval(timer);
    typing = false;
    bubble.classList.add("hidden");
    store.setItem(storeKey, "yes");
  }

  nextBtn.addEventListener("click", function () {
    if (typing) {
      clearInterval(timer);
      text.textContent = lines[i];
      typing = false;
      return;
    }
    i++;
    if (i < lines.length) show();
    else close();
  });

  skipBtn.addEventListener("click", close);

  avatar.addEventListener("click", function () {
    i = 0;
    show();
  });

  if (lines.length && !store.getItem(storeKey)) show();
})();