async function loadAll() {
  const logs = await (await fetch("/api/logs")).json();
  const clips = await (await fetch("/api/clips")).json();
  const stats = await (await fetch("/api/stats")).json();

  // Logs
  const tbody = document.querySelector("#logTable tbody");
  tbody.innerHTML = "";
  logs.slice().reverse().forEach(l => {
    tbody.innerHTML += `
      <tr>
        <td>${l.timestamp}</td>
        <td>${l.class}</td>
        <td>${parseFloat(l["confidence(%)"] || l.confidence).toFixed(1)}</td>
        <td><button onclick="play('${l.clip}')">▶</button></td>
      </tr>`;
  });

  // Clips
  const clipBox = document.getElementById("clips");
  clipBox.innerHTML = "";
  clips.forEach(c => {
    const name = c.split("/").pop();
    clipBox.innerHTML += `
      <div>
        <span>${name}</span>
        <span>
          <button onclick="play('${c}')">▶</button>
          <button onclick="delClip('${c}')">🗑️</button>
        </span>
      </div>`;
  });

  // Stats
  const statsBox = document.getElementById("stats");
  statsBox.innerHTML = "";
  Object.entries(stats).forEach(([k, v]) => {
    statsBox.innerHTML += `<div class="stat">${k}: ${v}</div>`;
  });
}

function play(path) {
  const v = document.getElementById("player");
  v.pause();
  v.src = "/clips/" + path;
  v.load();
  v.play();
}

async function delClip(path) {
  if (!confirm("Delete clip?")) return;
  await fetch("/api/delete_clip", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ name: path })
  });
  loadAll();
}

loadAll();
setInterval(loadAll, 5000);
