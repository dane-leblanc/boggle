from flask import Flask, render_template, request, redirect, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret'

boggle_game = Boggle()

@app.route('/')
def show_homepage():
    
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)
    return render_template('index.html', board=board, highscore=highscore, numplays=numplays)

@app.route('/check-word')
def check_word():
    
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})
    
@app.route("/end-game", methods=["POST"])
def end_game():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)
    
    session["numplays"] = numplays + 1
    session["highscore"] = max(score, highscore)
    
    return jsonify(brokeRecord=score > highscore)