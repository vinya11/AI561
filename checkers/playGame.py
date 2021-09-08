import random
import numpy as np
from copy import deepcopy
import json

import gameInput
import optimize
import alphabeta
import gameDesc
import piece


    
def playGame():
    board,gameType,pieceColor,timeInSecs,blackCount,blackKings,whiteCount,whiteKings = gameInput.getInput()
    checkers = gameDesc.Checkers(board)
    player = 'black'
    state = deepcopy(checkers.board)
    select_move = list()
    player = pieceColor.lower()
    if gameType.lower() == 'single':
        black_moves,white_moves,is_jump = checkers.all_moves(state,player)
        if not white_moves and not black_moves:
            return checkers.board
        for key,value in is_jump.items():
            if value == True:
                if player == 'black':
                    select_move = black_moves[key]
                    init = key
                else:
                    select_move = white_moves[key]
                    init = key
        
        if select_move:
            jump=True
            path = random.choice(select_move)
            result_board,old_board = checkers.resultState(state,path,piece.Piece(init,state[init[0]][init[1]]),jump=True)
                
        else:
            jump=False
            if player == 'black':
                init,select_move = random.choice(list(black_moves.items()))
            else:
                init,select_move = random.choice(list(white_moves.items()))
            
            path = random.choice(select_move)
            result_board,old_board = checkers.resultState(state,path,piece.Piece(init,state[init[0]][init[1]]))

    else:
   
        init_board = [['.', 'b', '.', 'b', '.', 'b', '.', 'b'], ['b', '.', 'b', '.', 'b', '.', 'b', '.'], ['.', 'b', '.', 'b', '.', 'b', '.', 'b'], ['.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.'], ['w', '.', 'w', '.', 'w', '.', 'w', '.'], ['.', 'w', '.', 'w', '.', 'w', '.', 'w'], ['w', '.', 'w', '.', 'w', '.', 'w', '.']]
        init_white = [['w', '.', 'w', '.', 'w', '.', 'w', '.'], ['.', 'w', '.', 'w', '.', 'w', '.', 'w'], ['w', '.', 'w', '.', 'w', '.', 'w', '.']]

        if state == init_board and player == 'black':
            init = (2,5)
            path = (3,4)
            jump = False
            #write original game time to file
            time = {
            "total_game_time": float(timeInSecs)
            }
            with open('playData.txt','w') as f:
                json.dump(time,f)
        elif state[5:] == init_white and player == 'white':
            if checkers.board[3][4] == 'b':
                white_moves = {(5,4):[(4,5)],(5,2):[(4,1)]}
                init,path  = random.choice(list(white_moves.items()))
                path=path[0]
            else:
                init = (5,2)
                path = (4,3)
            jump = False
            # write original game time to file
            time = {
            "total_game_time": float(timeInSecs)
            }
            with open('playData.txt','w') as f:
                json.dump(time,f)
        else:
            json_text = {"depth":{"MAX_DEPTH": 10,"MEDIUM_DEPTH": 7,"REGULAR_DEPTH" : 3,"JUMP_DEPTH" : 1}}
            max_depth = json_text["depth"]["MAX_DEPTH"]
            
            """calculating depth based on time"""
            with open('playData.txt','r') as f:
                time_data = json.load(f)
            total_game_time = time_data["total_game_time"]
            time_remaining = total_game_time-float(timeInSecs)
            opt = optimize.Optimize(board,player)
            bc,bk,wc,wk = opt.count_checkers(board)
            if 18 >=bc+bk+wc+wk >=6 or 1/3<=time_remaining/total_game_time <=2/3  :
                depth = json_text["depth"]["MEDIUM_DEPTH"]
            else:
                depth = json_text["depth"]["REGULAR_DEPTH"]
            
            #alpha beta pruning
            state,path,init,jump = alphabeta.alphaBeta(state,checkers,player,depth)
        
        result_board,old_state = checkers.resultState(checkers.board,path,piece.Piece(init,checkers.board[init[0]][init[1]]),jump)
        
    for r in result_board:
        print("".join(r))     
    if init in path:
        path.remove(init)
        path.reverse()
    gameInput.print_output(init,path,jump)
    
playGame()


