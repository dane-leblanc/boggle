from flask import Flask, render_template, request, redirect, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret'

boggle_game = Boggle()

@app.route('/')
def show_homepage():
    """ make the board, reset the board in session to match the current board. Get high score and number of plays from session (report as zero if they're not in session). Render gameboard in DOM.  """
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)
    
    return render_template('index.html', board=board, highscore=highscore, numplays=numplays)

@app.route('/check-word')
def check_word():
    """ get the word from the form and check it against the current board (stored in our session)
    """
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})
    
@app.route("/end-game", methods=["POST"])
def end_game():
    #get the axios post (score) from endgame function
    score = request.json["score"]
    #get high score and number of times played from session
    #if they are not in the session, set that value to zero
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)
    #update session data
    session["numplays"] = numplays + 1
    session["highscore"] = max(score, highscore)
    #apparently we have to return something or there will be a 500 error, which is bad?
    return jsonify({})
