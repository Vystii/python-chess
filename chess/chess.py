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
        self.gameOver = False
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
        self.message = str()
        self.opponent = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
        self.newTurn = True

    def testGameOver(self):
        state: bool = bool
        self.gameOver = not self.canMove()
        if self.gameOver:
            state = True
            message = f"CHECK MATE {self.opponent} Won"
        else:
            state = False
            message = None
        return state, message

    def isNewTurn(self):
        state = self.newTurn
        self.newTurn = False
        return state

    def selected(self, position: tuple[str, int], board: dict[str, list[Position]]):
        # print(self.turn)
        print(f"selected => {position}")
        column = position[0]
        line = position[1]
        position = self.board[column][line]
        # if the target is free and a piece have already been selected
        if position.isFree() and not self.pieceSelected == None:
            piece = self.pieceSelected
            moveList = piece.getMoveList(self.board)
            if position in moveList:
                piece.move(position, board)
                if self.isKingThreatened():
                    piece.cancelMove()
                    return False
                else:
                    print("gg")
                    self.pieceSelected = None
                    opponent = self.turn
                    self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
                    self.newTurn = True

            else:
                raise ("there")
                self.pieceSelected = None

        # if the target is not free
        elif not position.isFree():
            target = position.piece
            # if if a piece have already been selected
            if not self.pieceSelected == None:
                piece = self.pieceSelected
                moveList = piece.getMoveList(self.board)
                # if selected box is in the move list of the selected piece then kill to piece on the target and replace it
                if position in moveList and target.color != self.turn:
                    initLen = len(self.pieces[target.color.name])
                    self.pieces[target.color.name].remove(target)
                    self.killedPieces[target.color.name].append(target)
                    finalLen = len(self.pieces[target.color.name])
                    piece.move(position, self.board)
                    if finalLen != initLen - 1:
                        raise ("something went wrong")

                    if self.isKingThreatened():
                        piece.cancelMove()
                        return False
                    else:
                        self.opponent = self.turn
                        self.turn = (
                            Color.BLACK if self.turn == Color.WHITE else Color.WHITE
                        )
                        self.pieceSelected = None
                        self.newTurn = True

                # if the piece in the target box has the same color then set it as the selected piece
                elif target.color == self.turn:
                    self.pieceSelected = target
                # unselect
                else:
                    self.pieceSelected = None
            else:
                if target.color == self.turn:
                    self.pieceSelected = target
        return True

    def canMove(self):
        canMove = False
        print("canMovel")
        for piece in self.pieces[self.turn.name]:
            moveList = piece.getMoveList(self.board)
            piece_position = {
                "column": COLUMN[piece.position.column],
                "line": piece.position.line,
            }
            for move in moveList:
                line = move.line
                column = COLUMN[move.column]
                self.selected(
                    (piece_position["column"], piece_position["line"]), self.board
                )
                temp = self.selected((column, line), self.board)
                print(temp)
                if temp:
                    # print(f"the position is {piece.position}")
                    canMove = True
                    raise ("pause")
                    piece.cancelMove()
                    break
                # raise ("first")
        return canMove

    def isKingThreatened(self) -> bool:
        opponentColor = Color.WHITE if self.turn == Color.BLACK else Color.WHITE
        pieces: list[Piece] = self.pieces[opponentColor.name]
        threat = False
        for piece in pieces:
            moves = piece.getMoveList(self.board)
            if self.kings[self.turn].position in moves:
                threat = True
                break
        return threat
