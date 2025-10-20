
import tkinter as tk, random
from tkinter import messagebox
from .game import ConnectX, COLS, ROWS
from . import ai as ai_impl
CELL=70; MARGIN=20
def main():
    g=ConnectX(); root=tk.Tk(); root.title("HW4 ConnectX — Minimax/Alpha-Beta/Evaluator")
    status=tk.StringVar(value="Human (R) vs AI (Y)"); tk.Label(root,textvariable=status).pack()
    canvas=tk.Canvas(root,width=COLS*CELL+MARGIN*2,height=ROWS*CELL+MARGIN*2,bg='white'); canvas.pack(padx=8,pady=8)
    mode=tk.StringVar(value="AI")
    tk.Radiobutton(root,text="Random",variable=mode,value="RANDOM").pack(anchor="w")
    tk.Radiobutton(root,text="AI",variable=mode,value="AI").pack(anchor="w")
    def draw():
        canvas.delete("all")
        for c in range(COLS):
            for r in range(ROWS):
                x=MARGIN+c*CELL+CELL//2; y=MARGIN+r*CELL+CELL//2
                canvas.create_oval(x-30,y-30,x+30,y+30,fill="lightblue")
                v=g.board[r][c]
                if v: canvas.create_oval(x-28,y-28,x+28,y+28, fill=("red" if v=='R' else "gold"))
    def click(evt):
        if g.is_terminal(): return
        c=int((evt.x-MARGIN)//CELL)
        if 0<=c<COLS and g.can_play(c):
            g.play(c); draw()
            if not g.is_terminal(): root.after(50, ai_turn)
    def ai_turn():
        if mode.get()=="RANDOM":
            mv=random.choice(g.legal_actions())
        else:
            try: mv=ai_impl.best_move(g, depth=3, use_alpha_beta=True, evaluator=lambda gg: 0)
            except NotImplementedError:
                messagebox.showinfo("AI not implemented","Implement best_move() in ai.py; using random.")
                mv=random.choice(g.legal_actions())
        g.play(mv); draw()
    tk.Button(root,text="Reset",command=lambda:(g.reset(),draw())).pack(pady=6)
    canvas.bind("<Button-1>", click); draw(); root.mainloop()
if __name__=="__main__": main()
