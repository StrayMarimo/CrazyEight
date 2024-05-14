import json
from deck import Card, Deck

def write_to_file(data, filename):
  with open('database/' + filename, 'w') as f:
    json.dump(data, f)

def read_from_file(filename):
  with open ('database/' + filename, 'r') as f:
    return json.load(f)

def save_deck_to_file(deck):
  deck_data = [card.to_dict() for card in deck.get_deck()]
  write_to_file(deck_data, 'deck.json')

def save_discard_pile_to_file(discard_pile):
  discard_pile_data = [card.to_dict() for card in discard_pile.get_cards_in_discard_pile()]
  write_to_file(discard_pile_data, 'discard_pile.json')

def save_player_hand_to_file(player, hand):
  player_hand_data = [card.to_dict() for card in hand.get_cards_in_hand()]
  write_to_file(player_hand_data, player + '.json')

def save_top_card_to_file(top_card):
  top_card_data = top_card.to_dict()
  write_to_file(top_card_data, 'top_card.json')

def load_deck_from_file(filename):
  deck_data = read_from_file(filename)
  return deck_data

def load_discard_pile_from_file(filename):
  discard_pile_data = read_from_file(filename)
  return discard_pile_data

def load_player_hand_from_file(filename):
  player_hand_data = read_from_file(filename)
  return player_hand_data

def load_top_card_from_file(filename):
  top_card_data = read_from_file(filename)
  return top_card_data

def set_initial_game_state():
  game_state = {
    'is_server_turn': True,
    # 'is_player2_turn': False,
    # 'did_player_won': False,
    # 'did_player2_won': False,
    # 'is_game_running': True,
    'is_player_ready': False,
    'is_player2_ready': False
  }
  write_to_file(game_state, 'game_state.json')

# def is_game_over():
#   game_state = read_from_file('game_state.json')
#   return game_state['is_game_over']

# def is_player_turn():
#   game_state = read_from_file('game_state.json')
#   return game_state['is_player_turn']

# def is_player2_turn():
#   game_state = read_from_file('game_state.json')
#   return game_state['is_player2_turn']

# def did_player_won():
#   game_state = read_from_file('game_state.json')
#   return game_state['did_player_won']

# def did_player2_won():
#   game_state = read_from_file('game_state.json')
#   return game_state['did_player2_won']

# def is_game_running():
#   game_state = read_from_file('game_state.json')
#   return game_state['is_game_running']

def set_server_turn(is_server_turn):
  game_state = read_from_file('game_state.json')
  game_state['is_server_turn'] = is_server_turn
  write_to_file(game_state, 'game_state.json')

def is_server_turn():
  game_state = read_from_file('game_state.json')
  return game_state['is_server_turn']

# def set_player2_turn():
#   game_state = read_from_file('game_state.json')
#   game_state['is_player2_turn'] = True
#   game_state['is_player_turn'] = False
#   write_to_file(game_state, 'game_state.json')

# def set_player_won():
#   game_state = read_from_file('game_state.json')
#   game_state['did_player_won'] = True
#   write_to_file(game_state, 'game_state.json')

# def set_player2_won():
#   game_state = read_from_file('game_state.json')
#   game_state['did_player2_won'] = True
#   write_to_file(game_state, 'game_state.json')

# def toggle_game_running(is_game_running):
#   game_state = read_from_file('game_state.json')
#   game_state['is_game_running'] = is_game_running
#   write_to_file(game_state, 'game_state.json')

def set_player_ready():
  game_state = read_from_file('game_state.json')
  game_state['is_player_ready'] = True
  write_to_file(game_state, 'game_state.json')

def set_player2_ready():
  game_state = read_from_file('game_state.json')
  game_state['is_player2_ready'] = True
  write_to_file(game_state, 'game_state.json')

def is_player_ready():
  game_state = read_from_file('game_state.json')
  return game_state['is_player_ready']

def is_player2_ready():
  game_state = read_from_file('game_state.json')
  return game_state['is_player2_ready']