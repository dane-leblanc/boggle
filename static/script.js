"use strict";

let score = 0;
let time = 10;
$("#timer").html(time + " sec");

$(".submit-word").on("submit", handleSubmit);

async function handleSubmit(e) {
  e.preventDefault();

  if (time === 0) {
    return;
  }
  const $word = $(".word");

  let word = $word.val();
  if (!word) return;

  // const res = await axios.get("/check-word", { params: { word: word } });

  const res = await axios.get(`/check-word?word=${word}`);

  let response = res.data.result;
  console.log(response);
  $(".submit-word").trigger("reset");

  $("#response").html(response);

  if (response === "ok") {
    score += word.length;
    $("#score").html(`Score: ${score}`);
  }
}

let countDown = setInterval(function () {
  time--;
  $("#timer").html(time + " sec");
  stopTimer();
}, 1000);

function stopTimer() {
  if (time < 1) {
    clearInterval(countDown);
  }
}
