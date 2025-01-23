'''
MAIN FILE : To handle user moves ( input ) and display the Output
'''

import pygame as pg
import ChessEngine , MoveFinder
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = HEIGHT = 512
DIMENSION = 8
SQR = HEIGHT // DIMENSION # 8 x 8 square total to be made z

MAX_FPS = 15
IMAGES = {}

def loadimages():
    #list of pieces and then load pieces
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces :
        IMAGES[piece] = pg.transform.scale(pg.image.load("Images/" + piece + ".png") , (SQR , SQR))
        #Above dictionary stores the piece as key and image as value
        #To Access the image we can use   :   'IMAGES[piece]'

'''
DRIVER CODE TO HANDLE INPUT OUTPUT 
'''
def draw_button(screen, text, rect, font, color, hover_color, is_hovered):
    """Draw a button with hover effect."""
    pg.draw.rect(screen, hover_color if is_hovered else color, rect)
    text_surf = font.render(text, True, pg.Color("white"))
    screen.blit(
        text_surf,
        (rect.centerx - text_surf.get_width() // 2, rect.centery - text_surf.get_height() // 2),
    )

def show_menu(screen):
    """Display the main menu with button-style options."""
    font = pg.font.SysFont("Helvetica", 32, True, False)
    title_font = pg.font.SysFont("Helvetica", 48, True, False)
    options = ["Player vs Player", "Player vs AI", "Exit"]
    button_rects = []
    selected_option = 0

    # Create button rects dynamically
    button_width, button_height = 250, 50
    spacing = 20
    start_y = HEIGHT / 3

    for i in range(len(options)):
        button_rects.append(pg.Rect((WIDTH / 2 - button_width / 2, start_y + i * (button_height + spacing)), (button_width, button_height)))

    running = True
    while running:
        screen.fill(pg.Color("lightblue"))

        # Title
        title_surf = title_font.render("Chess Game", True, pg.Color("darkblue"))
        screen.blit(title_surf, (WIDTH / 2 - title_surf.get_width() / 2, HEIGHT / 6))

        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return None
            elif event.type == pg.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        return i

        for i, rect in enumerate(button_rects):
            is_hovered = rect.collidepoint(mouse_pos)
            draw_button(
                screen,
                options[i],
                rect,
                font,
                pg.Color("darkblue"),
                pg.Color("blue"),
                is_hovered,
            )

        pg.display.flip()

def show_end_screen(screen, message):
    """Display the end screen with button-style options."""
    font = pg.font.SysFont("Helvetica", 32, True, False)
    title_font = pg.font.SysFont("Helvetica", 48, True, False)
    options = ["Play Again", "Exit"]
    button_rects = []

    button_width, button_height = 250, 50
    spacing = 20
    start_y = HEIGHT / 2

    for i in range(len(options)):
        button_rects.append(pg.Rect((WIDTH / 2 - button_width / 2, start_y + i * (button_height + spacing)), (button_width, button_height)))

    running = True
    while running:
        screen.fill(pg.Color("lightblue"))

        # Title
        title_surf = title_font.render(message, True, pg.Color("darkblue"))
        screen.blit(title_surf, (WIDTH / 2 - title_surf.get_width() / 2, HEIGHT / 3))

        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return None
            elif event.type == pg.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        return i

        for i, rect in enumerate(button_rects):
            is_hovered = rect.collidepoint(mouse_pos)
            draw_button(
                screen,
                options[i],
                rect,
                font,
                pg.Color("darkblue"),
                pg.Color("blue"),
                is_hovered,
            )

        pg.display.flip()


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    
    while True:
        mode = show_menu(screen)
        if mode is None or mode == 2:  # Exit option
            break

        playerOne = True  # Player 1 is always human
        playerTwo = mode == 0  # Player 2 is human if "Player vs Player" is selected

        g_state = ChessEngine.GameState()
        validMoves = g_state.getValidMoves()
        moveMade = False
        AIThinking = False
        loadimages()
        running = True
        undoMade = False
        gameOver = False

        sqrSelected = ()
        playerClicks = []

        while running:
            isHuman = (g_state.whitemove and playerOne) or (not g_state.whitemove and playerTwo)
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    running = False
                elif e.type == pg.MOUSEBUTTONDOWN and isHuman and not gameOver:
                    # Handle player move
                    location = pg.mouse.get_pos()
                    col = location[0] // SQR
                    row = location[1] // SQR
                    if sqrSelected == (row, col):
                        sqrSelected = ()
                        playerClicks = []
                    else:
                        sqrSelected = (row, col)
                        playerClicks.append(sqrSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], g_state.board)
                        for validMove in validMoves:
                            if move == validMove:
                                g_state.make_Move(validMove)
                                moveMade = True
                                sqrSelected = ()
                                playerClicks = []
                                break
                        if not moveMade:
                            playerClicks = [sqrSelected]
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_r:  # Restart game
                        running = False
                    elif e.key == pg.K_z:  # Undo move
                        g_state.undo_Move()
                        moveMade = True
                        gameOver = False

            # AI Move
            if not gameOver and not isHuman and not moveMade:
                if not AIThinking and not undoMade:
                    AIThinking = True
                    AImove = MoveFinder.findRandomMove(validMoves)
                    g_state.make_Move(AImove)
                    moveMade = True
                    AIThinking = False

            if moveMade:
                validMoves = g_state.getValidMoves()
                moveMade = False

            draw_game_state(screen, g_state, validMoves, sqrSelected)

            if g_state.CheckMate:
                gameOver = True
                message = "Black wins by Checkmate!" if g_state.whitemove else "White wins by Checkmate!"
                option = show_end_screen(screen, message)
                if option == 1:
                    return
                elif option == 0:
                    running = False
            elif g_state.StaleMate:
                gameOver = True
                option = show_end_screen(screen, "Stalemate!")
                if option == 1:
                    return
                elif option == 0:
                    running = False

            clock.tick(MAX_FPS)
            pg.display.flip()


