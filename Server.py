from display import DisplaySetUp
from game_menu import GameMenu
from play_menu import PlayMenu
from main_menu import MainMenu
import utils
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345

# Bind to the port
s.bind(('', port))

# Put the socket into listening mode
s.listen(5)

print('Server is listening')

while True: 
  c, addr = s.accept()
  print('Got connection from', addr)

  # Send ack to client
  c.send(b'Thank you for connecting')

  utils.set_initial_game_state()
  display_set_up = DisplaySetUp("Crazy Eights -- Server")
  display = display_set_up.get_display()
  main_clock = display_set_up.get_main_clock()
  display_dimensions = display_set_up.get_display_dimensions()
  background_image = display_set_up.get_background_image()

  game_menu = GameMenu(display, display_dimensions, display_set_up, main_clock, background_image, True, c)

  play_menu = PlayMenu(display_set_up, display, display_dimensions, main_clock, background_image, game_menu, True, c)

  main_menu = MainMenu(display, main_clock, display_set_up, display_dimensions, background_image, play_menu)
  main_menu.main_menu_loop()

  # Close the connection with the client
  c.close()
