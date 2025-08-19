async function postJSON(url = "", data = {}){
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(data)
  });
  if(!res.ok){ throw new Error("Network error"); }
  return await res.json();
}

function pct(x){ return Math.round(x * 100); }

function setProbBars(probs){
  const rock = document.getElementById("p-rock");
  const paper = document.getElementById("p-paper");
  const scissors = document.getElementById("p-scissors");
  rock.style.width = `${pct(probs.rock ?? 1/3)}%`;
  paper.style.width = `${pct(probs.paper ?? 1/3)}%`;
  scissors.style.width = `${pct(probs.scissors ?? 1/3)}%`;
}

function setScoreboard(stats){
  const el = document.getElementById("scoreboard");
  el.textContent = `AI: ${stats.wins} • You: ${stats.losses} • Ties: ${stats.ties}`;
}

async function playMove(move){
  try{
    const data = await postJSON("/play", { move });
    document.getElementById("result").textContent =
      `You: ${data.user} | AI: ${data.ai} → ${data.result}`;
    setScoreboard(data.stats);
    setProbBars(data.probs);
    document.getElementById("pred").textContent = `Prediction: ${data.predicted_user_move}`;
  }catch(e){
    document.getElementById("result").textContent = "Error contacting server. Is it running?";
  }
}

async function resetMemory(){
  try{
    const data = await postJSON("/reset", {});
    document.getElementById("result").textContent = data.message;
    setScoreboard({wins:0,losses:0,ties:0});
    setProbBars({rock:1/3,paper:1/3,scissors:1/3});
    document.getElementById("pred").textContent = "Prediction: —";
  }catch(e){
    document.getElementById("result").textContent = "Couldn't reset.";
  }
}

window.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".move").forEach(btn => {
    btn.addEventListener("click", () => playMove(btn.dataset.move));
  });
  document.getElementById("reset").addEventListener("click", resetMemory);
});
