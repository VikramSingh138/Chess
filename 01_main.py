'''
MAIN FILE : To handle user moves ( input ) and display the Output
'''

import pygame as pg
import ChessEngine
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

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH , HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    g_state = ChessEngine.GameState()
    validMoves = g_state.getValidMoves()
    moveMade = False #track if a move is made

    loadimages()    #done once only
    running = True

    sqrSelected =  () #tuplpe to keep track of the selected sqr by the user
                      #Keeps track of last click of the user
    playerClicks = [] #Keeps tracks of the Users Initial and final clicks
    gameOver = False

    # while running : 
    #     for e in pg.event.get() : 
    #         if e.type == pg.QUIT:
    #             running = False
    #         elif e.type == pg.MOUSEBUTTONDOWN :
    #             location = pg.mouse.get_pos() #x, y
    #             col = location[0] // SQR
    #             row = location[1] // SQR

    #             if sqrSelected == (row , col) : 
    #                 sqrSelected = ()
    #                 #undoing the previous click if clicked twice on same sqr
    #                 playerClicks = []
    #             else:
    #                 sqrSelected = (row ,col)
    #                 playerClicks.append(sqrSelected) 
    #                 #append for both first and second clicks
    #             if len(playerClicks) == 2 : 
    #                 #second click done so now move
    #                 move = ChessEngine.Move(playerClicks[0] , playerClicks[1] , g_state.board)
    #                 print(move.getChessNotation())
                    
    #                 for i in range(len(validMoves)) :
    #                     if move == validMoves[i] :     #check if Valid Move
    #                         g_state.make_Move(validMoves[i]) # making the move 
    #                         moveMade =True
    #                         sqrSelected = () #reseting the player clicks after move is made
    #                         playerClicks = []
                    
    #                 if not moveMade :
    #                     playerClicks = [sqrSelected]

    #         elif e.type == pg.KEYDOWN : 
    #             if e.key == pg.K_z : # WHEN Z IS PRESSED 
    #                 g_state.undo_Move()
    #                 moveMade =True

    #         if moveMade :
    #             validMoves = g_state.getValidMoves()
    #             #new set of valid moves to be found after move is made
    #             moveMade = False

    #     draw_game_state(screen , g_state)
    #     clock.tick(MAX_FPS)
    #     pg.display.flip()
    while running: 
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN and not moveMade:
                if not gameOver :
                    location = pg.mouse.get_pos()  # x, y
                    col = location[0] // SQR
                    row = location[1] // SQR

                    if sqrSelected == (row, col):
                        # Undo the previous click if clicked twice on the same square
                        sqrSelected = ()
                        playerClicks = []
                    else:
                        sqrSelected = (row, col)
                        playerClicks.append(sqrSelected)

                    if len(playerClicks) == 2:  # After second click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], g_state.board)
                        print(move.getChessNotation())

                        for validMove in validMoves:
                            if move == validMove:
                                g_state.make_Move(validMove)  # Make the move
                                moveMade = True
                                sqrSelected = ()
                                playerClicks = []
                                break  # Prevent additional moves before toggling whitemove
                        
                        if not moveMade:
                            playerClicks = [sqrSelected]

                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_z:  # Undo move with "Z"
                        g_state.undo_Move()
                        moveMade = True
                    
                    # Resetting the board with R
                    if e.key == pg.K_r:
                        g_state = ChessEngine.GameState()
                        validMoves = g_state.getValidMoves()
                        sqrSelected = ()
                        playerClicks = []
                        moveMade = False
                        # undoing all the flags and resetting everything

        if moveMade:
            validMoves = g_state.getValidMoves()  # Update valid moves
            moveMade = False

        draw_game_state(screen, g_state , validMoves , sqrSelected)

        if g_state.CheckMate:
            gameOver = True
            if g_state.whitemove :
                drawText(screen , 'BLACK WINS BY CHECKMATE')
            else:
                drawText(screen , 'WHITE WINS BY CHECKMATE')
        elif g_state.StaleMate:
            gameOver = True
            drawText(screen , 'STALEMATE')

        clock.tick(MAX_FPS)
        pg.display.flip()


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