import gameInput
import itertools
import piece
import collections
import optimize
from copy import deepcopy
class Checkers:
    """Defining the board game checkers"""
    def __init__(self,board):
        """Pass the initial state of the board for each move"""
        self.board = board
        
    def opposite(self,color):
        if color.lower() == 'w':
            return 'b'
        elif color.lower() == 'b':
            return 'w'
        else:
            return None
    def get_color(self,player):
        if player == 'white':
            return 'w'
        else:
            return 'b'
    def is_king(self,piece,endx=None):
        if piece.king:
            return True
        if piece.color == 'B' or piece.color == "W":
            return True
        if piece.color == 'b' and endx == 7:
            return True
        elif piece.color == 'w' and endx == 0:
            return True
        return False
     
    def resultState(self,board,path,piece,jump=False):
        """resulting state of the board after a move. Called by alpha beta func for a valid move/path"""
        state = deepcopy(board)
        #print(f"#printing path {path}")
        if jump:
            for cell in range(len(path)-1,0,-1):
                
                removex,removey = tuple(map(lambda x: int(x/2), map(sum, zip(path[cell], path[cell-1]))))

                state[removex][removey] = '.'
        if type(path) == tuple:
            endx,endy = path
        else:
            endx,endy = path[0]
        # print(piece.color)
        if self.is_king(piece,endx) or state[piece.row][piece.col] == piece.color.upper():
            
            piece.color = piece.color.upper()
            piece.king = True
            
        state[endx][endy] = piece.color
        
        state[piece.row][piece.col] = '.'
        

        piece.row = endx
        piece.col = endy

        return state,board
    def is_right_jump_poss(self,board,r,c,step_count,color):
        if 0<=c<8 and 0<=r<8 and 0<=c+1<8 and 0<=r+step_count<8:
            if board[r+step_count][c+1].lower()== color.lower():
                if 0<=r+2*step_count<8 and 0<=c+2<8:
                    if board[r+2*step_count][c+2]=='.':
                        return True
        return False
    def is_left_jump_poss(self,board,r,c,step_count,color):
        if 0<=c<8 and 0<=r<8 and 0<=c-1<8 and 0<=r+step_count<8:
            if board[r+step_count][c-1].lower()== color.lower():
                if 0<=r+2*step_count<8 and 0<=c-2<8:
                
                    if board[r+2*step_count][c-2]=='.':
                        return True
        return False

    def right(self,board,r,c,multiple_jumps,single_moves,end_moves,step_count,color,king):
        """The right move by either black or white piece identified by step_count value. Called by func valid_moves"""
    
        if self.is_right_jump_poss(board,r,c,step_count,color):


            #remove r,c from multiple_jumps if it exists, since we are already adding r+2*step_count,c+2
            if (r,c) in end_moves:
                end_moves.remove((r,c))
            if (r+2*step_count,c+2) not in end_moves:
                end_moves.append((r+2*step_count,c+2))
            multiple_jumps[(r+2*step_count,c+2)].append((r,c))
            self.right(board,r+2*step_count,c+2,multiple_jumps,single_moves,end_moves,step_count,color,king)
            self.left(board,r+2*step_count,c+2,multiple_jumps,single_moves,end_moves,step_count,color,king)
            
           
        else:
            if 0<=c<8 and 0<=r<8 and 0<=c+1<8 and 0<=r+step_count<8:
                if board[r+step_count][c+1] == '.':
                    single_moves.append((r+step_count,c+1))
                
        return multiple_jumps,single_moves,end_moves

    def left(self,board,r,c,multiple_jumps,single_moves,end_moves,step_count,color,king):
        """The left move by either black or white piece identified by step_count value. Called by func valid_moves""" 
        
        if self.is_left_jump_poss(board,r,c,step_count,color):
            #remove r,c from multiple_jumps if it exists, since we are already adding r+2*step_count,c+2
            if (r,c) in end_moves:
                end_moves.remove((r,c))
            if (r+2*step_count,c-2) not in end_moves:
                end_moves.append((r+2*step_count,c-2))
            multiple_jumps[(r+2*step_count,c-2)].append((r,c))
            self.right(board,r+2*step_count,c-2,multiple_jumps,single_moves,end_moves,step_count,color,king)
            self.left(board,r+2*step_count,c-2,multiple_jumps,single_moves,end_moves,step_count,color,king)
            
            
        else:
            if 0<=c<8 and 0<=r<8 and 0<=c-1<8 and 0<=r+step_count<8:
                if board[r+step_count][c-1] == '.':
                    single_moves.append((r+step_count,c-1))
        return multiple_jumps,single_moves,end_moves

    def valid_moves(self,piece,board):
        """Defining a legal move for a particular piece on board. Called by all_moves func"""
        end_moves=list()
        moves= list()
        multiple_jumps =collections.defaultdict(list)
        single_moves =list()
        skipped = list()
        is_jump=False
        r = piece.row
        c = piece.col
        king = self.is_king(piece,piece.row)
        # normal move
        if piece.color == 'w' or king:
            jumps,single_moves,end_moves= self.left(board,r,c,multiple_jumps,single_moves,end_moves,step_count=-1,color =self.opposite(piece.color),king=king)
            jumps,single_moves,end_moves = self.right(board,r,c,multiple_jumps,single_moves,end_moves,step_count=-1,color=self.opposite(piece.color),king=king)
            
        if piece.color == 'b' or king:
            jumps,single_moves,end_moves  = self.left(board,r,c,multiple_jumps,single_moves,end_moves,step_count=1,color=self.opposite(piece.color),king=king)
            jumps,single_moves,end_moves= self.right(board,r,c,multiple_jumps,single_moves,end_moves,step_count=1,color=self.opposite(piece.color),king=king)
        
        #force jumps, therefore dont consider single move until jumps is not available    
        if jumps:
            is_jump =True
            #for each path get the opponent to capture
            queue = collections.deque()
            path = list()

            for move in end_moves:
                queue.append(move)
                skipped = list() #collections.defaultdict(list)
                vertex = move
                while queue:
                    if not path:
                        path.append(move)
                    vertex = queue.pop()
                    if vertex!=move:
                        path.append(vertex)
                    if vertex!= (r,c):
                        for neighbor in jumps[vertex]:
                            queue.append(neighbor)

                    else:
                        moves.append(path)
                        path = list()
        else:
            moves = single_moves
        
        return moves,is_jump
    def all_moves(self,states,player):
        """Check all moves for the current player on the board. called by action func"""
        black_moves = dict()
        white_moves = dict()
        is_jump = dict()
        state = deepcopy(states)
        if player == 'black':
            for i in range(0,len(states)):
                for j in range(0,len(states[i])):
                    if states[i][j] == 'b':
                        black_moves[(i,j)],is_jump[(i,j)]= self.valid_moves(piece.Piece([i,j],'b'),states)
                        if not black_moves[(i,j)]:
                            del black_moves[(i,j)]
                    if states[i][j] == 'B':
                        black_moves[(i,j)],is_jump[(i,j)]= self.valid_moves(piece.Piece([i,j],'b',king=True),states)
                        if not black_moves[(i,j)]:
                            del black_moves[(i,j)]
                        if is_jump[(i,j)]:
                            for moves in black_moves[(i,j)]:
                                board,state = self.resultState(state,moves,piece.Piece([i,j],'b',king=True),jump=True)
                                endx = moves[0][0]
                                endy = moves[0][1]
                                rem_val = self.valid_moves(piece.Piece([endx,endy],'b',king=True),board)
                                
                                if rem_val[1]:
                                    for items in rem_val[0]:
                                        black_moves[(i,j)].append(items[:len(items)-1] + moves)
                                    black_moves[(i,j)].remove(moves)
                                    
                        
        if player == 'white':
            for i in range(0,len(states)):
                for j in range(0,len(states[i])):
                    
                    if states[i][j] == 'w':
                        white_moves[(i,j)],is_jump[(i,j)]= self.valid_moves(piece.Piece([i,j],'w'),states)
                        if not white_moves[(i,j)]:
                            del white_moves[(i,j)]
                    if states[i][j] == 'W':
                        white_moves[(i,j)],is_jump[(i,j)]= self.valid_moves(piece.Piece([i,j],'w',king=True),states)
                        if not white_moves[(i,j)]:
                            del white_moves[(i,j)]
                        if is_jump[(i,j)]:
                            for moves in white_moves[(i,j)]:
                                board,state = self.resultState(state,moves,piece.Piece([i,j],'w',king=True),jump=True)
                                endx = moves[0][0]
                                endy = moves[0][1]
                                rem_val = self.valid_moves(piece.Piece([endx,endy],'w',king=True),board)
                                
                                if rem_val[1]:
                                    for items in rem_val[0]:
                                        white_moves[(i,j)].append(items[:len(items)-1] + moves)
                                    white_moves[(i,j)].remove(moves)
                                    
                        
   


        return black_moves,white_moves,is_jump
    def any_move(self,states,player):
        """Check for any moves for the current player on the board. If exists return true called by scores func"""
        black_moves = dict()
        white_moves = dict()
        if player == 'black':
            for i in range(0,8):
                for j in range(0,8):
                    if states[i][j] == 'b':
                        black_moves[(i,j)],is_jump= self.valid_moves(piece.Piece([i,j],'b'),states)
                    if states[i][j] == 'B':
                        black_moves[(i,j)],is_jump= self.valid_moves(piece.Piece([i,j],'b',king=True),states)
                    if black_moves.get((i,j)):
                        return True
        if player == 'white':
            
            for i in range(0,8):
                for j in range(0,8):
                    if states[i][j] == 'w':
                        
                        white_moves[(i,j)],is_jump= self.valid_moves(piece.Piece([i,j],'w'),states)
                        
                    if states[i][j] == 'W':
                        white_moves[(i,j)],is_jump= self.valid_moves(piece.Piece([i,j],'w',king=True),states)
                    if white_moves.get((i,j)):
                        return True
        return False

    def score(self,board,player):
        """This function is called by alpha-beta func to get the score if end of game else return moves"""
        black_moves = dict()
        white_moves = dict()
        states = board.copy()
        flag = 0
        opt = optimize.Optimize(board,player)
        
        move_exists = self.any_move(states,player)
        #if player is black, if no black coins remain, black loses, if black cannot move and white cannnot move, draw 
        if player == 'black':
            for rows in states:
                if 'b' in rows or 'B' in rows:
                    flag =1
                    break
            if flag ==0:
                bc,bk,wc,wk = opt.count_checkers(board)
                return -(wc+(2*wk))
            if not move_exists:
                white_move_exists = self.any_move(states,player='white')
                if not white_move_exists:
                    return 0
                else:
                    bc,bk,wc,wk = opt.count_checkers(board)
                    return -(wc+(2*wk))
            
        elif player == 'white':
            for rows in states:
                if 'w' in rows or 'W' in rows:
                    flag =1
                    break
            if flag ==0:
                bc,bk,wc,wk = opt.count_checkers(board)
                return -(bc+(2*bk))
            if not move_exists:
                black_move_exists = self.any_move(states,player='black')
                if not black_move_exists:
                    return 0
                else:
                    bc,bk,wc,wk = opt.count_checkers(board)
                    return -(bc+(2*bk))

        return None
    def game_action(self,states,player):
        return self.all_moves(states,player)

    


    def priority(self,board):
        """ priority of actions in checkers"""
        pass
    
    