# def main():
#     pg.init()
#     screen = pg.display.set_mode((WIDTH, HEIGHT))
#     clock = pg.time.Clock()
#     screen.fill(pg.Color("white"))
#     g_state = ChessEngine.GameState()
#     validMoves = g_state.getValidMoves()
#     moveMade = False  # Track if a move is made
#     AIThinking = False  # Track if the AI is calculating its move
#     loadimages()  # Done once only
#     running = True
#     undoMade = False

#     sqrSelected = ()  # Tuple to keep track of the selected square by the user
#     playerClicks = []  # Keep track of user's initial and final clicks
#     gameOver = False
#     playerOne = True  # Human plays white if True
#     playerTwo = False  # Human plays black if True


#     while running:
#         isHuman = (g_state.whitemove and playerOne) or (not g_state.whitemove and playerTwo)  # True if human turn
        
#         for e in pg.event.get():
#             if e.type == pg.QUIT:
#                 running = False
#             elif e.type == pg.MOUSEBUTTONDOWN:
#                 if not gameOver and isHuman and not moveMade:
#                     location = pg.mouse.get_pos()  # (x, y) of mouse click
#                     col = location[0] // SQR
#                     row = location[1] // SQR

#                     if sqrSelected == (row, col):
#                         # Deselect the square if clicked again
#                         sqrSelected = ()
#                         playerClicks = []
#                     else:
#                         sqrSelected = (row, col)
#                         playerClicks.append(sqrSelected)

#                     if len(playerClicks) == 2:  # After second click
#                         move = ChessEngine.Move(playerClicks[0], playerClicks[1], g_state.board)
#                         print(move.getChessNotation())

#                         for validMove in validMoves:
#                             if move == validMove:
#                                 g_state.make_Move(validMove)  # Make the move
#                                 moveMade = True
#                                 sqrSelected = ()
#                                 playerClicks = []
#                                 undoMade = False
#                                 break  # Exit loop once move is made
                        
#                         if not moveMade:
#                             # Reset selection if move was invalid
#                             playerClicks = [sqrSelected]

