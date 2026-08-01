document.addEventListener("DOMContentLoaded", function () {
  initNavbarScroll();
  initHeroCanvas();
  initTerminalTyping();
  initChatWidget();
});

/* ---------------------------------------------------------------
   Sticky navbar background swap on scroll
   --------------------------------------------------------------- */
function initNavbarScroll() {
  const nav = document.getElementById("rsNavbar");
  if (!nav) return;
  const toggle = () => {
    if (window.scrollY > 24) {
      nav.classList.add("rs-scrolled");
    } else {
      nav.classList.remove("rs-scrolled");
    }
  };
  toggle();
  window.addEventListener("scroll", toggle, { passive: true });
}

/* ---------------------------------------------------------------
   Hero background: a quiet, drifting network of connected nodes.
   Kept low-contrast and slow so it reads as ambient texture, not
   a distraction. Respects prefers-reduced-motion.
   --------------------------------------------------------------- */
function initHeroCanvas() {
  const canvas = document.getElementById("rsHeroCanvas");
  if (!canvas) return;

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  const ctx = canvas.getContext("2d");
  let width, height, nodes;
  const NODE_COUNT = 46;
  const LINK_DIST = 130;

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    width = canvas.width = rect.width;
    height = canvas.height = rect.height;
  }

  function makeNodes() {
    nodes = Array.from({ length: NODE_COUNT }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.18,
      vy: (Math.random() - 0.5) * 0.18,
    }));
  }

  function step() {
    ctx.clearRect(0, 0, width, height);

    for (const n of nodes) {
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < 0 || n.x > width) n.vx *= -1;
      if (n.y < 0 || n.y > height) n.vy *= -1;
    }

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i], b = nodes[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < LINK_DIST) {
          ctx.strokeStyle = `rgba(94, 234, 212, ${0.14 * (1 - dist / LINK_DIST)})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    for (const n of nodes) {
      ctx.fillStyle = "rgba(91, 141, 255, 0.55)";
      ctx.beginPath();
      ctx.arc(n.x, n.y, 1.6, 0, Math.PI * 2);
      ctx.fill();
    }

    if (!prefersReducedMotion) {
      requestAnimationFrame(step);
    }
  }

  resize();
  makeNodes();
  step();

  window.addEventListener(
    "resize",
    () => {
      resize();
      makeNodes();
      if (prefersReducedMotion) step();
    },
    { passive: true }
  );
}

/* ---------------------------------------------------------------
   Hero terminal: types out a short build sequence, then loops.
   Purely decorative copy — reflects the real process, no fake
   claims about specific timings.
   --------------------------------------------------------------- */
function initTerminalTyping() {
  const output = document.getElementById("rsTerminalOutput");
  if (!output) return;

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  const lines = [
    "$ ransomsyntax init project",
    "> analyzing requirements...      done",
    "> designing architecture...      done",
    "> writing clean, tested code...  done",
    "> running security review...     done",
    "> shipping to production...      ✓",
    "",
    "Ready when you are.",
  ];

  if (prefersReducedMotion) {
    output.textContent = lines.join("\n");
    return;
  }

  let lineIndex = 0;
  let charIndex = 0;
  let displayed = "";

  function typeNext() {
    if (lineIndex >= lines.length) {
      setTimeout(() => {
        displayed = "";
        lineIndex = 0;
        charIndex = 0;
        output.textContent = "";
        typeNext();
      }, 2600);
      return;
    }

    const currentLine = lines[lineIndex];
    if (charIndex <= currentLine.length) {
      output.textContent = displayed + currentLine.slice(0, charIndex);
      charIndex++;
      setTimeout(typeNext, 18 + Math.random() * 22);
    } else {
      displayed += currentLine + "\n";
      lineIndex++;
      charIndex = 0;
      setTimeout(typeNext, 220);
    }
  }

  typeNext();
}

/* ---------------------------------------------------------------
   AI help chat widget. Placeholder logic only — see
   website/views.py::chat_reply for where a real AI backend can be
   wired in later.
   --------------------------------------------------------------- */
function initChatWidget() {
  const root = document.getElementById("rsChat");
  const toggleBtn = document.getElementById("rsChatToggle");
  const body = document.getElementById("rsChatBody");
  const form = document.getElementById("rsChatForm");
  const input = document.getElementById("rsChatInput");
  const chips = document.getElementById("rsChatQuickReplies");
  if (!root || !toggleBtn || !form) return;

  toggleBtn.addEventListener("click", () => {
    const isOpen = root.classList.toggle("rs-chat-open");
    toggleBtn.setAttribute("aria-expanded", String(isOpen));
    if (isOpen) input.focus();
  });

  function appendMessage(text, from) {
    const msg = document.createElement("div");
    msg.className = `rs-chat-msg rs-chat-msg-${from}`;
    msg.textContent = text;
    body.appendChild(msg);
    body.scrollTop = body.scrollHeight;
  }

  function getCookie(name) {
    const match = document.cookie.match(
      new RegExp("(^| )" + name + "=([^;]+)")
    );
    return match ? decodeURIComponent(match[2]) : null;
  }

  async function sendMessage(text) {
    appendMessage(text, "user");
    if (chips) chips.remove();

    try {
      const response = await fetch("/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
        body: JSON.stringify({ message: text }),
      });
      const data = await response.json();
      appendMessage(
        data.reply || "Thanks — our team will follow up by email shortly.",
        "bot"
      );
    } catch (err) {
      appendMessage(
        "Sorry, something went wrong. Please email us directly or use the enquiry form.",
        "bot"
      );
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendMessage(text);
  });

  if (chips) {
    chips.addEventListener("click", (e) => {
      const chip = e.target.closest(".rs-chat-chip");
      if (!chip) return;
      sendMessage(chip.dataset.msg);
    });
  }
}
