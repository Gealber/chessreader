from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from model.square import Square
from model.engine import GameState, Move
import os
import re
import chess.pgn

IMAGE_DIR = os.path.join('images', 'pieces')

class MainWindow(QWidget):
    """
    As the name suggests is just the main window of the application.
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self._black_pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP']
        self._white_pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP']
        self.setAcceptDrops(True)

        self.repaint = False
        self.squares = []
        self.setWindowTitle("Chess Board")

        self._layout = QGridLayout()
        self.setSquares()
        self._layout.setSpacing(0)

        self.setLayout(self._layout)
        self.setFixedSize(650, 650)
        self.game_state = GameState(self.squares)

    def setSquares(self, board=None):
        self.squares = []
        for i in range(8):
            temp = []
            for j in range(8):
                color = '#00695C'
                if (i+j) % 2 == 0:
                    color = 'white'

                if board:
                    name = board[i][j]
                    if name != "--":
                        piece = os.path.join(IMAGE_DIR, f"{board[i][j]}.svg")
                    else:
                        piece = None
                else:
                    piece = self.getPiece(i,j)
                square = Square(color, [i, j], piece=piece)
                square.sqSelected.connect(self.onSqSelected)
                temp.append(square) #this is not needed
                self._layout.addWidget(square, i, j)
            self.squares.append(temp)
        if board:
            self.game_state.squares = self.squares

    def getPiece(self, i , j):
        if i == 0:
            image = os.path.join(IMAGE_DIR, f"{self._black_pieces[j]}.svg")
            return image
        elif i == 1:
            image = os.path.join(IMAGE_DIR, f"{self._black_pieces[8]}.svg")
            return image
        elif i == 6:
            image = os.path.join(IMAGE_DIR, f"{self._white_pieces[8]}.svg")
            return image
        elif i == 7:
            image = os.path.join(IMAGE_DIR, f"{self._white_pieces[j]}.svg")
            return image
        else:
            return None

    def paintEvent(self, event):
        if self.repaint:
            pass
        return

    def render(self, FEN):
        """
        This function will be called when we drop a pgn document in the widget.
        """
        if FEN:
            print(FEN)
            self.game_state.updateState(FEN)
            self.setSquares(self.game_state.board)
        else:
            print("You must provide a FEN")

    def onSqSelected(self, square):
        self.game_state.playerClicks.append(square)
        if len(self.game_state.playerClicks) == 2:
            sq1 = self.game_state.playerClicks[0]
            sq2 = self.game_state.playerClicks[1]
            move = Move(sq1.pos, sq2.pos, self.game_state.board)
            if self.game_state.isValidMove(move):
                self.game_state.makeMove(move)
            else:
                print("Not a valid move moron!")
            self.game_state.playerClicks = []

    def dragEnterEvent(self, event):
        data = event.mimeData()
        if data.hasText():
            event.accept()

    def dropEvent(self, event):
        data = event.mimeData()
        path_file = data.text().strip().replace("file://", "")
        isfile = os.path.isfile(path_file)
        if re.compile(r'.pgn$').findall(path_file) and isfile:
            with open(path_file) as pgn:
                new_board = chess.pgn.read_game(pgn)
                fen = new_board.headers.get("FEN")
                if new_board and fen:
                    #Need to handle the FEN
                    self.render(fen)
                else:
                    print("Not a valid pgn")

if __name__ == '__main__':
    app = QApplication([])
    board = MainWindow()
    board.show()
    app.exec_()
