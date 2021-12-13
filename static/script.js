"use strict";

let score = 0;

//Set countdown timer to endgame
let time = 60;
$("#timer").html(time + " sec");

//create a Set where correct words from the board are stored
let words = new Set();

$(".submit-word").on("submit", handleSubmit);

async function handleSubmit(e) {
  e.preventDefault();
  //variable for the word submitted through the form
  let word = $(".word").val();
  //do nothing if form was submitted with no text
  if (!word) return;
  //if submitted word is already in our Set of words, reset form and do nothing else
  if (words.has(word)) {
    $(".submit-word").trigger("reset");
    return;
  }

  //Send the word from the form to the "server" to have it check if it is an appropriate response. **Why is this a get instead of post if we are sending data?**
  const res = await axios.get("/check-word", { params: { word: word } });

  //this is just equivalent to the request above
  // const res = await axios.get(`/check-word?word=${word}`);

  //set the response from the server to a variable
  let response = res.data.result;
  console.log(response);

  //reset form
  $(".submit-word").trigger("reset");

  //Display the server's response in the DOM
  $("#response").html(response);

  //If the server determined this was an appropriate response, add the word to the words Set, update the score value and update the score displayed in the DOM.
  if (response === "ok") {
    words.add(word);
    score += word.length;
    $("#score").html(`Score: ${score}`);
  }
}

let countDown = setInterval(function () {
  //Every second, decrease time by one and update time displayed in the DOM
  time--;
  $("#timer").html(time + " sec");
  //run this function that only continues to run if time is up.
  stopTimer();
}, 1000);

async function stopTimer() {
  //if time has run out, stop the countdown and run endGame function.
  if (time < 1) {
    clearInterval(countDown);
    await endGame();
  }
}

async function endGame() {
  //Replace timer with the text "GAME OVER"
  $(".submit-word").hide();
  $("#boggle").append($("<span>").html("GAME OVER"));
  //update the server by telling it we have completed another game, and update the high score (if necessary) **This one is post, but the other one is get. How come?**
  const res = await axios.post("/end-game", { score: score });
  //this is just because I wanted to see what this response looks like
  console.log(res);
}
