"""
Contains all the state of the game. There are three principal classes here:
GameState: like the name say contains the actual state of the game.
Move: Describe a move in the game.
GameLoaded: This is only in case a pgn file is drop into the board, so in this case
the state of the game will be refreshed and will be the current pgn dropped.
"""

import chess
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class GameState:
    """
    Describe the state of the game
    squares: a list with all the square widgets
    _board: the game in the python-chess,
    necesary to validate moves and all the logic.
    board: a representation of the square necesary to paint the board.
    moveLog: a log of all the move that were made.
    playerClicks: to keep a count on the clicks of the user,
    is empty every two clicks.
    game_loaded: a flag to know if a pgn was dropped.
    """
    def __init__(self, squares):
        self.squares = squares
        self._board = chess.Board()
        self.board = self.board_repre()
        self.whiteToMove = True
        self.moveLog = []
        self.playerClicks = []
        self.game_loaded = None

    def board_repre(self):
        board = [row.split() for row in self._board.__str__().split("\n")]
        result = []
        for i, row in enumerate(board):
            temp = []
            for el in row:
                if el != ".":
                    color = "b" if el.islower() else "w"
                    temp.append(color+el.upper())
                else:
                    temp.append("--")
            result.append(temp)
        return result


    def makeMove(self, move):
        if self._board.is_check():
            print("You are in check moron")
            if self._board.is_checkmate():
                print("Ouuu you're done moron")
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.replacePieces(move.startRow, move.startCol, move.endRow, move.endCol)
        #Passant
        if self.enPassant(move):
            self.makePassant(move)
        #Castling
        self.makeIfCastling(move)
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if self.moveLog:
            lastMove = self.moveLog.pop()
            sq1 = self.squares[lastMove.endRow][lastMove.endCol]
            sq2 = self.squares[lastMove.startRow][lastMove.startCol]
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCapture
            sq1.piece = os.path.join("images","pieces",f"{lastMove.pieceCapture}.svg")
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved
            sq2.piece = os.path.join("images","pieces",f"{lastMove.pieceMoved}.svg")
            sq1.refresh_pixmap()
            sq2.refresh_pixmap()
            self.passant_update(lastMove)
            self.castling_update(lastMove)

            self._board.pop()
            self.whiteToMove = not self.whiteToMove

    def passant_update(self, lastMove):
        """
        Update the correct pixmaps in case a
        pawn passant was made. Also update board.
        """
        if lastMove.special == 'pb':
            sq3 = self.squares[lastMove.endRow-1][lastMove.endCol]
            sq3.piece = os.path.join("images","pieces","wP.svg")
            self.board[lastMove.endRow-1][lastMove.endCol] = 'wP'
            sq3.refresh_pixmap()
        elif lastMove.special == 'pw':
            sq3 = self.squares[lastMove.endRow+1][lastMove.endCol]
            sq3.piece = os.path.join("images", "pieces", "bP.svg")
            self.board[lastMove.endRow+1][lastMove.endCol] = 'bP'
            sq3.refresh_pixmap()

    def castling_update(self,lastMove):
        """
        Update the correct pixmaps in case a castling
        was made.
        """
        if lastMove.special == 'cr':
            sq3 = self.squares[lastMove.endRow][7]
            sq3.piece = os.path.join("images","pieces",f"{lastMove.pieceMoved[0]}R.svg")
            sq3.refresh_pixmap()
            self.board[lastMove.endRow][7] = f'{lastMove.pieceMoved[0]}R'
            sq3 = self.squares[lastMove.endRow][5]
            sq3.piece = None
            sq3.refresh_pixmap()
            self.board[lastMove.endRow][5] = "--"
        elif lastMove.special == 'cl':
            sq3 = self.squares[lastMove.endRow][0]
            sq3.piece = os.path.join("images","pieces",f"{lastMove.pieceMoved[0]}R.svg")
            sq3.refresh_pixmap()
            self.board[lastMove.endRow][0] = f'{lastMove.pieceMoved[0]}R'
            sq3 = self.squares[lastMove.endRow][3]
            sq3.piece = None
            sq3.refresh_pixmap()
            self.board[lastMove.endRow][3] = "--"

    def isValidMove(self, move):
        """
        Validate the move using python-chess. In case
        of been a valid move is pushed into _board.
        """
        uci_move = chess.Move.from_uci(move.getChessNotation())
        isvalid = uci_move in self._board.legal_moves
        if isvalid:
            self._board.push(uci_move)
            return True
        return False

    def enPassant(self, move):
        isPawn = move.pieceMoved[1] == 'P'
        captureEmpty = (move.pieceCapture == "--") and (move.startCol != move.endCol)
        return isPawn and captureEmpty

    def makePassant(self, move):
        if move.pieceMoved[0] == 'b':
            self.board[move.endRow-1][move.endCol] = "--"
            self.squares[move.endRow-1][move.endCol].setPixmap(QPixmap())
            move.special = 'pb' #p de passant black

        else:
            self.board[move.endRow+1][move.endCol] = "--"
            self.squares[move.endRow+1][move.endCol].setPixmap(QPixmap())
            move.special = 'pw' #p de passant white

    def makeIfCastling(self, move):
        if move.pieceMoved[1] == 'K':
            if (move.startCol == move.endCol - 2):
                #right
                rook = self.board[move.startRow][7]
                rook_pixmap = self.squares[move.startRow][7].pixmap()
                self.board[move.startRow][7] = self.board[move.startRow][5]
                self.board[move.startRow][5] = rook
                self.squares[move.startRow][5].setPixmap(rook_pixmap)
                self.squares[move.startRow][7].setPixmap(QPixmap())
                move.special = 'cr' #c de castling to right

            if (move.startCol == move.endCol + 2):
                #left
                rook = self.board[move.startRow][0]
                rook_pixmap = self.squares[move.startRow][0].pixmap()
                self.board[move.startRow][0] = self.board[move.startRow][3]
                self.board[move.startRow][3] = rook
                self.squares[move.startRow][3].setPixmap(rook_pixmap)
                self.squares[move.startRow][0].setPixmap(QPixmap())
                move.special = 'cl' #castling to left

    def replacePieces(self, startRow, startCol, endRow, endCol):
        sq2 = self.squares[endRow][endCol]
        sq1 = self.squares[startRow][startCol]
        sq2.setPixmap(sq1.pixmap())
        sq1.setPixmap(QPixmap())

    def updateState(self, FEN):
        self._board = chess.Board(FEN)
        self.board = self.board_repre()


