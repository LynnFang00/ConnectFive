'''
This is a chess game involving two players, one holds the black side and the other one holds the white side.
The game by default starts with the black side, and the two players take turns to place a chess piece.
The chess piece can be placed on any empty intersections.
The way to win this game is to connect 5 chess pieces of your color in a row in any of the four directions (horizontal, vertical, and two diagonals).
In this code, the pygame package is installed. There are two classes, GameObject and Button.
Multiple user-define functions are also used.
In the game, black side is represented by O in the object list, and even numbers of the flag.
White side is represented by X in the object list, and odd numbers of the flag.
There are three buttons on the right side. 
    Regret - Recall the last chess piece placed.
    Recover - Recover the last chess pieced recalled.
    Restart - Restart the whole game.
Get ready to strategize, outwit your opponent, and claim victory in Connect Five!
'''

import pygame as pg

# The GameObject class has attributes for each stone and is used in appending object list
class GameObject:
    def __init__(self, image, pos):
        self.image = image
        self.pos = image.get_rect(center= pos) # Rectangular object, set center to position

# The Button class has the attributes for buttons on the screen
class Button:
    def __init__(self, text, color, x = None, y = None):
        self.surface = pg.font.SysFont("Times New Roman", 40).render(text, True, color) # Surface object
        self.WIDTH = self.surface.get_width() # Get the width and the height of the button
        self.HEIGHT = self.surface.get_height()
        self.x = x
        self.y = y

    # This function is used to check if a button is clicked
    def check_click(self, position) -> bool:
        x_match = self.x < position[0] < self.x + self.WIDTH
        y_match = self.y < position[1] < self.y + self.HEIGHT
        if x_match and y_match: # If both the x and y position of the mouse is in the area of the button
            return True
        else:
            return False

# This function loads an image from a file and convert it to a format suitable for display with alpha transparency.
def load_image(name):
    return pg.image.load(name).convert_alpha()
    #Alpha transparency refers to the level of opacity or translucency of an image or pixel.
    #Alpha transparency enables images to have areas that are see-through, allowing them to blend smoothly with the background or other images when displayed.

# This function is used to set chess when clicking on the board
# It checks and updates the corresponding position in the list
def set_chess(board,x,y,color) -> bool:
    if board[x][y] != ' ':
        print('spot occupied')
        return False
    else:
        board[x][y] = color
        return True

# This function is used to check if there's a winning condition on the board
# Return 0 if 'O' (black) wins, 1 if 'X' (white) wins, -1 if no one wins yet.
# The game board is represented as a list of strings
def check_win(board) -> int:
    for list_str in board:
        if ''.join(list_str).find('O'*5) != -1:
            # join() is used to concatenate all the characters in list_str (which represents a row or column of the board) into a single string
            # find() returns the index of the first occurrence of the substring if found, and -1 if the substring is not found
            print('Black Win')
            return 0
        elif ''.join(list_str).find('X'*5) != -1:
            print('White Win')
            return 1
    else:
        return -1

# This function checks the winning condition in the board in all directions
# It shifts the objects in different directions to a list in transverse direction, and apply the same checking function
def check_win_all(board) -> list:
    board_c = [[] for i in range(29)] # Diagonal - bottom left to top right
    for x in range(15):
        for y in range(15):
            board_c[x+y].append(board[x][y])
    board_d =  [[] for i in range(29)] # Diagonal - top left to bottom right
    for x in range(15):
        for y in range(15):
            board_d[x-y].append(board[x][y])
    return [check_win(board) , # Horizontal
             check_win([list(i) for i in zip(*board)]) , # Vertical  # change tuple type to a list
            check_win(board_c) , # Diagonal - bottom left to top right
            check_win(board_d)] # Diagonal - top left to bottom right


