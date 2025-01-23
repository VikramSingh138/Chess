import random as rand

piece_val = {"K" : 0 , 
             "Q" : 9 ,
             "N" : 3 ,
             "B" : 3,
             "P" : 1 , 
             "R" : 5}

CHECKMATE = 1000
STALEMATE = 0
'''
if +ve Score of Board then White is Winning
if -ve Score of Board then Black is Winning
'''

def findRandomMove(validMoves) :
    rand.randint(0 , len(validMoves) - 1)
    return validMoves[rand.randint(0 , len(validMoves) - 1)]


'''
MINIMISING THE OPP SCORE 
MAXIMISING OWN SCORE
'''
def findBestMove(g_state , validMoves):
    # initially the worst case for black 
    whose_turn = 1 if g_state.whitemove else -1
    opp_minmax_score = CHECKMATE
    bestplayerMove = None
    rand.shuffle(validMoves)
    '''
    OUTER LOOP FOR MY OWN MOVE
    '''

    for playerMove in validMoves :
        g_state.make_Move(playerMove)
        opp_moves  = g_state.getValidMoves()
        
        if g_state.StaleMate :
            opp_maxscore = STALEMATE
        elif g_state.CheckMate :
            opp_maxscore = -CHECKMATE
        else:
            '''
            THE INNER LOOP IS GOING TO FIND THE BEST MOVE FOR OPPONENT AFTER
            MY OWN MOVE IS BEING MADE
            '''
            opp_maxscore = -CHECKMATE
            for opp_move in opp_moves :
                g_state.make_Move(opp_move)

                g_state.getValidMoves()

                if g_state.CheckMate : 
                    score = CHECKMATE
                elif g_state.StaleMate : 
                    score = STALEMATE
                else :
                    score = -whose_turn * scoreMaterial(g_state , g_state.board)
                
                if (score > opp_maxscore) :
                    opp_maxscore = score

                g_state.undo_Move()
            '''
            IF THE OPPONENTS NEW BEST MOVE IS LESS THAN THE 
            PREVIOUS BEST MOVE THEN THAT'S MY BEST MOVE
            '''
        if opp_minmax_score > opp_maxscore : 
            opp_minmax_score = opp_maxscore
            bestplayerMove = playerMove
            
        g_state.undo_Move()  
        
    return bestplayerMove

'''
SCORING ON MATERIAL
'''
def scoreMaterial(g_state , board) :
    score = 0
    for row in board : 
        for sqr in row :
            if sqr[0] == 'w' :
                score += piece_val[sqr[1]]
            elif sqr[0] == 'b' :
                score -= piece_val[sqr[1]]
    return score

'''
MINMAX USING RECURSION
'''
DEPTH = 3
    
# def scoreBoard(g_state) : 

#     if g_state.CheckMate : 
#         if g_state.whitemove :
#             return -CHECKMATE
#         #Black Wins

#         else : 
#             return CHECKMATE
#         #White Wins

#     elif g_state.StaleMate : 
#         return STALEMATE

#     score = 0
#     for row in g_state.board : 
#         for sqr in row :
#             if sqr[0] == 'w' :
#                 score += piece_val[sqr[1]]
#             elif sqr[0] == 'b' :
#                 score -= piece_val[sqr[1]]
#     return score 

# def minmax_helper(g_state , validMoves) :
#     global nextMove 
#     nextMove = None
#     findMinmaxMove(g_state , validMoves , DEPTH , g_state.whitemove)
#     return nextMove   

# def findMinmaxMove(g_state , validMoves , depth , whitemove) :
#     global nextMove
#     if depth == 0:
#         #evaluate the board now max depth is reached
#         return scoreBoard(g_state)
    
#     if whitemove : 
#         #Maximise the score
#         maxscore = -CHECKMATE
#         for move in validMoves : 
#             g_state.make_Move(move)
#             nextMoves = g_state.getValidMoves()
#             score = findMinmaxMove(g_state , nextMoves , depth -1  , not whitemove)
#             if score > maxscore : 
#                 maxscore = score
#                 if depth == DEPTH: 
#                     nextMove = move
#             g_state.undo_Move()
#         return maxscore

#     else :
#         minscore = CHECKMATE
#         for move in validMoves : 
#             g_state.make_Move(move)
#             nextMoves = g_state.getValidMoves()
#             score = findMinmaxMove(g_state , nextMoves , depth - 1 , not whitemove)
#             if score < minscore : 
#                 minscore = score
#                 if depth == DEPTH :
#                     nextMove = move
#                 g_state.undo_Move()
#         return minscore

def scoreBoard(g_state):
    if g_state.CheckMate:
        if g_state.whitemove:
            return -CHECKMATE  # Black wins
        else:
            return CHECKMATE  # White wins
    elif g_state.StaleMate:
        return STALEMATE

    score = 0
    for row in g_state.board:
        for sqr in row:
            if sqr[0] == 'w':
                score += piece_val.get(sqr[1], 0)  # Avoid KeyError
            elif sqr[0] == 'b':
                score -= piece_val.get(sqr[1], 0)
    return score


def minmax_helper(g_state, validMoves, depth):
    bestMove, _ = findMinmaxMove(g_state, validMoves, depth, g_state.whitemove)
    return bestMove


def findMinmaxMove(g_state, validMoves, depth, whitemove):
    if depth == 0 or g_state.CheckMate or g_state.StaleMate:
        return None, scoreBoard(g_state)

    if whitemove:  # Maximize
        maxScore = -CHECKMATE
        bestMove = None
        for move in validMoves:
            g_state.make_Move(move)
            nextMoves = g_state.getValidMoves()
            _, score = findMinmaxMove(g_state, nextMoves, depth - 1, not whitemove)
            if score > maxScore:
                maxScore = score
                bestMove = move
            g_state.undo_Move()
        return bestMove, maxScore
    else:  # Minimize
        minScore = CHECKMATE
        bestMove = None
        for move in validMoves:
            g_state.make_Move(move)
            nextMoves = g_state.getValidMoves()
            _, score = findMinmaxMove(g_state, nextMoves, depth - 1, not whitemove)
            if score < minScore:
                minScore = score
                bestMove = move
            g_state.undo_Move()
        return bestMove, minScore
    
'''
NEGA MAX AND ALPHA BETA PRUINING
'''


