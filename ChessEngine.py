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

        self.moveFunctions = {
            'P' : self.getPawnMoves,
            'R' : self.getRookMoves,
            'N' : self.getKnightMoves,
            'B' : self.getBishopMoves,
            'Q' : self.getQueenMoves,
            'K' : self.getKingMoves,
        }

        self.whitemove = True
        self.movelogs = []

    '''
    TAKES START AND END POSITIONS TO MAKE MOVE
    DOESN'WORK FOR CASTLING , PAWN PROMOTION , EN PASSANT 
    '''
    def make_Move(self , move) : 
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol]     = move.pieceMoved
        self.movelogs.append(move)  #pushing to move log
        self.whitemove = not self.whitemove

    def undo_Move(self) : 
        if len(self.movelogs) != 0 :  # Shouldn't be the first move to undo
            move = self.movelogs.pop() #storing the last move in this variable
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol]     = move.pieceCaptured
            self.whitemove = not self.whitemove
        
    '''
    All  moves considering checks
    '''

    def getValidMoves(self) :
        return self.getPossibleMoves()

    '''
    GET ALL POSSIBLE MOVES
    '''

    def getPossibleMoves(self) :
        moves = []

        for row in range(len(self.board)) :
            for col in range(len(self.board[row])) :
                if ( self.board[row][col][0] == 'w' and self.whitemove) or (self.board[row][col][0]=='b' and not self.whitemove):
                    #whites turn and white piece or black turn and black piece
                    #so we can move this piece if possible
                    
                    piece = self.board[row][col][1]

                    self.moveFunctions[piece](row , col , moves)
                    #calls the function from moveFunctions dictionary based on the piece

        return moves 
        #return all possible moves list at a particular game state


    '''
    PAWN MOVES
    '''

    def getPawnMoves(self , row , col , moves) :
        if self.whitemove :
            if self.board[row-1][col] == "--" :
                #one square forward 
                moves.append(Move((row,col) , (row-1 , col) , self.board))

                if row == 6 and self.board[row-2][col] == "--" : 
                    #double square move on first move 
                    moves.append(Move((row,col) , (row-2 , col) , self.board))
                    ''' Move ( startsqr , endsqr , board)'''

            if col-1 >= 0 :
                if self.board[row-1][col-1][0] == 'b' :
                    #enemy piece to capture
                    moves.append(Move((row,col) , (row-1 , col-1) ,self.board))
                
            if col+1 <= 7 :
                if self.board[row-1][col+1][0] == 'b' :
                    #enemy piece to capture
                    moves.append(Move((row,col) , (row-1 , col+1) ,self.board))

        else :
            if self.board[row+1][col] == "--" :
                moves.append(Move((row,col) , (row+1 , col) , self.board))

                if row==1 and self.board[row+2][col] == "--" :
                    moves.append(Move((row,col) , (row+2 , col) , self.board))

            if col-1 >= 0 :
                if self.board[row+1][col-1][0] == 'w' :
                    moves.append(Move((row,col) , (row+1 , col-1) ,self.board))

            if col+1 <= 7 :
                if self.board[row+1][col+1][0] == 'w' :
                    moves.append(Move((row,col) , (row+1 , col+1) ,self.board))

    '''
    ROOK MOVES
    '''
    
    def getRookMoves(self , row , col , moves) :
        directions = ((-1,0) , (0,-1) , (1, 0) , (0 , 1))
        
        enemy_Color = "b" if self.whitemove else "w"

        for d in directions:
            for i in range(1,8) :
                #EndRow and EndCol are decided by the direction 
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0<= endRow < 8 and 0 <= endCol < 8 :
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" :               #Empty Space
                        moves.append(Move((row, col) , (endRow , endCol) , self.board))
                    elif endPiece[0] == enemy_Color:
                        #Enemy Piece
                        moves.append(Move((row,col) , (endRow , endCol) , self.board))
                        break
                    else :
                        break # Own Piece
                else:
                    #OFF BOARD
                    break
                    
    '''
    QUEEN MOVES
    '''

    def getQueenMoves(self , row , col , moves) :
        self.getBishopMoves(row , col , moves)
        self.getBishopMoves(row , col , moves)
        #Abstraction 
    '''
    BISHOP MOVES
    '''

    def getBishopMoves(self , row , col , moves) :
        directions  = ((1,1) , (-1,-1) , (1,-1) , (-1,1))

        enemy_Color = "b" if self.whitemove else "w"

        for d in directions :
            for i in range(1,8) :
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0<= endRow < 8 and 0 <= endCol < 8 :
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" :
                        moves.append(Move((row, col) , (endRow , endCol) , self.board))
                    elif endPiece[0] == enemy_Color :
                        moves.append(Move((row,col) , (endRow , endCol) , self.board))
                        break
                    else : 
                        break
                else:
                    break

    '''
    KNIGHTS MOVE
    '''

    def getKnightMoves(self , row , col , moves) :
        knight_moves = ((-2,-1) , (-2 , 1) , (-1 , -2) , (-1 , 2) , (1,-2) , (1,2) , (2,-1) , (2,1))
        enemy_Color = "b" if self.whitemove else "w"
        for m in knight_moves :
            endRow = row + m[0]
            endCol = col + m[1]
            if 0<= endRow < 8 and 0 <= endCol < 8 :
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" :
                    moves.append(Move((row, col) , (endRow , endCol) , self.board))
                elif endPiece[0] == enemy_Color :
                    moves.append(Move((row,col) , (endRow , endCol) , self.board))
    
    '''
    KING MOVES
    '''

    def getKingMoves(self , row , col , moves) :
        directions = ((-1,0) , (0,-1) , (1, 0) , (0 , 1) , (1,1) , (-1,-1) , (1,-1) , (-1,1))

        enemy_Color = "b" if self.whitemove else "w"

        for d in directions :
            endRow = row + d[0]
            endCol = col + d[1]

            if 0<=endRow < 8 and 0 <= endCol < 8 :
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" :
                    moves.append(Move((row,col) , (endRow , endCol) , self.board))
                elif endPiece[0] == enemy_Color :
                    moves.append(Move((row , col) , (endRow , endCol) , self.board))
        

