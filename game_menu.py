from deck import Card, Deck, Hand, DiscardPile
from button import Button
import utils
import pygame as pyg

class GameMenu:

    def __init__(self, display, display_dimensions, display_set_up, main_clock, bg, is_server, socket):

        self.__running = True
        self.__mouse_click = False

        self.__display = display
        self.__display_dimensions = display_dimensions
        self.__display_set_up = display_set_up
        self.__main_clock = main_clock
        self.__bg = bg
        self.__is_server = is_server
        self.__socket = socket

        self.__deck_img = pyg.image.load("img/cards/back.png")
        self.__deck_x_pos = (self.__display_dimensions[0] // 2) + 5
        self.__deck_y_pos = (self.__display_dimensions[1] // 2) - (self.__deck_img.get_height() // 2)

        self.__discard_pile_x = (self.__display_dimensions[0] // 2) - (self.__deck_img.get_width() + 5)
        self.__discard_pile_y = (self.__display_dimensions[1] // 2) - (self.__deck_img.get_height() // 2)

        self.__icons = {
            "clubs": pyg.image.load("img/clubs.png"),
            "diamonds": pyg.image.load("img/diamonds.png"),
            "hearts": pyg.image.load("img/hearts.png"),
            "spades": pyg.image.load("img/spades.png")
        }

        self.__icon_x_pos = self.__discard_pile_x + self.__icons.get("clubs").get_width() - 5
        self.__icon_y_pos = self.__discard_pile_y - self.__icons.get("clubs").get_height() - 15

        self.__change_suit_box_width = (self.__icons.get("clubs").get_width() * 4) + (13 * 2)
        self.__change_suit_box_height = self.__icons.get("clubs").get_height() + 30
        self.__change_suit_box_x_pos = (self.__display_dimensions[0] // 2) - (self.__change_suit_box_width // 2)
        self.__change_suit_box_y_pos = 360
        self.__yellow = (255, 210, 0)
        self.__white = (255, 255, 255)
        self.__change_suit_box_text = "Choose a Suit"
        self.__change_suit_font = pyg.font.Font("COMIC.TTF", 15)
        self.__change_suit_box = pyg.Rect(self.__change_suit_box_x_pos, self.__change_suit_box_y_pos, self.__change_suit_box_width, self.__change_suit_box_height)

        self.__win_text_x_pos = 0
        self.__win_text_y_pos = 0
        self.__win_text_font = pyg.font.Font("COMIC.TTF", 40)
        self.__player_win_text = "YOU WIN!"
        self.__player2_win_text = "OPPONENT WINS!"

        self.__icons_x_pos = {
            "clubs": self.__change_suit_box_x_pos + 5,
            "diamonds": self.__change_suit_box_x_pos + self.__icons.get("diamonds").get_width() + 10,
            "hearts": self.__change_suit_box_x_pos + (self.__icons.get("hearts").get_width() * 2) + 15,
            "spades": self.__change_suit_box_x_pos + (self.__icons.get("spades").get_width() * 3) + 20,
        }
        self.__change_suit_icon_y = self.__change_suit_box_y_pos + 25

        # self.__player_turn = True
        self.__draw_card = False
        self.__current_suit = None
        self.__eight_is_selected = False
        self.__selected_card = None
        self.__game_over = False
        self.__player_win = False
        self.__player2_win = False

    def update_screen(self, player_hand, player2_hand, discard_pile):
        self.__display.fill((0, 0, 0))

        # Scales the background image and places it on the screen
        scaled_bg = pyg.transform.scale(self.__bg, self.__display_dimensions)
        self.__display.blit(scaled_bg, (0, 0))

        # Displays the deck of cards on the screen
        self.__display.blit(self.__deck_img, (self.__deck_x_pos, self.__deck_y_pos))

        # Automatically moves cards in to the right position along the x-axis based on the width between cards,
        # the gap between cards and the number of cards currently in hand
        player_cards_x = (self.__display_dimensions[0] // 2) - ((70 + 5) * len(player_hand.get_cards_in_hand()) / 2)
        player_cards_y = self.__display_dimensions[1] // 2 + 125
        player_hand.show_hand(player_cards_x, player_cards_y, is_player=True)

        # Automatically moves cards in to the right position along the x-axis based on the width between cards,
        # the gap between cards and the number of cards currently in hand
        player2_cards_x = (self.__display_dimensions[0] // 2) - ((70 + 5) * len(player2_hand.get_cards_in_hand()) / 2)
        player2_cards_y = 65
        player2_hand.show_hand(player2_cards_x, player2_cards_y, is_player=False)

        discard_pile.show_top_card(self.__discard_pile_x, self.__discard_pile_y)

        self.__display_current_suit_icon()

        if self.__eight_is_selected:
            self.__display_change_suit_box()

    def game_menu_loop(self):
        """
        Runs and displays the game menu
        """

        self.__running = True
        self.__game_over = False
        self.__player_win = False
        self.__player2_win = False
        self.__is_receiving = False

        # Creates a deck, discard pile and player hand
        deck = Deck()
        discard_pile = DiscardPile(self.__display)
        player_hand = Hand(self.__display)
        player2_hand = Hand(self.__display)
        top_card = None

        if self.__is_server:

            # Shuffles the cards
            deck.shuffle_deck()

            # Adds 7 cards to the player hand and player2 hand
            for num in range(7):
                player_hand.add_card(deck.deal())
                player2_hand.add_card(deck.deal())

            # Sorts the player2 hand in descending order of rank so player2 always gets rid of higher rank cards first
            player2_hand.sort_hand(reverse=True)

            discard_pile.add_card(deck.deal())
            top_card = discard_pile.get_top_card()

            utils.save_deck_to_file(deck)
            utils.save_discard_pile_to_file(discard_pile)
            utils.save_top_card_to_file(top_card)

            utils.save_player_hand_to_file("player1", player_hand)
            utils.save_player_hand_to_file("player2", player2_hand)

        else:
            deck.set_deck(utils.load_deck_from_file('deck.json'))
            discard_pile.set_cards_in_discard_pile(utils.load_discard_pile_from_file('discard_pile.json'), utils.load_top_card_from_file('top_card.json'))
            player_hand.set_cards_in_hand(utils.load_player_hand_from_file('player2.json'))
            player2_hand.set_cards_in_hand(utils.load_player_hand_from_file('player1.json'))

        self.__current_suit = discard_pile.get_top_card().get_suit()

        game_loads = False

        while self.__running:
            self.update_screen(player_hand, player2_hand, discard_pile)
            if self.__is_receiving and game_loads:
                self.update_screen(player_hand, player2_hand, discard_pile)
                received_data = self.__socket.recv(1024)
                if received_data:
                    print("Received data: ", received_data)
                    deck.set_deck(utils.load_deck_from_file('deck.json'))
                    discard_pile.set_cards_in_discard_pile(utils.load_discard_pile_from_file('discard_pile.json'), utils.load_top_card_from_file('top_card.json'))
                    top_card = discard_pile.get_top_card()
                    if self.__is_server:
                        player_hand.set_cards_in_hand(utils.load_player_hand_from_file('player1.json'))
                        player2_hand.set_cards_in_hand(utils.load_player_hand_from_file('player2.json'))
                    else:
                        player_hand.set_cards_in_hand(utils.load_player_hand_from_file('player2.json'))
                        player2_hand.set_cards_in_hand(utils.load_player_hand_from_file('player1.json'))
                    self.__current_suit = discard_pile.get_top_card().get_suit()
                    self.__is_receiving = False

            self.update_screen(player_hand, player2_hand, discard_pile)

            # If the game is over displays a win or lose message depending on whether the player or player2 won
            if self.__game_over:
                if self.__player_win:
                    self.__display_win_text(self.__player_win_text)
                if self.__player2_win:
                    self.__display_win_text(self.__player2_win_text)
                self.__socket.send(b'game over')

            # Stores the position of the mouse
            mouse_pos = pyg.mouse.get_pos()

            if not self.__game_over:
                # Loops through the cards in the players hand
                for card in player_hand.get_cards_in_hand():
                    # Checks if it is the player turn
                    if not self.__is_receiving:
                        card_img = card.get_image()
                        card_rect_x = card.get_x() + (card_img.get_width() / 2)
                        card_rect_y = card.get_y() + (card_img.get_height() / 2)
                        if card_img.get_rect(center=(card_rect_x, card_rect_y)).collidepoint((mouse_pos[0], mouse_pos[1])) and not self.__eight_is_selected:
                            if self.__mouse_click:
                                self.__player_card_play(discard_pile, card, player_hand, player2_hand)
                                self.__mouse_click = False

                        if self.__eight_is_selected:
                            self.__player_eight_play(mouse_pos, player_hand, player2_hand, discard_pile)
        
                        # if self.__is_server and game_start:
                        #     game_start = False
                self.__check_for_win(player_hand, player2_hand)

                self.__reshuffle_deck(deck, discard_pile)
                deck.set_deck(utils.load_deck_from_file('deck.json'))
                
                # Loops through the cards in the players hand and checks if a playable card is present. If not,
                # allows the player to draw a single card
                for card in player_hand.get_cards_in_hand():
                    if not self.__is_receiving:
                        top_card = discard_pile.get_top_card()
                        top_card_rank = top_card.get_rank()

                        card_suit = card.get_suit()
                        card_rank = card.get_rank()
                        if card_rank == "eight" or card_suit == self.__current_suit or card_rank == top_card_rank:
                            self.__draw_card = False
                            break
                        else:
                            self.__draw_card = True
            # If player cannot play any card, player can draw a card
            if not self.__is_receiving and self.__draw_card:
                deck_rect_x = self.__deck_x_pos + (self.__deck_img.get_width() / 2)
                deck_rect_y = self.__deck_y_pos + (self.__deck_img.get_height() / 2)
                if self.__deck_img.get_rect(center=(deck_rect_x, deck_rect_y)).collidepoint((mouse_pos[0], mouse_pos[1])):
                    if self.__mouse_click:
                        self.__card_draw(deck, player_hand, discard_pile)
                        
                        self.__draw_card = False
                        if not self.__eight_is_selected:
                            if self.__is_server:
                                player_hand.set_cards_in_hand(utils.load_player_hand_from_file('player1.json'))
                                utils.set_server_turn(False)
                            else:
                                player_hand.set_cards_in_hand(utils.load_player_hand_from_file('player2.json'))
                                utils.set_server_turn(True)
                            deck.set_deck(utils.load_deck_from_file('deck.json'))
                            self.__is_receiving = True
                            self.update_screen(player_hand, player2_hand, discard_pile)
                            self.__socket.send(b'opponent drew a card')

            # Allows player2 to play a turn and sets player turn to true to allow player to play a card or draw a card
            # if the game is not over
            if not self.__game_over and self.__is_receiving:
                self.__reshuffle_deck(deck, discard_pile)
                deck.set_deck(utils.load_deck_from_file('deck.json'))
                self.__check_for_win(player_hand, player2_hand)
                if self.__is_server:
                    utils.set_server_turn(True)
                else:
                    utils.set_server_turn(False)

            # Resets the mouse click
            self.__mouse_click = False

            for event in pyg.event.get():
                # If the exit button is clicked, exits the program
                if event.type == pyg.QUIT:
                    self.__display_set_up.exit()
                # If a key is pressed and that key is escape (ESC), exits the program
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        self.__running = False
                # If the left mouse button is clicked, sets the mouse click to true
                if event.type == pyg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.__mouse_click = True

            # Updates the screen on every iteration
            pyg.display.update()
            # Sets the FPS
            self.__main_clock.tick(60)

            if not game_loads and self.__is_server:
                self.__socket.send(b'game start')
                data = self.__socket.recv(1024)
                if data:
                    game_loads = True
            if not game_loads and not self.__is_server:
                data = self.__socket.recv(1024)
                if data: 
                    game_loads = True
                    self.__is_receiving = True
                    self.__socket.send(b' game start')

    def __player_card_play(self, discard_pile, card, hand, opponent_hand):
        """
        Allows for the play of a playable card
        """

        top_card = discard_pile.get_top_card()
        top_card_rank = top_card.get_rank()

        # Stores the current suit and rank of the card in player2 hand
        card_suit = card.get_suit()
        card_rank = card.get_rank()

        # Checks if the card is an 8
        if card_rank == "eight":
            self.__eight_is_selected = True
            self.__selected_card = card
        else:
            # Checks if the cards suit or rank equals that of the discard pile card
            if card_suit == self.__current_suit or card_rank == top_card_rank:
                self.__add_card_to_discard_pile(hand, card, discard_pile)
                self.update_screen(hand, opponent_hand, discard_pile)
                self.__is_receiving = True
                self.__socket.send(b'opponent played a card')


    def __player_eight_play(self, mouse_pos, hand, opponent_hand, discard_pile):
        """
        Allows the player to change the current suit when they play an 8
        """

        for icon in self.__icons:
            icon_x_pos = self.__icons_x_pos.get(icon) + (self.__icons.get(icon).get_width() / 2)
            icon_y_pos = self.__change_suit_icon_y + (self.__icons.get("clubs").get_height() / 2)
            if self.__icons.get(icon).get_rect(center=(icon_x_pos, icon_y_pos)).collidepoint(mouse_pos[0], mouse_pos[1]):
                if self.__mouse_click:
                    card_to_remove = hand.remove_card(self.__selected_card)
                    discard_pile.set_top_card(card_to_remove)
                    discard_pile.add_card(card_to_remove)

                    self.__current_suit = icon
                    self.__selected_card = None
                    self.__eight_is_selected = False

                    top_card = discard_pile.get_top_card()
                    top_card.set_suit(icon)
                    utils.save_top_card_to_file(top_card)
                    # print(top_card)

                    if self.__is_server:
                        utils.save_player_hand_to_file("player1", hand)

                    else:
                        utils.save_player_hand_to_file("player2", hand)
                    utils.save_discard_pile_to_file(discard_pile)


                    self.update_screen(hand, opponent_hand, discard_pile) 
                    self.__is_receiving = True
                    self.__socket.send(b'opponent played an 8')

    def __card_draw(self, deck, hand, discard_pile):
        """
        Draws a card into the hand. If the card is playable, plays it automatically
        """

        print("drawing a card")
        card = deck.deal()
        hand.add_card(card)

        utils.save_deck_to_file(deck)

        top_card = discard_pile.get_top_card()
        top_card_rank = top_card.get_rank()

        if card.get_rank() == "eight":
            self.__eight_is_selected = True
            self.__selected_card = card
        else:
            if card.get_suit() == self.__current_suit or card.get_rank() == top_card_rank:
                card = hand.remove_card(card)
                discard_pile.set_top_card(card)
                discard_pile.add_card(card)

                top_card = discard_pile.get_top_card()
                utils.save_top_card_to_file(top_card)

        if self.__is_server:
            utils.save_player_hand_to_file("player1", hand)

        else:
            utils.save_player_hand_to_file("player2", hand)
        utils.save_discard_pile_to_file(discard_pile)
            
        self.__current_suit = discard_pile.get_top_card().get_suit()

    def __add_card_to_discard_pile(self, hand, card, discard_pile):
        """
        Removes a card from hand and adds it to the discard pile
        """
        card_to_remove = hand.remove_card(card)
        discard_pile.set_top_card(card_to_remove)
        discard_pile.add_card(card_to_remove)

        top_card = discard_pile.get_top_card()
        utils.save_top_card_to_file(top_card)

        if self.__is_server:
            utils.save_player_hand_to_file("player1", hand)

        else:
            utils.save_player_hand_to_file("player2", hand)
        utils.save_discard_pile_to_file(discard_pile)
            
        self.__current_suit = discard_pile.get_top_card().get_suit()

    def __check_for_win(self, player_hand, player2_hand):
        """
        Checks if player or player2 discarded all their cards. If so, ends the game
        """

        if len(player_hand.get_cards_in_hand()) == 0:
            self.__draw_card = False
            self.__game_over = True
            self.__player_win = True

        if len(player2_hand.get_cards_in_hand()) == 0:
            self.__draw_card = False
            self.__game_over = True
            self.__player2_win = True

    @staticmethod
    def __reshuffle_deck(deck, discard_pile):
        """
        When there is no more cards in the deck, moves all the cards aside from the last played card from the
        discard pile back into the deck and shuffles the deck
        """

        if len(deck.get_deck()) == 0:
            cards = discard_pile.get_cards_in_discard_pile()[:-1]
            deck.reset_deck(cards)
            deck.shuffle_deck()
            utils.save_deck_to_file(deck)

    def __display_current_suit_icon(self):
        """
        Displays the icon of the suit of the current top card in the discard pile
        """

        self.__display.blit(self.__icons.get(self.__current_suit), (self.__icon_x_pos, self.__icon_y_pos))

    def __display_change_suit_box(self):
        """
        Displays a box which allows player to change the current suit when player plays an 8
        """

        pyg.draw.rect(self.__display, self.__yellow, self.__change_suit_box)

        text = self.__change_suit_font.render(self.__change_suit_box_text, True, self.__white)
        self.__display.blit(text, (self.__change_suit_box_x_pos + 27, self.__change_suit_box_y_pos))

        for icon in self.__icons:
            self.__display.blit(self.__icons.get(icon), (self.__icons_x_pos.get(icon), self.__change_suit_icon_y))

    def __display_win_text(self, win_text):
        """
        Displays who won the game
        """

        text = self.__win_text_font.render(win_text, True, self.__white)
        self.__win_text_x_pos = (self.__display_dimensions[0] // 2) - (text.get_width() // 2)
        self.__display.blit(text, (self.__win_text_x_pos, self.__win_text_y_pos))
