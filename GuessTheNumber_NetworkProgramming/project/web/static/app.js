let socket = null;
let myName = null;

const connectForm = document.getElementById("connectForm");
const guessForm = document.getElementById("guessForm");
const nameInput = document.getElementById("nameInput");
const serverIpInput = document.getElementById("serverIpInput");
const connectBtn = document.getElementById("connectBtn");
const statusMessage = document.getElementById("statusMessage");
const guessInput = document.getElementById("guessInput");
const guessBtn = document.getElementById("guessBtn");
const attemptsSpan = document.getElementById("attemptsSpan");
const timeSpan = document.getElementById("timeSpan");
const winnerBanner = document.getElementById("winnerBanner");
const historyList = document.getElementById("historyList");

// Scoreboard
const scoreboardActive = document.getElementById("scoreboardActive");
const scoreboardGlobal = document.getElementById("scoreboardGlobal");

// Admin Butonu
const resetLbBtn = document.getElementById("resetLbBtn");

// Admin Butonuna Tıklama Olayı
resetLbBtn.addEventListener("click", () => {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    alert("Önce sunucuya bağlanmalısın!");
    return;
  }

  // Şifre Sor
  const password = prompt("Lütfen Admin Şifresini Girin (3 haneli):");
  if (password) {
    // Sunucuya özel mesaj yolla
    socket.send(
      JSON.stringify({
        type: "reset_leaderboard",
        key: password,
      })
    );
  }
});

function setStatus(text) {
  statusMessage.textContent = text;
}

function updateScoreboards(activeList, globalList) {
  // Aktif Liste
  scoreboardActive.innerHTML = "";
  if (!activeList || activeList.length === 0) {
    scoreboardActive.innerHTML =
      '<div style="color:#64748b; padding:5px;">Kimse yok</div>';
  } else {
    activeList.forEach((s) => {
      const row = document.createElement("div");
      row.className = "score-row";
      if (myName && s.name === myName) row.classList.add("me");
      row.innerHTML = `<span>${s.name}</span><span><strong>${s.total}</strong> p</span>`;
      scoreboardActive.appendChild(row);
    });
  }

  // Global Liste
  scoreboardGlobal.innerHTML = "";
  if (!globalList || globalList.length === 0) {
    scoreboardGlobal.innerHTML =
      '<div style="color:#64748b; padding:5px;">Liste boş</div>';
  } else {
    globalList.forEach((s, index) => {
      const row = document.createElement("div");
      row.className = "score-row";
      let rank = `#${index + 1}`;
      if (index === 0) rank = "🥇";
      if (index === 1) rank = "🥈";
      if (index === 2) rank = "🥉";

      row.innerHTML = `
        <span style="display:flex; gap:8px;">
            <span>${rank}</span> <span>${s.name}</span>
        </span>
        <span><strong>${s.total}</strong></span>
      `;
      scoreboardGlobal.appendChild(row);
    });
  }
}

function connectWebSocket(name, ip) {
  if (socket) socket.close();
  const host = ip || window.location.hostname || "localhost";
  socket = new WebSocket(`ws://${host}:8765`);

  setStatus("Bağlanıyor...");

  socket.onopen = () => {
    socket.send(JSON.stringify({ type: "join", name: name }));
    myName = name;
    setStatus("Bağlandı.");
    connectBtn.disabled = true;
    guessInput.disabled = false;
    guessBtn.disabled = false;
  };

  socket.onmessage = (e) => {
    const msg = JSON.parse(e.data);

    if (msg.type === "welcome") {
      setStatus(msg.msg);

      // EĞER SERVER admin sensin DEDİYSE BUTONU AÇ
      if (msg.is_admin === true) {
        resetLbBtn.style.display = "block";
      } else {
        resetLbBtn.style.display = "none";
      }
    } else if (msg.type === "scores") {
      updateScoreboards(msg.active, msg.global);
    } else if (msg.type === "result") {
      const li = document.createElement("li");
      li.className = "history-item";
      li.innerHTML = `
            <span>${msg.guess}</span>
            <span>+${msg.plus} -${msg.minus} (${msg.gained}p)</span>
        `;
      historyList.prepend(li);
      attemptsSpan.textContent = msg.remaining;
      timeSpan.textContent = msg.time + "s";
    } else if (msg.type === "winner") {
      winnerBanner.style.display = "block";
      winnerBanner.innerHTML = `KAZANAN: <strong>${msg.winner}</strong> (Sayı: ${msg.secret})`;
    } else if (msg.type === "newround") {
      winnerBanner.style.display = "none";
      historyList.innerHTML = "";
      attemptsSpan.textContent = "-";
      timeSpan.textContent = "-";
    } else if (msg.type === "error") {
      alert("HATA: " + msg.msg);
    } else if (msg.type === "info") {
      alert("BİLGİ: " + msg.msg);
    }
  };

  socket.onclose = () => {
    setStatus("Bağlantı koptu.");
    connectBtn.disabled = false;
    guessInput.disabled = true;
    guessBtn.disabled = true;
  };
}

connectForm.addEventListener("submit", (e) => {
  e.preventDefault();
  connectWebSocket(nameInput.value, serverIpInput.value);
});

guessForm.addEventListener("submit", (e) => {
  e.preventDefault();
  if (socket) {
    socket.send(JSON.stringify({ type: "guess", guess: guessInput.value }));
    guessInput.value = "";
  }
});
