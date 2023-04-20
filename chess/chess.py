from entities import *
from piece import *


class Chess:
    """Class to handle the game play"""

    def __init__(
        self,
        whitePieces: list[Piece] = None,
        blackPieces: list[Piece] = None,
        killedPieces: dict[str, list[Piece]] = None,
        currentTurn=Color.WHITE,
    ) -> None:
        """create a chess game

        Args:
            whitePieces (list[Piece], optional): set of all white pieces. Defaults to None. leave it to none to create a default new game
            blackPieces (list[Piece], optional): set of all black pieces. Defaults to None.
            currentTurn (_type_, optional): color of the current player. Defaults to Color.WHITE.
        """
        # set current turn (white or black)
        self.turn: Color = currentTurn
        # creating the pieces(dict of list)
        self.pieces: dict[str, list[Piece]] = dict()
        self.killedPieces: dict[str, list[Piece]] = dict()
        # point on boot kings
        self.kings: dict[Color, King] = dict()
        # creating the board (dict of list 8*8)
        self.board: dict[str, list[Position]] = dict()
        for i in range(CHESS_SIZE):
            self.board[COLUMN[i]] = list()
            self.board[COLUMN[i]] = [
                Position(column=i, line=j) for j in range(CHESS_SIZE)
            ]
        # init pieces. if whitePieces not defined then all pices are set by default
        if not whitePieces:
            for color in Color:
                self.killedPieces[color.name] = list()
                self.pieces[color.name] = list()
                # creating pawns
                line = 1 if color == Color.WHITE else 6
                for i in range(8):
                    position: Position = self.board[COLUMN[i]][line]
                    pawn = Pawn(color=color, position=position)
                    self.pieces[color.name].append(pawn)

                # creating Rooks
                colPosition = [0, 7]
                line = 0 if color == Color.WHITE else 7
                for i in range(2):
                    position: Position = self.board[COLUMN[colPosition[i]]][line]
                    rook = Rook(color=color, position=position)
                    self.pieces[color.name].append(rook)

                # creating Knights
                colPosition = [1, 6]
                for i in range(2):
                    position: Position = self.board[COLUMN[colPosition[i]]][line]
                    knight = Knight(color=color, position=position)
                    self.pieces[color.name].append(knight)

                # creating Bishops
                colPosition = [2, 5]
                for i in range(2):
                    position: Position = self.board[COLUMN[colPosition[i]]][line]
                    bishop = Bishop(color=color, position=position)
                    self.pieces[color.name].append(bishop)
                # creating Queens
                position: Position = self.board[COLUMN[3]][line]
                queen = Queen(color=color, position=position)
                queen.position.free = False
                self.pieces[color.name].append(queen)

                # creating Kings
                position: Position = self.board[COLUMN[4]][line]
                self.kings[color] = King(color, position=position)
                self.pieces[color.name].append(self.kings[color])

        else:
            self.pieces[Color.WHITE] = whitePieces
            self.pieces[Color.BLACK] = blackPieces
            self.killedPieces = killedPieces

        self.pieceSelected = None

    def selected(self, position: tuple[str, int], board: dict[str, list[Position]]):
        print(self.turn)
        column = position[0]
        line = position[1]
        position = self.board[column][line]
        if position.isFree() and not self.pieceSelected == None:
            piece = self.pieceSelected
            moveList = piece.getMoveList(self.board)
            print("moving")
            if position in moveList:
                print("can move")
                print(type(piece))
                piece.move(position, board)
                self.pieceSelected = None
                self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
            else:
                print("moving canceled")
                self.pieceSelected = None

        elif not position.isFree():
            target = position.piece
            if not self.pieceSelected == None:
                piece = self.pieceSelected
                moveList = piece.getMoveList(self.board)
                if position in moveList and target.color != self.turn:
                    print("killing")
                    initLen = len(self.pieces[target.color.name])
                    self.pieces[target.color.name].remove(target)
                    self.killedPieces[target.color.name].append(target)
                    finalLen = len(self.pieces[target.color.name])
                    piece.move(position, self.board)
                    if finalLen != initLen - 1:
                        raise ("something went wrong")
                    self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
                    self.pieceSelected = None

                elif target.color == self.turn:
                    print("shit")
                    self.pieceSelected = target
                else:
                    print("damn")
                    self.pieceSelected = None
            else:
                print("else")
                if target.color == self.turn:
                    self.pieceSelected = target

    def isKingThreatened(self) -> bool:
        opponentColor = Color.WHITE if self.turn == Color.BLACK else Color.WHITE
        pieces: list[Piece] = self.pieces[opponentColor]
        threat = False
        for piece in pieces:
            moves = piece.getMoveList()
            if self.kings[self.turn].position in moves:
                threat = True
                break
        return threat