'''
MOVE CLASS TO HANDLE ALL MOVES
'''
class Move():

    ranks_To_Rows = {
        "1" : 7 ,
        "2" : 6 ,
        "3" : 5 ,
        "4" : 4 ,
        "5" : 3 ,
        "6" : 2 ,
        "7" : 1 ,
        "8" : 0
    }

    rows_To_Ranks = {
        v:k for k , v in ranks_To_Rows.items()
    }
    #reverses the dictionary KEY , VAL pair to VAL , KEY pair 

    files_To_Cols = {
        "a" : 0,
        "b" : 1,
        "c" : 2,
        "d" : 3,
        "e" : 4,
        "f" : 5,
        "g" : 6,
        "h" : 7
    }

    cols_To_Files = {
        v : k for k,v in files_To_Cols.items()
    }
    #reverses the dictionary KEY , VAL pair to VAL , KEY pair 

    def __init__(self , startsqr , endsqr , board ):
        self.startRow = startsqr[0] 
        self.startCol = startsqr[1]
        self.endRow   = endsqr[0]
        self.endCol   = endsqr[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.MoveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        # print(self.MoveID)
        ''' MOVE ID TO UNIQUELY IDENTIFY EACH 
            MOVE IN THE GAME STATE '''

    def __eq__(self , other) :
        if isinstance(other , Move):
            return self.MoveID == other.MoveID
        return False
    
    def getChessNotation(self) :
        return self.getRankFile(self.startRow , self.startCol) + self.getRankFile(self.endRow , self.endCol)
    
    def getRankFile(self , row , col) :
        return self.cols_To_Files[col] + self.rows_To_Ranks[row]
    
