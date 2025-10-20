
COLS, ROWS = 7, 6
class ConnectX:
    def __init__(self): self.board=[[None for _ in range(COLS)] for _ in range(ROWS)]; self.player='R'
    def reset(self): self.__init__()
    def clone(self):
        g=ConnectX(); g.board=[row[:] for row in self.board]; g.player=self.player; return g
    def can_play(self, col): return self.board[0][col] is None
    def legal_actions(self): return [c for c in range(COLS) if self.can_play(c)]
    def play(self, col):
        for r in range(ROWS-1,-1,-1):
            if self.board[r][col] is None:
                self.board[r][col]=self.player; self.player=('Y' if self.player=='R' else 'R'); break
    def is_terminal(self): return self.winner() is not None or not any(self.can_play(c) for c in range(COLS))
    def winner(self):
        B=self.board; dirs=[(1,0),(0,1),(1,1),(1,-1)]
        for r in range(ROWS):
            for c in range(COLS):
                if not B[r][c]: continue
                for dr,dc in dirs:
                    try: line=[B[r+i*dr][c+i*dc] for i in range(4)]
                    except IndexError: line=[]
                    if len(line)==4 and all(v==B[r][c] for v in line): return B[r][c]
        return None
