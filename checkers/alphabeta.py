import numpy as np
import gameDesc
import piece
import optimize
import time
import random
import heapq
from copy import deepcopy
max_depth = 7
depth = max_depth
#TODO: modify such  that node selected is a best node from the actions
def alphaBeta(state,gameObject,player,depth):
    print(depth)
    v,init,path,is_jump = maxValue(state, np.NINF,np.Inf,gameObject,player,depth)
    return state,path,init,is_jump

def maxValue(state,alpha,beta,gameObject,player,depth):
    #get the result/score from the terminal function
    v =  np.NINF
    old_state =deepcopy(state)
    init_point = None
    path = None
    key = None
    jump_flag = False
    valid_moves = dict()
    min_move = np.NINF

    if player == 'white':
        opponent = 'black'
    else:
        opponent = 'white'
    opt = optimize.Optimize(state,player)
    if depth ==0:
    
        min_move = opt.get_state_value(state,player,min_move)
        return min_move,None,None,None
    
    result = gameObject.score(state,player)

    if result:
        return (result,None,None,None)
    else:
        
        color = gameObject.get_color(player)
        black_moves,white_moves,is_jump = gameObject.game_action(state,player)
        if player == 'black':
            valid_moves = black_moves
        else:
            valid_moves = white_moves
        """check for jumps"""
        jump_pos,jump_list,d = opt.check_jump(is_jump,valid_moves,player,state,v)
        if jump_pos:
            valid_moves = jump_list
            depth =d
        
        for key,values in valid_moves.items():
            #check the jump pos and give the result for each
            for value in values:
                player_piece = piece.Piece(key,color)
                new_state,old_state = gameObject.resultState(old_state,value,player_piece,is_jump[key])
                min_move,point,j,some_flag = minValue(new_state,alpha,beta,gameObject,opponent,depth-1)
    
                if min_move>v:
                    v=min_move
                    init_point = key
                    path = value
                    jump_flag = is_jump[key]
                if v>=beta:
                    return v,init_point,path,jump_flag
                alpha = max(v,alpha)
        
            
    return v,init_point,path,jump_flag


def minValue(state,alpha,beta,gameObject,player,depth):
    #get the result/score from the terminal function
    max_move = np.Inf
    v =  np.Inf
    old_state = deepcopy(state)
    init_point = None
    path =None
    jump_pos = list()
    jump_flag = False
    if player == 'white':
        opponent = 'black'
    else:
        opponent = 'white'
    opt = optimize.Optimize(state,player)
    if depth ==0:
        max_move = opt.get_state_value(state,opponent,max_move)
        return max_move,None,None,None
    result = gameObject.score(state,player)
    if result:
        return (result,0,0,0)
    else:
        black_moves,white_moves,is_jump = gameObject.game_action(state,player)
        color = gameObject.get_color(player)
        #prioritize the jumps. that is if jump exists for any piece, choose between the jumps
        
        if player == 'black':
            valid_moves = black_moves
        else:
            valid_moves = white_moves
        """check for jumps"""
        jump_pos,jump_list,d = opt.check_jump(is_jump,valid_moves,player,state,v)
        if jump_pos:
            valid_moves = jump_list
            depth = d
            
        for key,values in valid_moves.items():
            #check the jump pos and give the result for each
            for value in values:
                player_piece = piece.Piece(key,color)
                new_state,old_state = gameObject.resultState(old_state,value,player_piece,is_jump[key])
                max_move,point,j,some_flag= maxValue(new_state,alpha,beta,gameObject,opponent,depth-1)
                if max_move<v:
                    v=max_move
                    init_point = key
                    path = value
                    jump_flag = is_jump[key]
                if v<=alpha:
                    return v,init_point,path,jump_flag
                beta = min(v,beta)
    return v,init_point,path,jump_flag