class Move:
    """
    Move represent a move in the game.
    """
    ranksToRows = {f"{8-i}": i for i in range(7, -1, -1)}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    letters = 'abcdefgh'
    filesToCols = {v:k for k, v in enumerate(letters)}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, special=None):
        self.special = special
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCapture = board[self.endRow][self.endCol]
        self.moveID = hash(self.pieceMoved+self.pieceCapture)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def __repr__(self):
        return f"<Move sq1='{self.pieceMoved}' sq2='{self.pieceCapture}'>"

    def getChessNotation(self):
        startRankFile = self.getRankFile(self.startRow, self.startCol)
        endRankFile = self.getRankFile(self.endRow, self.endCol)
        return startRankFile + endRankFile

    def getSan(self):
        capture = False
        piece = ""
        endRankFile = self.getRankFile(self.endRow, self.endCol)
        startRankFile = self.getRankFile(self.startRow, self.startCol)
        if self.pieceMoved[1] == "P" and self.pieceCapture != "--":
            piece = startRankFile
        elif self.pieceMoved[1] == "P" and self.pieceCapture == "--":
            piece = ""
        elif self.pieceMoved[1] == "K":
            if self.special == "cr":
                return "0-0"
            elif self.special == "cl":
                return "0-0-0"
            else:
                piece = self.pieceMoved[1]
        else:
            piece = self.pieceMoved[1]

        if self.pieceCapture != "--":
            capture = True
        x = "x" if capture else ""
        return f"{piece}{x}{endRankFile}"

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


class GameLoaded:
    """
    Represent the info when a widget is dropped into the
    widget.
    """
    letters = 'abcdefgh'
    filesToCols = {v:k for k, v in enumerate(letters)}
    def __init__(self, game):
        self.game = game
        self.headers = game.headers
        self.FEN = game.headers.get("FEN")
        self.moves = list(game.mainline_moves())
        self.current_pos = 0

    def get_move(self, direction, board):
        if direction == 'f' and self.current_pos < len(self.moves):
            uci = self.moves[self.current_pos].__str__()
            self.current_pos += 1
            move = self._move_from_uci(uci, board)
            return move

        elif direction == 'b' and self.current_pos > 0:
            self.current_pos -= 1
            uci = self.moves[self.current_pos-1].__str__()
            move = self._move_from_uci(uci, board)
            return move

    def uci2_pos(self, uci):
        pos1 = [8-int(uci[1]), self.filesToCols[uci[0]]]
        pos2 = [8-int(uci[3]), self.filesToCols[uci[2]]]
        return pos1, pos2

    def _move_from_uci(self, uci, board):
        pos1, pos2 = self.uci2_pos(uci)
        move = Move(pos1,pos2,board)
        return move
