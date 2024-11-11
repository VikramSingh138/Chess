'''
MAIN FILE : To handle user moves ( input ) and display the Output
'''

import pygame as pg
import ChessEngine
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = HEIGHT = 512
DIMENSION = 8
SQR = HEIGHT // DIMENSION # 8 x 8 square total to be made 

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

    while running : 
        for e in pg.event.get() : 
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN :
                location = pg.mouse.get_pos() #x, y
                col = location[0] // SQR
                row = location[1] // SQR

                if sqrSelected == (row , col) : 
                    sqrSelected = ()
                    #undoing the previous click if clicked twice on same sqr
                    playerClicks = []
                else:
                    sqrSelected = (row ,col)
                    playerClicks.append(sqrSelected) 
                    #append for both first and second clicks
                if len(playerClicks) == 2 : 
                    #second click done so now move
                    move = ChessEngine.Move(playerClicks[0] , playerClicks[1] , g_state.board)
                    print(move.getChessNotation())

                    if move in validMoves :     #check if Valid Move
                        g_state.make_Move(move) # making the move 
                        moveMade =True
                    
                    sqrSelected = () #reseting the player clicks after move is made
                    playerClicks = []

            elif e.type == pg.KEYDOWN : 
                if e.key == pg.K_z : # WHEN Z IS PRESSED 
                    g_state.undo_Move()
                    moveMade =True

            if moveMade :
                validMoves = g_state.getValidMoves()
                #new set of valid moves to be found after move is made
                moveMade = False

        draw_game_state(screen , g_state)
        clock.tick(MAX_FPS)
        pg.display.flip()

'''
DRAWING THE GAME BOARD AND PIECES
'''

def draw_game_state(screen , g_state) :
    drawBoard(screen)
    drawPieces(screen , g_state.board)


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