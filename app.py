#A web version of the game reds 
from flask import Flask, render_template, request, redirect, url_for, session
import requests


app = Flask(__name__)

hand = []                   #holds the content of players hand
values = {
    '2S':[2,"2 of Spades"],
    '2C':[2,"2 of Clubs"],
    '2H':[2,"2 of Hearts"],
    '2D':[2,"2 of Diamonds"],
    '3S':[3,"3 of Spades"],
    '3C':[3,"3 of Clubs"],
    '3H':[3,"3 of Hearts"],
    '3D':[3,"3 of Diamonds"],
    '4S':[4,"4 of Spades"],
    '4C':[4,"4 of Clubs"],
    '4H':[4,"4 of Hearts"],
    '4D':[4,"4 of Diamonds"],
    '5S':[5,"5 of Spades"],
    '5C':[5,"5 of Clubs"],
    '5H':[5,"5 of Hearts"],
    '5D':[5,"5 of Diamonds"],
    '6S':[6,"6 of Spades"],
    '6C':[6,"6 of Clubs"],
    '6H':[6,"6 of Hearts"],
    '6D':[6,"6 of Diamonds"],
    '7S':[7,"7 of Spades"],
    '7C':[7,"7 of Clubs"],
    '7H':[7,"7 of Hearts"],
    '7D':[7,"7 of Diamonds"],
    '8S':[8,"8 of Spades"],
    '8C':[8,"8 of Clubs"],
    '8H':[8,"8 of Hearts"],
    '8D':[8,"8 of Diamonds"],
    '9S':[9,"9 of Spades"],
    '9C':[9,"9 of Clubs"],
    '9H':[9,"9 of Hearts"],
    '9D':[9,"9 of Diamonds"],
    '10S':[10,"10 of Spades"],
    '10C':[10,"10 of Clubs"],
    '10H':[10,"10 of Hearts"],
    '10D':[10,"10 of Diamonds"],
    'JS':[10,"Jack of Spades"],
    'JC':[10,"Jack of Clubs"],
    'JH':[10,"Jack of Hearts"],
    'JD':[10,"Jack of Diamonds"],
    'QS':[10,"Queen of Spades"],
    'QC':[10,"Queen of Clubs"],
    'QH':[10,"Queen of Hearts"],
    'QD':[10,"Queen of Diamonds"],
    'KS':[10,"King of Spades"],
    'KC':[10,"King of Clubs"],
    'KH':[-2,"King of Hearts"],
    'KD':[-2,"King of Diamonds"],
    'AS':[1,"Ace of Spades"],
    'AC':[1,"Ace of Clubs"],
    'AH':[1,"Ace of Hearts"],
    'AD':[1,"Ace of Diamonds"]
}

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

@app.route('/game/exchange/<deckID>/<cardsLeft>/<position>/<cardCode>')
def exchange(deckID, cardsLeft, position, cardCode):
    emptyDiscard = False
    position = int(position)
    changed = hand[position]          #gets the card that will be replaced
    requests.get(f"https://deckofcardsapi.com/api/deck/{deckID}/pile/hand/add/?cards={cardCode}")        #adds new card to the hand pile
    requests.get(f"https://deckofcardsapi.com/api/deck/{deckID}/pile/hand/draw/?cards={changed['code']}")       #draws the card to remove from the hand pile
    requests.get(f"https://deckofcardsapi.com/api/deck/{deckID}/pile/discard/add/?cards={changed['code']}")     #adds the removed card to the discard pile
    card = requests.get(f"https://deckofcardsapi.com/api/deck/{deckID}/pile/hand/list/")
    card = card.json()
    card = card['piles']['hand']['cards']
    for item in card:
        if item['code'] == cardCode:
            hand[position] = item
    return redirect(url_for('game', deckID=deckID, cardsLeft=cardsLeft))

@app.route('/game/declare')
def declare():
    final = values[hand[0]['code']][0] + values[hand[1]['code']][0] + values[hand[2]['code']][0] + values[hand[3]['code']][0]
    return render_template("declare.html", hands=hand, values=values, final=final)

#going to need at least 3 more additional routes, one for drawing a card, one for shuffling, and one for end screen stuff?



if __name__ == '__main__':
    app.run(debug=True)