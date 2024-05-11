import tkinter as tk
from client import * 
import json
from rules import *
def parse_received_data(received_data):
    new_data = json.loads(received_data)
    return new_data
def receive_messages(client_socket,gui):
    while True:
        received_data = client_socket.recv(1024).decode("utf-8")
        if not received_data:
            print("Server closed the connection.")
            break
        
        new_board_state= parse_received_data(received_data)
        if(new_board_state["turn"]==2):
            gui.update_board(new_board_state["board"])
            gui.currPlayerTurn=1 
def send_messages(client_socket,data):
        encoded_data = json.dumps(data)
        client_socket.send(encoded_data.encode('utf-8'))
        


class ChessGUI:
    def __init__(self, master,client,turn):
        self.currPlayerTurn=int(turn)
        self.master = master
        self.client=client
        self.turn = int(turn)
        self.master.title("Chess")
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        self.draw_board()
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
        ]
        self.draw_pieces()
        self.selected_piece = None
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_drag)
        self.canvas.bind("<ButtonRelease-1>", self.handle_release)
        receive_thread = Thread(target=receive_messages, args=(client,self))
        receive_thread.start()
        
    def is_valid_movment(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Check if the start and end positions are the same
        if start_pos == end_pos:
            return False

        # Check if the destination is within the board boundaries
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        if(self.board[start_pos][1]=='q'):
            return is_valid_queen(self, start_pos, end_pos)
        if(self.board[start_pos][1]=='k'):
            return is_valid_king(self, start_pos, end_pos)
        
            
    def update_board(self, new_board_state):
        self.board = new_board_state
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()
    
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill=color)

    def draw_pieces(self):
        self.piece_images = {}
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece:
                    filename = piece + ".png"
                    self.piece_images[(i, j)] = tk.PhotoImage(file=filename)
                    self.canvas.create_image(j * 50 + 25, i * 50 + 25, image=self.piece_images[(i, j)])

    def handle_click(self, event):
        print(self.board)
        print(self.currPlayerTurn)
        print(self.turn)
        x, y = event.x, event.y
        col, row = x // 50, y // 50
        piece = self.board[row][col]
        if piece and (row, col) != self.selected_piece and self.currPlayerTurn==1:
            if(self.board[row][col][0]=='b' and self.turn==2):
                self.selected_piece = (row, col)
            elif(self.board[row][col][0]=='w' and self.turn==1):
                self.selected_piece = (row, col)


    def handle_drag(self, event):

        if self.selected_piece:
            x, y = event.x, event.y
            col, row = x // 50, y // 50
            # if(self.selected_piece[0]==row and self.selected_piece[1]==col):
            #     self.canvas.dtag(self.piece_images[(self.selected_piece[0], self.selected_piece[1])], "highlight")
            #     return
            self.canvas.delete("highlight")
            self.canvas.create_image(x, y, image=self.piece_images[self.selected_piece], tags="highlight")

    def handle_release(self, event):
        if self.selected_piece and self.currPlayerTurn==1:
            x, y = event.x, event.y
            col, row = x // 50, y // 50
            #check if the piece is released in its location :
            if(self.selected_piece[0]==row and self.selected_piece[1]==col):
                self.canvas.dtag(self.piece_images[(self.selected_piece[0], self.selected_piece[1])], "highlight")
                return 
            
            self.board[row][col] = self.board[self.selected_piece[0]][self.selected_piece[1]]
            self.board[self.selected_piece[0]][self.selected_piece[1]] = ""
            self.canvas.delete("highlight")
            self.canvas.delete("all")
            self.draw_board()
            self.draw_pieces()
            self.currPlayerTurn=2 
            send_messages(self.client,{"board":self.board,"turn":self.currPlayerTurn})
            self.selected_piece = None

def main():
    turn,client=init_network()
    root = tk.Tk()
    gui = ChessGUI(root,client,turn)
    root.mainloop()

if __name__ == "__main__":
    main()
