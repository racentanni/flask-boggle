class BoggleGame {
    constructor() {
        //initialize game variables
        this.guess = $("#guess");
        this.guessForm = $("#user_guess_form");
        this.guessFeedback = $("#guess_feedback");
        this.score = 0;
        this.time = 60;
        this.bindEvents();
        this.startTimer();
        this.wordsGuessed = new Set();
    }
    //Bind click event to game instance
    bindEvents() {
        this.guessForm.on("submit", (e) => this.handleGuess(e));
    }

    handleGuess(e) {
        e.preventDefault();
        let userGuess = this.guess.val();
        if (this.wordsGuessed.has(userGuess)) {
            this.displayFeedback("You already guessed that word!");
            this.guess.val("");
            return;
        }
        //send guess word to server to validate on backend
        this.validateGuess(userGuess);
        //Clear guess input
        this.guess.val("");
    }

    validateGuess(userGuess) {
        axios
           .post("/validate_guess", {guess: userGuess})
           .then((response) => this.handleServerResponse(response))
           .catch((error) => console.log("Error", error)); 
    }

    handleServerResponse(response) {
        let guessResponse = response.data.result;
        let word = response.data.word;
    
        if (guessResponse === "ok") {
          this.displayFeedback("Word is valid and exists on the board");
          this.updateScore(word);
          this.addWordToSet(word);
        } else if (guessResponse === "not-on-board") {
          this.displayFeedback("Word is not on board");
        } else {
          this.displayFeedback("Not a valid word");
        }
    
        setTimeout(() => {
          return this.clearFeedback();
        }, 1000);
      }
    
      addWordToSet(word) {
        this.wordsGuessed.add(word);
      }
    
      displayFeedback(msg) {
        this.guessFeedback.text(msg);
        console.log(this.guessFeedback.text());
      }
    
      clearFeedback() {
        this.guessFeedback.text("");
        console.log(this.guessFeedback.text());
      }
    
      updateScore(word) {
        let word_points = word.length;
        this.score += word_points;
        $("#game_score").text(this.score);
      }
    
      startTimer() {
        const timer = setInterval(() => {
          this.time -= 1;
          //Update timer
          $("#timer").text(this.time);
          //Once timer reaches 0, clear timer interval and disable form for guess
          if (this.time === 0) {
            clearInterval(timer);
            this.endGame();
          }
        }, 1000);
      }
    
      getGameOverHtml(highScore, gamesPlayed) {
        return `
            <div>
                <h1>Game Over</h1>
                <p>High Score: ${highScore}</p>
                <p>Games Played: ${gamesPlayed}</p>
                <form id="start_form" action="/start" method="post">
                    <input type="submit" class="btn" value="Start">
                </form>
            </div>
        `;
      }
    
      sendFinalScore(score) {
        axios
          .post("/game_over", { gameScore: score })
          .then((response) => {
            // Empty the page
            $("body").empty();
            // Append HTML with the high score and games played
            $("body").append(
              this.getGameOverHtml(response.data.high_score, response.data.games)
            );
          })
          .catch((error) => this.logError("Error:", error));
      }
    
      endGame() {
        this.guessForm.remove();
        this.sendFinalScore(this.score);
      }
    }
    
    $(document).ready(function () {
      new BoggleGame();
});