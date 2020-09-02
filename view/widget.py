from model.square import Square
from model.engine import GameState, Move, GameLoaded
import os
import re
import chess.pgn
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from view.lowerbar import LowerBar


IMAGE_DIR = os.path.join('images', 'pieces')

class MainWindow(QWidget):
    """
    As the name suggests is just the main window of the widget.
    """
    def __init__(self,dark=False, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        if dark:
            self.setAutoFillBackground(True)
            palette = self.palette()
            palette.setColor(QPalette.Window, QColor("#3a3a3a"))
            self.setPalette(palette)


        self._black_pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP']
        self._white_pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP']
        self.setAcceptDrops(True) #allow to drop pgn files

        self.squares = []
        self.setWindowTitle("Chess Board")

        self.vlayout = QVBoxLayout()
        self._layout = QGridLayout()
        self.setSquares()
        self._layout.setSpacing(0)
        self.vlayout.setSpacing(2)

        self.lowerbar = LowerBar()
        self.lowerbar.forward.pressed.connect(self.onForwardPressed)
        self.lowerbar.backward.pressed.connect(self.onBackwardPressed)
        self.setFixedSize(630, 660)
        self.game_state = GameState(self.squares)
        self.vlayout.addLayout(self._layout)
        self.vlayout.addWidget(self.lowerbar)
        self.setLayout(self.vlayout)

    def setSquares(self, board=None):
        """
        param board: a two dimensional array with the representation of the board.
        If given this board will be painted in the widget.
        """
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
                    piece = self._getPiece(i,j)
                square = Square(color, [i, j], piece=piece)
                square.sqSelected.connect(self.onSqSelected)
                temp.append(square) #this is not needed
                self._layout.addWidget(square, i, j)
            self.squares.append(temp)
        if board:
            self.game_state.squares = self.squares

    def _getPiece(self, i , j):
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


    def _render(self, FEN):
        """
        This function will be called when we drop a pgn document in the widget.
        """
        if FEN:
            self.game_state.updateState(FEN)
            self.setSquares(self.game_state.board)
        else:
            print("You must provide a FEN")

    def onSqSelected(self, square):
        """
        Define the behavior when the sqSelected signal is triggered.
        Order to make the move if the conditions are holded.
        """
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

    def extractGame(self, file):
        with open(file) as pgn:
            try:
                new_board = chess.pgn.read_game(pgn)
            except Exception as e:
                print("Bad encoding pgn: ", e)
                return
        return new_board


    def dropEvent(self, event):
        """
        Define the behavior on a drop event. In this case the only dropEvent
        will be when we drop a pgn file to be read.
        """
        data = event.mimeData()
        path_file = data.text().strip().replace("file://", "")
        isfile = os.path.isfile(path_file)
        if re.compile(r'.pgn$').findall(path_file) and isfile:
            game = self.extractGame(path_file)
            fen = game.headers.get("FEN")
            self.game_state.game_loaded = GameLoaded(game)
            if fen:
                #Need to handle the FEN
                self._render(fen)
            else:
                print("Not a valid pgn")

    def onForwardPressed(self, button):
        if self.game_state.game_loaded:
            game = self.game_state.game_loaded
            move = game.get_move('f', self.game_state.board)
            if move is not None and self.game_state.isValidMove(move):
                self.game_state.makeMove(move)


    def onBackwardPressed(self, button):
        self.game_state.undoMove()

