from abc import ABC, abstractmethod
from enum import Enum

# from entities import Piece, Position
import pygame


column = "a b c d e f g h"
line = [i + 1 for i in range(8)]
COLUMN: list[str] = column.split(sep=" ")
CHESS_SIZE = 8


class Color(Enum):
    WHITE = 1
    BLACK = 2


class Position:
    image: pygame.image
    _registries = list()

    def __init__(self, line: int, column: int, isFree: bool = True, piece=None):
        """Create a case

        Args:
            line (int): indice of the case
            column (int): column of the case
            isFree (bool, optional): state of the case (if it's occupied or not) Defaults to True.
        """
        # line -= 1
        # column -= 1
        self.piece: Piece = piece
        error_message = "invalid value"
        if line > 7 or line < 0:
            raise TypeError("line " + error_message)
        if column > 7 or column < 0:
            raise TypeError("column " + error_message)

        self.line = line
        self.column = column
        self.free = isFree
        pass

    def __eq__(self, other) -> bool:
        return self.column == other.column and self.line == other.line

    def __str__(self):
        return f"{self.line}, {COLUMN[self.column]}"

    def setFree(self) -> None:
        self.free = True

    def setOccupied(self) -> None:
        self.free = False

    def isFree(self) -> bool:
        """State of a position (free or not)

        Returns:
            bool: True when the position is available an false otherwise
        """
        return self.free

    def getIndices(self):
        """get the coordonates as a

        Returns:
            coordonates
        """
        return self.line, self.column

    def isthreatened(self, color: Color) -> bool:
        """know if the case is threatened by a given color

        Args:
            color (Color): the color that is suppose to threat the position

        Returns:
            bool: True if the position is threatened and False otherwise
        """
        opponentPiecesList: list[Piece] = Piece.getColorPieceList(color)
        for opponentPiece in opponentPiecesList:
            if opponentPiece.isAlive():
                targets: list[Position] = opponentPiece.getMoveList()
                for position in targets:
                    if self == position:
                        return True
        return False


class Piece(ABC):
    def __str__(self):
        return self.__class__.__name__

    image: pygame.image
    _registry = {"white": [], "black": []}

    def __init__(
        self,
        color: Color,
        position: Position = Position(0, 0, True),
        state: bool = True,
    ):
        """initialize a piece

        Args:
            position (Position, optional): initial position of the piece. Defaults to Position(1, 1, True).
            state (bool, optional): True if the piece is alive False if it's dead. Defaults to True.
            color(Color): WHITE or BLACK
        Raises:
            TypeError: the position of the piece your trying to save is currently occupied
        """
        self.moveCount = 0
        if not position.isFree():
            raise TypeError(f"position not available")
        self.state: bool = True
        self.position: Position = position
        self.color: Color = color
        self.position.free: bool = False
        self.position.piece: Piece = self
        self.oldPosition: Position = None
        if color == Color.BLACK:
            self._registry["black"].append(self)
        else:
            self._registry["white"].append(self)
        pass

    def getOpponentList(self):
        if self.color == Color.WHITE:
            return self._registry["black"]
        return self._registry["white"]

    @classmethod
    def getColorPieceList(cls, color: Color) -> list:
        """return all the living pieces of a given color


        Args:
            color (Color): the color of the pieces you want

        Returns:
            list[Piece]: list of pieces
        """
        strColor = "white" if color == Color.WHITE else Color.BLACK
        return [element for element in cls._registry[strColor] if element.isAlive()]

    def setDead(self):
        """Set the piece as dead"""
        self.state = False
        pass

    def isAlive(self) -> bool:
        """get the statut of the piece

        Returns:
            bool: True if the piece is still alive
        """
        return self.state

    def move(self, newPosition: Position, board: dict[str, list[Position]]) -> bool:
        """change the position of the piece

        Args:
            newPosition (Position): The new position of the piece

        Returns:
            bool: True if the position was free and False otherwise
        """
        print(f"new position => {newPosition}")

        canGo = self.getMoveList(board)
        if not (newPosition in canGo):
            raise TypeError("this piece can't go to the given position")
        self.oldPosition = self.position
        self.position.setFree()
        self.position = newPosition
        self.position.setOccupied()
        self.position.piece = self
        self.moveCount += 1
        return True

    def cancelMove(self) -> None:
        self.position.setFree()
        self.position = self.oldPosition
        self.oldPosition = None
        self.position.setOccupied()
        self.moveCount -= 1

    @abstractmethod
    def getMoveList(self, board: dict[str, list[Position]]) -> list[Position]:
        """Get the list of possible move

        Returns:
            list: possible moves
        """
        pass
