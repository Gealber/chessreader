import chess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class GameState:
    def __init__(self, squares):
        self.squares = squares
        self._board = chess.Board()
        self.board = self.board_repre()
        self.whiteToMove = True
        self.moveLog = []
        self.playerClicks = []

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
                print("Ouuu your done moron")
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
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCapture
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved
            self.whiteToMove = not self.whiteToMove

    def isValidMove(self, move):
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
        print(sq1)
        print(sq2)
        sq2.setPixmap(sq1.pixmap())
        sq1.setPixmap(QPixmap())

    def updateState(self, FEN):
        self._board = chess.Board(FEN)
        print(self._board)
        self.board = self.board_repre()

    def getValidMove(self):
        """All moves considering checks"""
        pass

    def getAllPosibleMoves(self):
        """All moves without consifering checks"""
        pass


class Move:
    ranksToRows = {f"{8-i}": i for i in range(7, -1, -1)}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    letters = 'abcdefgh'
    filesToCols = {v:k for k, v in enumerate(letters)}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
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

    def getChessNotation(self):
        startRankFile = self.getRankFile(self.startRow, self.startCol)
        endRankFile = self.getRankFile(self.endRow, self.endCol)
        return startRankFile + endRankFile


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


