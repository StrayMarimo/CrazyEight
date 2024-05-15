import pickle

def send_data(data, socket):
    pickled_data = pickle.dumps(data)

    socket.send(pickled_data + b'END_OF_PICKLE')

def receive_data(socket):
    data = b''
    while True:
        part = socket.recv(1024)
        data += part
        if b'END_OF_PICKLE' in part:
            break
    data = data[:-len(b'END_OF_PICKLE')]  # remove the delimiter from the end of the data
    if data:
        data = pickle.loads(data)
    else:
        data = None
    return data
  
def game_data_to_dict(deck=None, discard_pile=None, top_card=None, player1_hand=None, player2_hand=None, new_suit=None):
    return {
        'deck': [card.to_dict() for card in deck.get_deck()] if deck else None,
        'discard_pile': [card.to_dict() for card in discard_pile.get_cards_in_discard_pile()] if discard_pile else None,
        'top_card': top_card.to_dict() if top_card else None,
        'player1_hand': [card.to_dict() for card in player1_hand.get_cards_in_hand()] if player1_hand else None,
        'player2_hand': [card.to_dict() for card in player2_hand.get_cards_in_hand()] if player2_hand else None,
        'new_suit': new_suit
    }

def save_deck_to_file(deck, socket):
  deck_data = [card.to_dict() for card in deck.get_deck()]
  send_data(deck_data, socket)

def save_discard_pile_to_file(discard_pile, socket):
  discard_pile_data = [card.to_dict() for card in discard_pile.get_cards_in_discard_pile()]
  send_data(discard_pile_data, socket)

def save_player_hand_to_file(hand, socket):
  player_hand_data = [card.to_dict() for card in hand.get_cards_in_hand()]
  send_data(player_hand_data, socket)

def save_top_card_to_file(top_card, socket):
  top_card_data = top_card.to_dict()
  send_data(top_card_data, socket)