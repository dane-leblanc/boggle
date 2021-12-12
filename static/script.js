"use strict";

let score = 0;

//Set countdown timer to endgame
let time = 5;
$("#timer").html(time + " sec");

//create a Set where correct words from the board are stored
let words = new Set();

$(".submit-word").on("submit", handleSubmit);

async function handleSubmit(e) {
  e.preventDefault();

  let word = $(".word").val();
  if (!word) return;

  if (words.has(word)) {
    $(".submit-word").trigger("reset");
    return;
  }

  // const res = await axios.get("/check-word", { params: { word: word } });

  const res = await axios.get(`/check-word?word=${word}`);

  let response = res.data.result;
  console.log(response);
  $(".submit-word").trigger("reset");

  $("#response").html(response);

  if (response === "ok") {
    words.add(word);
    score += word.length;
    $("#score").html(`Score: ${score}`);
  }
}

let countDown = setInterval(function () {
  time--;
  $("#timer").html(time + " sec");
  stopTimer();
}, 1000);

async function stopTimer() {
  if (time < 1) {
    clearInterval(countDown);
    await endGame();
  }
}

async function endGame() {
  $(".submit-word").hide();
  $("#boggle").append($("<span>").html("GAME OVER"));
  const res = await axios.post("/end-game", { score: score });
  console.log(res);
}