def running():

    WIDTH = 815 # The width and height of the game board
    HEIGHT = 615

    board = [[' ']*15 for line in range(15)]
    objects = [] # A list to store the record of stone being placed
    recover_objects = [] # A list used to recover regretted stone

    # Initialize
    pg.font.init() # Initialize the Pygame font module
    pg.init() # Initialize all Pygame modules
    screen = pg.display.set_mode((WIDTH, HEIGHT)) # Set up the display window with the specified width and height

    # Load the image of stones and the background
    black = load_image("stone_black.png")
    white = load_image("stone_white.png")
    background = load_image(r"C:\CS ISU\ISU\bg.png")

    # Create buttons and display
    regret_button = Button("regret", (255,0,0), 657, 200) # Create a button with its text, color, and position
    screen.blit(regret_button.surface, (regret_button.x, regret_button.y)) # Display the button at its position
    recover_button = Button("recover", (255, 0, 0), 645, 300)
    screen.blit(recover_button.surface, (recover_button.x, recover_button.y))
    restart_button = Button("restart", (255, 0, 0), 657, 400)
    screen.blit(restart_button.surface, (restart_button.x, restart_button.y))

    pg.display.set_caption("Connect Five") # Window's title
    font = pg.font.SysFont('Times New Roman', 20)
    flag = 0 # Initialize the flag, starts with black

    going = True # Control the main loop to keep going or to end
    while going:

        if flag % 2 == 0: # Even - Black's turn
            text = font.render("Black's Turn", True, (0, 0, 0)) # The
        else: # Odd - White's turn
            text = font.render("White's Turn", True, (255, 255, 255))
        textpos = text.get_rect(centerx=background.get_width() / 2, centery=12) # This method returns a Rect object that represents the bounding box of the rendered text, with specified x and y coordinate
        screen.blit(background, (0, 0)) # Display the background surface onto the screen at position (0, 0)
        screen.blit(text, textpos) # Display the rendered text onto the screen at the position specified by textpos

        for event in pg.event.get():
            if event.type == pg.QUIT: # Check if the user clicks the close button on the window
                going = False # Set the 'going' variable to False to exit the loop
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # Check if the event type is KEYDOWN and if the key pressed is the escape key
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN: # Check if the mouse button is pressed
                pos = pg.mouse.get_pos() # Get the current mouse position
                if restart_button.check_click(pos): # Check if the restart button is clicked
                    restart_sound.play() # Play the sound when the restart button is hit
                    return True # Indicates to restart

                elif regret_button.check_click(pos): # Check if the regret button is clicked
                    click_sound.play() # Play the sound when the regret button is hit
                    if objects: # Check if there are objects on the board
                        print(objects)
                        x, y = [round((i + 18 - 27) / 40) for i in objects[-1].pos[:2]]
                        #print(objects[-1].pos)
                        #print(x,y)# Get the board position of the last placed flag
                        recover_objects.append([objects.pop(-1), board[x][y]])  # Add the flag object and it's color to the regret list(O or X)
                        print(recover_objects)
                        board[x][y] = ' '  # Clear the position on the board
                        #print(board) ### why is the board from top to bottom than from left to right
                        flag += 1  # Shift turn
                    else: # Show a hint text if there are no objects on the board
                        hint_text = font.render("nothing to regret", True,(0, 0, 0))
                        hint_textpos = hint_text.get_rect(centerx=background.get_width() / 2,centery=200)
                        screen.blit(hint_text, hint_textpos)
                        for o in objects:  # Keep showing the chess at the same time
                            screen.blit(o.image, o.pos)
                        pg.display.update()
                        pg.time.delay(300)
                        print("Nothing to regret")  # Prevent crash in case there's no flag on the board

                elif recover_button.check_click(pos): # If the recover button is clicked
                    click_sound.play() # Play the sound when the recover button is hit
                    if recover_objects: # If the list is not empty
                        x, y = [round((i + 18 - 27) / 40) for i in recover_objects[-1][0].pos[:2]]  # Get the board position and color of the last regret position
                        board[x][y] = recover_objects[-1][1]  # Set the last regret position to the original color
                        objects.append(recover_objects.pop(-1)[0])  # re-add the flag object
                        flag += 1  # Change the color
                    else: # Show a hint text if there are no objects in the recover list
                        hint_text = font.render("nothing to recover", True,(0, 0, 0))
                        hint_textpos = hint_text.get_rect(centerx=background.get_width() / 2, centery=200)
                        screen.blit(hint_text, hint_textpos)
                        for o in objects:  ###what is objects
                            screen.blit(o.image, o.pos)
                        pg.display.update()
                        pg.time.delay(300)
                        print("nothing to recover")  # Prevent crash in case there's no regret history

                else:  # Convert mouse position to bo ard position
                    chess_place_sound.play() # Play the sound when the chess piece is placed on the board screen
                    a, b = round((pos[0] - 27) / 40), round((pos[1] - 27) / 40)
                    if a >= 15 or b >= 15: # Check if the position is within the board  boundaries
                        continue
                    # Round the x and y position, when it's on the edge or outside the board shown on the screen, round it to 0 or 14
                    if pos[0] > 587:
                        x = 14
                    elif pos[0] < 27:
                        x = 0
                    else:
                        x = round((pos[0] - 27) / 40)
                    if pos[1] > 587:
                        y = 14
                    elif pos[1] < 27:
                        y = 0
                    else:
                        y = round((pos[1] - 27) / 40)

                    # Check whose turn it is and place the corresponding chess piece
                    if flag % 2 == 0: # Black's turn
                        if set_chess(board, x, y, 'O'): # True or False, True --> spot not occupied
                            objects.append(GameObject(black, (27 + x * 40, 27 + y * 40))) # Display the chess image onto the screen
                            #print(objects[-1].pos) # Print the last step's position
                            flag = 1 # Change to white's turn
                            recover_objects = [] # Set the recover_object list to empty
                            print(board)
                            print(objects) # game object and position
                            print(recover_objects) # X or O
                        else:  # Show a hint text if the spot is taken
                            hint_text = font.render("spot taken", True, (0,0,0))
                            hint_textpos = hint_text.get_rect(centerx=background.get_width() / 2, centery=200)
                            for o in objects:
                                screen.blit(o.image, o.pos)
                            screen.blit(hint_text, hint_textpos)
                            pg.display.update()
                            pg.time.delay(300) # Pause for 0.3 seconds

                    else: # White's turn
                        if set_chess(board, x, y, 'X'):
                            objects.append(GameObject(white, (27 + x * 40, 27 + y * 40)))
                            flag = 0
                            recover_objects = []
                        else:
                            hint_text = font.render("spot taken", True, (255, 255, 255))
                            hint_textpos = hint_text.get_rect(centerx=background.get_width() / 2, centery=200)
                            for o in objects:
                                screen.blit(o.image, o.pos)
                            screen.blit(hint_text, hint_textpos)
                            pg.display.update()
                            pg.time.delay(300) # Pause for 0.3 seconds

        # Display the chess image to its position
        for o in objects:
            screen.blit(o.image, o.pos)

        if 0 in check_win_all(board): # Check if black wins
            win_text = font.render("Black Wins. Game begins in 3 seconds.", True, (0, 0, 0)) # Render text indicating black player wins
            win_textpos = win_text.get_rect(centerx=background.get_width() / 2, centery=200)
            screen.blit(win_text, win_textpos) # Display the text on the screen
            pg.display.update()
            pg.time.delay(3000) # Pause for 3 seconds
            # Reset the board, objects, and flag for a new game
            board = [[' '] * 15 for line in range(15)]
            objects = []
            flag = 0
        elif 1 in check_win_all(board): # Check if white wins
            win_text = font.render("White Wins. Game begins in 3 seconds.", True, (255, 255, 255))
            win_textpos = win_text.get_rect(centerx=background.get_width() / 2, y=200)
            screen.blit(win_text, win_textpos)
            pg.display.update()
            pg.time.delay(3000)
            board = [[' '] * 15 for line in range(15)]
            objects = []

        pg.display.update()

    pg.mixer.music.stop() # Stop the music
    pg.quit() # Quit Pygame


if __name__ == "__main__":
    # Load the music for clicking the board, functionality buttons, and the background music
    pg.mixer.init()
    click_sound = pg.mixer.Sound('click.mp3')
    chess_place_sound = pg.mixer.Sound('chess_place.mp3')
    restart_sound = pg.mixer.Sound('restart.mp3')
    pg.mixer.music.load('bg_music.mp3')
    pg.mixer.music.play(-1, 0) # Play the background music in a loop, start from the beginning

    restart = False  # Initialize state
    restart = running()
    while restart:  # If the current process is closed manually, restart the process
        restart = False
        restart = running()


