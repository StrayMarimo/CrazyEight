# CrazyEights
A version of the Crazy Eights card game made with Python 3 and PyGame. Crazy Eights is a fun and simple card game that can be played with a standard 52 card deck.

## How to Play
Typically two to four people play Crazy Eights. If there are two players, each player gets 7 cards. If there are more, each player gets 5 cards.

The goal of the game is to discard all the cards in your hand.

During a turn, the player can play a card face up that matches the suit or rank of the most recently played card. Eights are wild and can be played at any time. When a player plays an eight, they get to pick and change the current suit.

If the player can't match the top card, they must draw a card from the deck. If the rank or suit of the drawn card matches the card or suit of the most recently played card or the drawn card is an eight, the player can automatically play that card.

The first player to discard all their cards is the winner!  

This is implemented with sockets

## Installation
```pip install -r requirements.txt```

## Usage
Run the server:
```python Server.py --hostname <hostname> --port <port> ```

Run the client
```python Client.py --hostname <hostname> --port <port> ```
