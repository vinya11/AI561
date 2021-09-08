class Piece:
    """
    pos: row and col
    colour : 'b','w'
    king: True, False
    """
    def __init__(self,pos,color,king=False):
        self.row = pos[0]
        self.col = pos[1]
        self.color = color

        self.king = king
