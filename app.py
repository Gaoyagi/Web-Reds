#A web version of the game reds 
from flask import Flask, render_template, request, redirect, url_for, session
import requests


app = Flask(__name__)

hand = []                   #holds the content of players hand
emptyDiscard = True         #bool to chekc if the discard pile is empty or not

#variable names that you will seen get passed around:
    #deckID: contains the ID for the current deck, needed to draw and shuffle for the deck
    #cardsLeft: counter number of cards currently left in the deck so I cna display it below the dekc image
    #emptyDiscard: checks if the the disscard pile is empty, used to determine what image to show for the discard pile in game.html
    #hand list: used so I can keep easily keep track of what cards the player has so i dont have to keep requesting and converting a response object
        #hand[0] and hand[1] represent the 2 top cards and hand[2] and hand[3] represent the 2 bottom cards that are shown the player at the beginning

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
        #creates/adds cards to a new "hand" pile
        requests.get("https://deckofcardsapi.com/api/deck/{}/pile/hand/add/?cards={}".format(deckHand["deck_id"], card["code"]))
    return render_template('start.html', deck=deckHand, hands=hand)

#route to display general game board
@app.route('/game/<deckID>/<cardsLeft>')
def game(deckID, cardsLeft):
    return render_template('game.html', deckID=deckID, cardsLeft=cardsLeft)

#route to show game board with a drawn card
@app.route('/game/draw/<deckID>/<cardsLeft>')
def draw(deckID, cardsLeft):
    #draws a card from the deck and 
    card = requests.get("https://deckofcardsapi.com/api/deck/{}/draw/?count=1".format(deckID))
    card = card.json()      #converts response object to json dictionary so I can parse through it
    return render_template('draw.html', deckID=deckID, card=card['cards'], cardsLeft=card['remaining'])    

#route to deal with if player discards drawn card
@app.route('/game/discard/<deckID>/<cardsLeft>/<cardCode>')
def discard(deckID, cardsLeft, cardCode):
    emptyDiscard = False
    #creates/adds cards to a discard pile
    requests.get(f"https://deckofcardsapi.com/api/deck/{deckID}/pile/discard/add/?cards={cardCode}")
    return redirect(url_for('game', deckID=deckID, cardsLeft=cardsLeft))

@app.route('/game/exchange/<deckID>/<cardsLeft>/<card>/<position>')
def exchange(deckID, cardsLeft, card, position):
    emptyDiscard = False
    changed = hand[position]
    requests.get(f"https://deckofcardsapi.com/api/deck/{deckID}/pile/discard/add/?cards={changed['code']}")
    hand[position] = card
    return redirect(url_for('game', deckID=deckID, cardsLeft=cardsLeft))


#@app.route('/game/declare')
#def declare():

#going to need at least 3 more additional routes, one for drawing a card, one for shuffling, and one for end screen stuff?



if __name__ == '__main__':
    app.run(debug=True)