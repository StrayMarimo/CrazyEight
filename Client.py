from display import DisplaySetUp
from game_menu import GameMenu
from play_menu import PlayMenu
from main_menu import MainMenu
import socket
import utils

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the port on which you want to connect
port = 12345

# Connect to the server on local computer
s.connect(('127.0.0.1', port))

# Receive ack from the server
print(s.recv(1024))

utils.set_initial_game_state()

# Use the received data to create the necessary objects
display_set_up = DisplaySetUp("Crazy Eights -- Client")
display = display_set_up.get_display()
main_clock = display_set_up.get_main_clock()
display_dimensions = display_set_up.get_display_dimensions()
background_image = display_set_up.get_background_image()

game_menu = GameMenu(display, display_dimensions, display_set_up, main_clock, background_image, False, s)

play_menu = PlayMenu(display_set_up, display, display_dimensions, main_clock, background_image, game_menu, False, s)

main_menu = MainMenu(display, main_clock, display_set_up, display_dimensions, background_image, play_menu)
main_menu.main_menu_loop()


# Close the connection
s.close()
