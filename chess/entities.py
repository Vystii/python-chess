from abc import ABC, abstractmethod
from enum import Enum
import chess.entities as _

column = "a b c d e f g h"
line = [i+1 for i in range(8)]
COLUMN:list[str] = column.split(sep=" ")
CHESS_SIZE = 8

class Color(Enum):
    WHITE = 1
    BLACK = 1
    
class Position:
    _registries = list()
    def __init__(self, line:int, column:int, isFree:bool = True):
        """Create a case

        Args:
            line (int): indice of the case
            column (int): column of the case
            isFree (bool, optional): state of the case (if it's occupied or not) Defaults to True.
        """
        line -= 1
        column -= 1
        error_message = "invalid value"
        if line  > 7 or line < 0:
            raise TypeError("line " + error_message)
        if column  > 7 or column < 0:
            raise TypeError("line " + error_message)
        
        self.line = line
        self.column = column
        self.free = isFree
        pass
    
    def __eq__(self, other) -> bool:
        return self.column == other.column and self.line == other.line
    
    def isFree(self)->bool:
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
    
    def  isthreatened(self, color:Color)->bool:
        """know if the case is threatened by a given color

        Args:
            color (Color): the color that is suppose to threat the position 

        Returns:
            bool: True if the position is threatened and False otherwise
        """
        opponentPiecesList:list[Piece] = Piece.getColorPieceList(color)
        for opponentPiece in opponentPiecesList:
            if opponentPiece.isAlive():
                targets: list[Position] = opponentPiece.getMoveList()
                for position in targets:
                    if self == position:
                        return True
        return False

class Piece(ABC):
    _registry = {
        "white": [],
        "black": []
    }
    
    def __init__(self, color:Color, position:Position = Position(1, 1, True), state:bool = True):
        """initialize a piece

        Args:
            position (Position, optional): initial position of the piece. Defaults to Position(1, 1, True).
            state (bool, optional): True if the piece is alive False if it's dead. Defaults to True.
            color(Color): WHITE or BLACK
        Raises:
            TypeError: the position of the piece your trying to save is currently occupied
        """
        
        if not position.isFree():
            raise TypeError(f"position not available")
        self.state :bool = True
        self.position :Position = position
        self.color: Color = color
        if color == Color.BLACK:
            self._registry['black'].append(self)
        else:
            self._registry['white'].append(self)
        pass
  
    def getOpponentList(self):
        if self.color == Color.WHITE:
            return self._registry['black']
        return self._registry['white']
    
    @classmethod
    def getColorPieceList(cls, color: Color)->list[_.Piece]:
        """return all the living pieces of a given color


        Args:
            color (Color): the color of the pieces you want

        Returns:
            list[_.Piece]: list of pieces
        """
        strColor = "white" if color == Color.WHITE else Color.BLACK
        return  [element for element in cls._registry[strColor] if element.isAlive()]
    
    def setDead(self):
        """Set the piece as dead
        """
        self.state = False
        pass
    
    def isAlive(self)->bool:
        """get the statut of the piece

        Returns:
            bool: True if the piece is still alive
        """
        return self.state
    
    @abstractmethod
    def move(newPosition:Position)->bool:
        """change the position of the piece

        Args:
            newPosition (Position): The new position of the piece

        Returns:
            bool: True if the position was free and False otherwise
        """
        pass
    
    @abstractmethod
    def getMoveList()->list:
        """Get the list of possible move

        Returns:
            list: possible moves
        """
        pass
    
class king(Piece):
    def __init__(self, position: Position = Position(1, 1, True), state: bool = True):
        super().__init__(position, state)
    
    def getMoveList(self) -> list:
        datas = list()
        #list of move modifications
        mouvement = list()
        position = self.position
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                position = position
                            
        return datas

class Pawn(Piece):
    def __init__(self, position: Position = Position(1, 1, True), state: bool = True):
        super().__init__(position, state)
    def move():
        pass
    def promotion():
        pass

class Chess:
    """Class to handle the game play
    """
    def __init__(self, whitePieces:list[Piece] = None, blackPieces:list[Piece] = None, currentTurn = Color.WHITE) -> None:
        #set current turn (white or black)
        self.turn:Color = currentTurn
        #creating the pieces(dict of list)
        self.pieces:dict[str, list] = dict()
        #creating the board (dict of list 8*8)
        self.board:dict[str, list] = dict()
        for i in range(CHESS_SIZE):
            self.board[COLUMN] = list()
            self.board[COLUMN] = [Position(i, j) for j in range(CHESS_SIZE)]
        #init pieces. if whitePieces not defined then all pices are set by default
        if not whitePieces:
            colorLine= 0
            colorLine:list[int] = [1, 6]
            for color in Color:
                for i in range(8):
                    line  = colorLine[colorLine]
                    position:Position = self.board[COLUMN[i]][line]
                    self.pieces[color.name].append(Pawn(color = color, position = position))
        else:
            self.pieces[Color.WHITE] = whitePieces
            self.pieces[Color.BLACK] = blackPieces
        