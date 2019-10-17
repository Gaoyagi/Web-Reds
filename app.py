#A web version of the game reds 
from flask import Flask, render_template, request, redirect, url_for, session
import requests


app = Flask(__name__)

hand = []                   #holds the content of players hand
emptyDiscard = True         #bool to chekc if the discard pile is empty or not

#route for home page
@app.route('/')
def index():
    return render_template('index.html')

#route for the rules of reds
@app.route('/rules')    
def rules():
    return render_template('rules.html')

#route for starting the game
#creates shuffled deck and deals each player 4 cards
@app.route('/game/start')
def gameStart():
    #shuffles new deck and draws a hand for the player
    deckHand = requests.get("https://deckofcardsapi.com/api/deck/new/draw/?count=4")
    deckHand = deckHand.json()
    #adds the drawn cards to the hand list
    for card in deckHand["cards"]:
        hand.append(card)
        requests.get("https://deckofcardsapi.com/api/deck/{}/pile/hand/add/?cards={}".format(deckHand["deck_id"], card["code"]))
    return render_template('start.html', deck=deckHand, hands=hand)

@app.route('/game/<deckID>/<cardsLeft>/<empty')
def game(deckID, cardsLeft, emptyDiscard):
    return render_template('game.html', deckID=deckID, cardsLeft=cardsLeft, emptyDiscard=emptyDiscard)

@app.route('/game/draw/<deckID>/<cardsLeft>')
def draw(deckID, cardsLeft):
    card = requests.get(f"https://deckofcardsapi.com/api/deck/{deckID}/draw/?count=1")
    card = card.json()
    return render_template('draw.html', deckID=deckID, card=card["cards"], cardsLeft=card['remaining'])    

@app.route('/game/discard/<deckID>/<cardsLeft>/<cardValue>')
def discard(deckID, cardsLeft, cardValue):
    emptyDiscard = False
    requests.get(f"https://deckofcardsapi.com/api/deck/{deckID}/pile/discard/add/?cards={cardValue}")
    return redirect(url_for('game', deckID=deckID, cardsLeft=cardsLeft, emptyDiscard=emptyDiscard))

# @app.route('/game/exchange/<cardValue>/<cardNum>')
# def exchange():




#@app.route('/game/declare')
#def declare():

#going to need at least 3 more additional routes, one for drawing a card, one for shuffling, and one for end screen stuff?



if __name__ == '__main__':
    app.run(debug=True)