#             elif e.type == pg.KEYDOWN:
#                 if e.key == pg.K_z:  # Undo move with "Z"
#                     g_state.undo_Move()
#                     moveMade = True
#                     gameOver = False
#                     undoMade = False
                
#                 if e.key == pg.K_t: #TakeBack move with "T"
#                     g_state.undo_Move()
#                     undoMade = True
#                     moveMade = True 
#                     gameOver = False

#                 if e.key == pg.K_r:  # Reset the board with "R"
#                     g_state = ChessEngine.GameState()
#                     validMoves = g_state.getValidMoves()
#                     sqrSelected = ()
#                     playerClicks = []
#                     moveMade = False
#                     gameOver = False
#                     undoMade = False

#         # AI Turn
#         if not gameOver and not isHuman and not moveMade :
#             if not AIThinking and not undoMade:
#                 AIThinking = True
#                 AImove = MoveFinder.findRandomMove(validMoves)
#                 g_state.make_Move(AImove)
#                 moveMade = True
#                 AIThinking = False

#         if moveMade:
#             validMoves = g_state.getValidMoves()  # Update valid moves
#             moveMade = False

#         draw_game_state(screen, g_state, validMoves, sqrSelected)

#         if g_state.CheckMate:
#             gameOver = True
#             if g_state.whitemove:
#                 drawText(screen, "BLACK WINS BY CHECKMATE")
#             else:
#                 drawText(screen, "WHITE WINS BY CHECKMATE")
#         elif g_state.StaleMate:
#             gameOver = True
#             drawText(screen, "STALEMATE")

#         clock.tick(MAX_FPS)
#         pg.display.flip()


'''
HIGHLIGHTS POSSIBLE MOVE SQUARES FOR A PIECE 
'''
def highlight_sqrs(screen , g_state ,validMoves ,  sqr_selected):
    if sqr_selected != ():
        row , col  = sqr_selected
        if g_state.board[row][col][0] == ('w' if g_state.whitemove else 'b') :
            #highlight selected sqr
            s = pg.Surface((SQR , SQR))
            s.set_alpha(100) #transparency  , if 0 then transparent else 100 means opaque
            s.fill((0, 0, 255))  # blue color
            screen.blit(s , (col * SQR , row * SQR))
            #highlight moves from that square
            s.fill(pg.Color('yellow'))
            for move in validMoves :
                if move.startRow == row and move.startCol == col :
                    screen.blit(s , (SQR*move.endCol , SQR*move.endRow))


'''
DRAWING THE GAME BOARD AND PIECES
'''

def draw_game_state(screen , g_state , validMoves , sqr_selected) :
    drawBoard(screen)
    highlight_sqrs(screen , g_state , validMoves , sqr_selected)
    drawPieces(screen , g_state.board)

def drawText(screen , text) :
    font = pg.font.SysFont("Helvitca" , 32 , True , False)
    textObj = font.render(text , 0 , pg.Color('Black'))
    textLoc = pg.Rect(0 , 0 , WIDTH , HEIGHT).move(WIDTH/2 - textObj.get_width()/2 , HEIGHT/2 - textObj.get_height()/2)
    textObj = font.render(text , 0 , pg.Color('Red'))
    screen.blit(textObj , textLoc.move(2 , 2))
'''
WE CAN PASS ANOTHER ARGUMENT TO CHOOSE THE COLOR COMBINATIONS
ACCORDING TO THE USER 
'''
def drawBoard(screen):
    colors = [pg.Color("white") , pg.Color("gray")]
    for row in range(DIMENSION) :
        for col in range(DIMENSION) : 
            color  = colors[((row + col) % 2)]
            pg.draw.rect(screen , color , pg.Rect(col*SQR , row*SQR , SQR , SQR)) 
            #pg.Rect(left , top , height , width)
            

def drawPieces(screen ,board):   
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece] , pg.Rect(col*SQR , row*SQR , SQR , SQR))

if __name__ == "__main__" :
    main()