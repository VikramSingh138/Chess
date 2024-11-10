'''
Stores the current Game State
Keeps Move Logs
'''

class GameState():
    def __init__(self):
        #BOARD : 8 x 8 2-D LIST 
        # COLOR : b , w
        # PIECE TYPE : R , N , B , Q, K , P , -- (No-Piece)
        self.board = [
            ["bR" , "bN" , "bB" , "bQ" , "bK" , "bB" , "bN" , "bR"],
            ["bP" , "bP" , "bP" , "bP" , "bP" , "bP" , "bP" , "bP"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["wP" , "wP" , "wP" , "wP" , "wP" , "wP" , "wP" , "wP"],
            ["wR" , "wN" , "wB" , "wQ" , "wK" , "wB" , "wN" , "wR"],
        ]

        self.whitemove = True
        self.movelogs = []