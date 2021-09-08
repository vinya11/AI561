import gameDesc
import piece
import heapq
import collections

class Optimize:
    def __init__(self,board,player):
        self.board = board
        self.player = player

    def count_checkers(self,board):
        """Call this function before and after resultState to check for "making a king" and "number of captures/captured"""
        blackCount=0
        blackKings=0
        whiteCount=0
        whiteKings=0
        for r in board:
            blackCount+=r.count('b')
            blackKings+=r.count('B')
            whiteCount+=r.count('w')
            whiteKings+=r.count('W')
        return blackCount,blackKings,whiteCount,whiteKings


    

    def get_state_value(self,state,player,min_move):
        blackCount,blackKings,whiteCount,whiteKings = self.count_checkers(state)
        if player == 'white':
            min_move = 1.5*(12-blackCount) - ((12-whiteCount)) + 2*(whiteKings-blackKings)
        else:
            min_move = 1.5*(12-whiteCount) - ((12-blackCount)) + 2*(blackKings-whiteKings)
        
        return min_move
    
    def check_king_move(self,player,state,valid_moves):
        king_move=collections.defaultdict(list)
        game_object = gameDesc.Checkers(state)
        depth =0
        #king move
        for key,paths in valid_moves.items():
            for path in paths:
                #1.check king move
                if type(path) == tuple:
                    if player == 'black':
                        if path[0] == 7 and not game_object.is_king(piece.Piece(key,'b')):
                            king_move[key].append(path)
                            depth = 1
                            
                    else:
                        if path[0] == 0 and not game_object.is_king(piece.Piece(key,'w')):
                            king_move[key].append(path)
                            depth = 1

        return king_move,depth


        #getting more captures: more priority
        #getting coin captured : less priority
    def check_jump(self,is_jump,valid_moves,player,state,v):
        jump_pos = list()
        jump_list = collections.defaultdict(list)
        depth = 0
        
        game_object = gameDesc.Checkers(state)
        #prioritize the jumps. that is if jump exists for any piece, choose between the jumps
        for pos,flag in is_jump.items():
            if flag:
                jump_pos.append(pos)
        
        
        for key,paths in valid_moves.items():
            if key in jump_pos:
                jump_list[key]=paths
        #if only one jump exists, no need to look ahead
        if len(jump_pos) == 1:
            depth = 2
        #if few jump exists, choose between the jumps by looking ahead only 4 moves
        elif len(jump_pos) >1:
            depth = 4
        return jump_pos,jump_list,depth
    





                    

