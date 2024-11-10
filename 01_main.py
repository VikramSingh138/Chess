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

    loadimages()
    running = True

    while running : 
        for e in pg.event.get() : 
            if e.type == pg.QUIT:
                running = False
        
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