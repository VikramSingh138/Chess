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
        self.WhiteKing = (7,4)
        self.BlackKing = (0,4)
        self.CheckMate = False
        self.StaleMate = False
        self.incheck = False
        self.pins = []
        self.checks = []
        self.EnPassant_Possible = () #coords of possible enpassant move

    '''
    TAKES START AND END POSITIONS TO MAKE MOVE
    DOESN'WORK FOR CASTLING , PAWN PROMOTION , EN PASSANT 
    '''
    def make_Move(self , move) : 
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol]     = move.pieceMoved
        self.movelogs.append(move)  #pushing to move log

        # Update King Move
        if move.pieceMoved == "wK" : 
            self.WhiteKing = (move.endRow , move.endCol)
        elif move.pieceMoved == "bK" :
            self.BlackKing = (move.endRow , move.endCol)

        self.whitemove = not self.whitemove

        if move.isPawnPromotion :
            #make by default queen
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

        #En-Passant 
        if move.isEnPassant : 
            self.board[move.startRow][move.endCol] = "--" #captring enemy pawn
        
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2 :
            self.EnPassant_Possible = ((move.startRow + move.endRow)//2 , move.startCol)
        else :
            self.EnPassant_Possible = ()


    '''
    Undoing the Previous Move made
    '''

    def undo_Move(self) : 
        if len(self.movelogs) != 0 :  # Shouldn't be the first move to undo
            move = self.movelogs.pop() #storing the last move in this variable
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol]     = move.pieceCaptured

            # Update King Move
            if move.pieceMoved == "wK" : 
                self.WhiteKing = (move.startRow , move.startCol)
            elif move.pieceMoved == "bK" :
                self.BlackKing = (move.startRow , move.startCol)

            self.whitemove = not self.whitemove

        if move.isEnPassant : 
            self.board[move.endRow][move.endCol] = '--'
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.EnPassant_Possible = (move.endRow , move.endCol)

        #undo the 2 square pawn moved
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2 :
            self.EnPassant_Possible = ()
        
    '''
    All  moves considering checks
    1) Generate Valid Moves 
    2) Make Move
    3) Generate Opponents Moves
    4) See if Opponents Move attacks king
    5) If Attack King then Not Valid
    '''

    def getValidMoves(self) :
        # moves = self.getPossibleMoves()

        # for i in range(len(moves)-1 , -1 , -1) :
        #     self.make_Move(moves[i])
        #     # made a move 
        #     self.whitemove = not self.whitemove
        #     # going to check if it's causes check on king
        #     if self.In_Check() : 
        #         moves.remove(moves[i])
            
        #     self.whitemove = not self.whitemove
        #     # undoing the move after checking
        #     self.undo_Move()

        # if len(moves) == 0 :
        #     # CheckMate or Stalemate
        #     if self.In_Check() :
        #         self.CheckMate = True
        #     else :
        #         self.StaleMate = True
        # else :
        #     self.CheckMate = False
        #     self.StaleMate = False

        # return moves

        # moves = []
        # self.inCheck, self.pins , self.checks = self.CheckPinsAndChecks()

        # if self.whitemove : 
        #     kingRow = self.WhiteKing[0]
        #     kingCol = self.WhiteKing[1]

        # else :
        #     kingRow = self.BlackKing[0]
        #     kingCol = self.BlackKing[1]

        # if self.inCheck :
        #     if len(self.checks) == 1 :
        #         # Single check applied

        #         moves = self.getPossibleMoves()
        #         check = self.checks[0] #info about the check

        #         checkRow = check[0]
        #         checkCol = check[1]

        #         piece_Checking = self.board[checkRow][checkCol]
        #         Valid_Sqrs = []

        #         if piece_Checking[1] == 'N' :
        #             Valid_Sqrs = [(checkRow , checkCol)]
        #             '''
        #             When Knight is Checking we can't Block  , Only Capture it is Option
        #             so anyother piece must Capture the knight and move to same position
        #             '''

        #         else :
        #             # Not a Knight Checking
        #             for i in range(1 , 8) :
        #                 Valid_Sqr = (kingRow + check[2] * i , kingCol + check[3] * i)
        #                 # checks[2] and checks[3] give the direction of the incoming check 
        #                 Valid_Sqrs.append(Valid_Sqr)

        #                 if Valid_Sqr[0] == checkRow and Valid_Sqr[1] == checkCol :
        #                     break
        #                 ''' we moved to the piece from where check was coming and found no valid move to block in between so break'''
                
        #         for i in range(len(moves) -1 , -1 , -1) :
        #             if moves[i].pieceMoved[1] != 'K' :
        #                 # if King is not moved then the piece moved must go one of the Valid Squares which were found earlier
        #                 # if not then remove that move
        #                 if not (moves[i].endRow , moves[i].endCol) in Valid_Sqrs :
        #                     moves.remove(moves[i])

        #     else :
        #         self.getKingMoves(kingRow , kingCol , moves)
        # else :
        #     moves = self.getPossibleMoves()

        # return moves

        temp_Enpassant = self.EnPassant_Possible

        moves = []
        self.inCheck, self.pins, self.checks = self.CheckPinsAndChecks()  # Determine if the king is in check

        if self.whitemove:
            kingRow, kingCol = self.WhiteKing
        else:
            kingRow, kingCol = self.BlackKing

        if self.inCheck:
            if len(self.checks) == 1:
                # Single check: other pieces can block/capture or the king can move
                moves = self.getPossibleMoves()  # Get all possible moves
                check = self.checks[0]  # Information about the check
                checkRow, checkCol, checkDirRow, checkDirCol = check

                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []  # Squares that can block the check

                # If the checking piece is a knight, it must be captured
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    # Generate squares along the check path (including the checking piece)
                    for i in range(1, 8):
                        validSquare = (kingRow + checkDirRow * i, kingCol + checkDirCol * i)
                        validSquares.append(validSquare)
                        if validSquare == (checkRow, checkCol):  # Stop at the checking piece
                            break

                # Remove invalid moves
                for i in range(len(moves) - 1, -1, -1):  # Traverse in reverse to safely modify the list
                    move = moves[i]
                    if move.pieceMoved[1] != 'K':  # Not a king move
                        if (move.endRow, move.endCol) not in validSquares:
                            moves.remove(move)
                # Add king moves to escape check
                self.getKingMoves(kingRow, kingCol, moves)
            else:
                # Double check: only king moves are valid
                moves = []
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            # No check: all possible moves are valid
            moves = self.getPossibleMoves()

            # Filter king moves to ensure the king doesn't move into check
            kingMoves = []
            self.getKingMoves(kingRow, kingCol, kingMoves)
            moves = [move for move in moves if move.pieceMoved[1] != 'K'] + kingMoves

        # Check for checkmate or stalemate
        if len(moves) == 0:
            if self.inCheck:
                self.CheckMate = True
            else:
                self.StaleMate = True
        else:
            self.CheckMate = False
            self.StaleMate = False

        self.EnPassant_Possible = temp_Enpassant

        return moves

    

    '''
    Function to check all possible pins and checks for a king at any moment
    '''

    def CheckPinsAndChecks(self) :
        pins = []
        checks = []
        inCheck = False

        if self.whitemove : 
            enemy_Color = "b"
            own_Color = "w"
            startRow = self.WhiteKing[0]
            startCol = self.WhiteKing[1]
        else :
            enemy_Color = "w"
            own_Color = "b"
            startRow = self.BlackKing[0]
            startCol = self.BlackKing[1]

        directions = ((-1,0) , (0,-1) , (1, 0) , (0 , 1) , (1,1) , (-1,-1) , (1,-1) , (-1,1))

        for j in range (len(directions)) :
            d = directions[j]
            possiblePin = ()

            for i in range(1,8) : 
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0<= endRow < 8 and 0 <= endCol < 8 :
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == own_Color and endPiece[1] != 'K' :
                        if possiblePin == () : 
                            #first piece of the same color which can be pinned
                            possiblePin = (endRow , endCol , d[0] , d[1])
                            '''
                            we save the LOCATION of PIECE which can be pinned as well as the direction
                            in which it can be pinned
                            '''
                        else :
                            # second piece of same color
                            # can't pin the king 
                            break
                    
                    elif endPiece[0] == enemy_Color : 
                        piece_type = endPiece[1]

                        if (0<= j <= 3 and piece_type == 'R') or \
                        (4 <= j <= 7 and piece_type == 'B') or \
                        (i == 1 and piece_type == 'P' and ((enemy_Color == 'w' and 6<= j <= 7) or (enemy_Color == 'b' and 4<= j <= 5))) or \
                        (piece_type == 'Q') or (i== 1 and piece_type == 'K') :
                            # if the piece is in front of the king and it's a rook or queen or
                            # if it's a pawn and it's moving diagonally
                            # we can pin the king
                            if possiblePin == () :
                                ''' Not a Pin but a Check '''
                                inCheck = True
                                checks.append((endRow , endCol , d[0] , d[1]))
                                break
                            else :
                                '''
                                Piece Blocking Check
                                '''
                                pins.append(possiblePin)
                                break
                        else :
                            '''
                            Enemy Piece not applying Check
                            '''
                            break
                else :
                    break
                '''
                Piece is Off Board
                '''
        '''
        For Knights
        '''
        knight_moves = ((-2,-1) , (-2 , 1) , (-1 , -2) , (-1 , 2) , (1,-2) , (1,2) , (2,-1) , (2,1))

        for d in knight_moves : 
            endRow = startRow + d[0]
            endCol = startCol + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8 :
                # On Board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemy_Color  and endPiece[1] == 'N' :
                    inCheck = True
                    checks.append((endRow , endCol , d[0] , d[1]))
        return inCheck , pins , checks

    '''
    CHECK FOR CHECKS IN CURRENT GAME STATE
    '''
    def In_Check(self) :
        if self.whitemove :
            return self.square_under_attack(self.WhiteKing[0] , self.WhiteKing[0]) 
        else :
            return self.square_under_attack(self.BlackKing[0] , self.BlackKing[1])

    ''' 
    IF ENEMY CAN ATTACK ( ROW , COL )
    '''

    def square_under_attack(self , row , col) :
        self.whitemove = not self.whitemove
        moves = self.getPossibleMoves()
        self.whitemove = not self.whitemove
        for move in moves :
            if move.endRow == row and move.endCol == col :
                return True
        return False

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
        
        piecePinned = False
        pin_Direction = ()

        for i in range(len(self.pins) -1 , -1 ,-1) :
            if self.pins[i][0] == row and self.pins[i][1] == col :
                piecePinned = True
                pin_Direction = (self.pins[i][2] , self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
            
        ''' Above part checks if the piece is pinned '''

        if self.whitemove :
            if self.board[row-1][col] == "--" :
                #one square forward 
                if not piecePinned or pin_Direction == (-1 , 0) : 
                    moves.append(Move((row,col) , (row-1 , col) , self.board))

                    if row == 6 and self.board[row-2][col] == "--" : 
                        #double square move on first move 
                        moves.append(Move((row,col) , (row-2 , col) , self.board))
                        ''' Move ( startsqr , endsqr , board)'''

            if col-1 >= 0 :
                if self.board[row-1][col-1][0] == 'b' :
                    #enemy piece to capture
                    if not piecePinned or pin_Direction == (-1 , -1) : 
                        moves.append(Move((row,col) , (row-1 , col-1) ,self.board))

                elif (row -1 , col -1) == self.EnPassant_Possible :
                    moves.append(Move((row,col) , (row-1 , col-1) ,self.board , isEnpassant =True))
                
            if col+1 <= 7 :
                if self.board[row-1][col+1][0] == 'b' :
                    #enemy piece to capture
                    if not piecePinned or pin_Direction == (-1 , 1) : 
                        moves.append(Move((row,col) , (row-1 , col+1) ,self.board))
                elif (row -1 , col +1) == self.EnPassant_Possible :
                    moves.append(Move((row,col) , (row-1 , col+1) ,self.board , isEnpassant =True))

        else :
            if self.board[row+1][col] == "--" :
                if not piecePinned or pin_Direction == (1 , 0) : 
                    moves.append(Move((row,col) , (row+1 , col) , self.board))

                    if row==1 and self.board[row+2][col] == "--" :
                        moves.append(Move((row,col) , (row+2 , col) , self.board))

            if col-1 >= 0 :
                if self.board[row+1][col-1][0] == 'w' :
                    if not piecePinned or pin_Direction == (1 , -1) : 
                        moves.append(Move((row,col) , (row+1 , col-1) ,self.board))
                elif (row +1 , col -1) == self.EnPassant_Possible :
                    moves.append(Move((row,col) , (row+1 , col-1) ,self.board , isEnpassant =True))

            if col+1 <= 7 :
                if self.board[row+1][col+1][0] == 'w' :
                    if not piecePinned or pin_Direction == (1 , 1) : 
                        moves.append(Move((row,col) , (row+1 , col+1) ,self.board))
                elif (row +1 , col +1) == self.EnPassant_Possible :
                    moves.append(Move((row,col) , (row+1 , col+1) ,self.board , isEnpassant =True))

    '''
    ROOK MOVES
    '''
    
    def getRookMoves(self , row , col , moves) :
        
        piecePinned = False
        pin_Direction = ()

        for i in range(len(self.pins) -1 , -1 ,-1) :
            if self.pins[i][0] == row and self.pins[i][1] == col :
                piecePinned = True
                pin_Direction = (self.pins[i][2] , self.pins[i][3])
                if self.board[row][col][1] != 'Q' :
                    self.pins.remove(self.pins[i])
                break
            
        ''' Above part checks if the piece is pinned '''

        directions = ((-1,0) , (0,-1) , (1, 0) , (0 , 1))
        
        enemy_Color = "b" if self.whitemove else "w"

        for d in directions:
            for i in range(1,8) :
                #EndRow and EndCol are decided by the direction 
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0<= endRow < 8 and 0 <= endCol < 8 :
                    if not piecePinned == d or pin_Direction == (-d[0] , -d[1]) : 
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
        self.getRookMoves(row , col , moves)
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

        piecePinned = False
        pin_Direction = ()

        for i in range(len(self.pins) -1 , -1 ,-1) :
            if self.pins[i][0] == row and self.pins[i][1] == col :
                piecePinned = True
                pin_Direction = (self.pins[i][2] , self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2,-1) , (-2 , 1) , (-1 , -2) , (-1 , 2) , (1,-2) , (1,2) , (2,-1) , (2,1))
        enemy_Color = "b" if self.whitemove else "w"
        for m in knight_moves :
            endRow = row + m[0]
            endCol = col + m[1]
            if 0<= endRow < 8 and 0 <= endCol < 8 :
                if not piecePinned :
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" :
                        moves.append(Move((row, col) , (endRow , endCol) , self.board))
                    elif endPiece[0] == enemy_Color :
                        moves.append(Move((row,col) , (endRow , endCol) , self.board))
    
    '''
    KING MOVES
    '''

    # def getKingMoves(self , row , col , moves) :
    #     rowMoves = (-1 , -1 , -1 , 0 , 0 , 1 , 1, 1)
    #     colMoves = (-1 , 0 , 1 , -1 , 1 , -1 , 0 , 1)

    #     enemy_Color = "b" if self.whitemove else "w"

    #     for i in range(8) : 
    #         endRow = row + rowMoves[i]
    #         endCol = col + colMoves[i]

    #         if 0<= endRow < 8 and 0<=endCol < 8 :
    #             endPiece = self.board[endRow][endCol]
    #             if endPiece[0] == enemy_Color :

    #                 if enemy_Color == 'b' : 
    #                     self.WhiteKing = (endRow , endCol)
    #                 else : 
    #                     self.BlackKing = (endRow , endCol)
                    
    #                 incheck , pins , checks = self.CheckPinsAndChecks()

    #                 if not incheck :
    #                     moves.append(Move((row , col) , (endRow , endCol) , self.board))

    #                 if enemy_Color == 'b' :
    #                     self.WhiteKing = (row , col)
    #                 else :
    #                     self.BlackKing = (row , col)

    def getKingMoves(self, row, col, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)

        enemy_Color = "b" if self.whitemove else "w"

        for i in range(8):
            endRow = row + rowMoves[i]
            endCol = col + colMoves[i]

            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if within board boundaries
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ("w" if self.whitemove else "b"):  # Ensure square is not occupied by allied piece
                    # Temporarily move the king to this square
                    if self.whitemove:
                        self.WhiteKing = (endRow, endCol)
                    else:
                        self.BlackKing = (endRow, endCol)

                    # Check if the king would be in check
                    incheck, pins, checks = self.CheckPinsAndChecks()

                    if not incheck:  # If not in check, add the move
                        moves.append(Move((row, col), (endRow, endCol), self.board))

                    # Restore the king's original position
                    if self.whitemove:
                        self.WhiteKing = (row, col)
                    else:
                        self.BlackKing = (row, col)


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

    def __init__(self , startsqr , endsqr , board , isEnpassant = False):
        self.startRow = startsqr[0] 
        self.startCol = startsqr[1]
        self.endRow   = endsqr[0]
        self.endCol   = endsqr[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.isPawnPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0 ) or (self.pieceMoved == 'bP' and self.endRow == 7 ):
            #pawn reached opposite end of board
            self.isPawnPromotion =True
        
        self.isEnPassant = isEnpassant
        if self.isEnPassant:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

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
    
