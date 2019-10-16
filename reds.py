#A web version of the game reds 
from flask import Flask, render_template, request, redirect, url_for, session
#

app = Flask(__name__)

#route for home page
@app.route('/')
def index():
    return render_template('index.html')

# #route for the rules of reds
# @app.route('/rules')
# def rules():
#     return render_template('rules.html')

# #route for starting the game
# #creates shuffled deck and deals each player 4 cards
# @app.route('/game/start/<playerCount>')
# def gameStart(playerCount):
#     deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
#     shuffled = deck.json()  
#     players = list(playerCount)
#     cards = requests.get("https://deckofcardsapi.com/api/deck/<<deck_id>>/draw/?count=4")
#     hand = cards.json()
#     players.append(hand)
#     return redirect(url_for('game', variable=shuffled["deck_id"]), variable=players)

# #route for displaying the main game
# @app.route('/game/<deck_id>/<player_list>')
# def game(deckID, playerList):
#     return render_template('game.html', deckID=deckID, players = playerList)

# #route to display the drawn card

# #route to display results

# #