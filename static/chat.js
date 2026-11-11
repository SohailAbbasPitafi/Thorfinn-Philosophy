(function () {
  const log = document.getElementById("chat-log");
  const nextBtn = document.getElementById("chat-next");
  const replayBtn = document.getElementById("chat-replay");
  const counter = document.getElementById("chat-count");
  if (!log || !nextBtn) return;

  const messages = Array.from(log.querySelectorAll(".msg"));
  let shown = 0;
  let busy = false;

  function updateCounter() {
    counter.textContent = shown + " / " + messages.length;
  }

  function reveal(index) {
    messages[index].classList.remove("msg-hidden");
    messages[index].scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function showNext() {
    if (busy || shown >= messages.length) return;
    busy = true;

    // "typing..." dots on the correct side, then the real message
    const upcoming = messages[shown];
    const typing = document.createElement("div");
    typing.className = "msg typing " +
      (upcoming.classList.contains("from-thorfinn") ? "from-thorfinn" : "from-figure");
    for (let i = 0; i < 3; i++) typing.appendChild(document.createElement("span"));
    log.insertBefore(typing, upcoming);

    setTimeout(function () {
      typing.remove();
      reveal(shown);
      shown++;
      updateCounter();
      busy = false;
      if (shown >= messages.length) {
        nextBtn.hidden = true;
        replayBtn.hidden = false;
      }
    }, 650);
  }

  function restart() {
    messages.forEach(function (m) { m.classList.add("msg-hidden"); });
    shown = 0;
    replayBtn.hidden = true;
    nextBtn.hidden = false;
    reveal(0);
    shown = 1;
    updateCounter();
  }

  nextBtn.addEventListener("click", showNext);
  replayBtn.addEventListener("click", restart);

  // first line appears straight away
  reveal(0);
  shown = 1;
  updateCounter();
})();