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
        self.position :Position = position()
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
    
    def move(self, newPosition:Position, board:dict[str, list[Position]])->bool:
        """change the position of the piece

        Args:
            newPosition (Position): The new position of the piece

        Returns:
            bool: True if the position was free and False otherwise
        """
        canGo = self.getMoveList()
        if not (newPosition in canGo):
            raise TypeError("this piece can't go to the given position")
        self.position = newPosition
        return True
    
    @abstractmethod
    def getMoveList(self, board:dict[str, list[Position]])->list:
        """Get the list of possible move

        Returns:
            list: possible moves
        """
        pass

    
    
class King(Piece):
    def __init__(self, position: Position = Position(1, 1, True), state: bool = True):
        super().__init__(position, state)
    
    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas :list = list()
        
        #list of move modifications
        positions = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column
        
        positions.append([])
        if pieceLine:
            positions[0].append((COLUMN[pieceColumn], pieceLine - 1))
        if pieceLine - 1 < CHESS_SIZE:
                positions[0].append((COLUMN[pieceColumn], pieceLine + 1))
                
                
        if pieceColumn - 1  < CHESS_SIZE:
            positions.append([(COLUMN[pieceColumn + 1], pieceLine)])
            if pieceLine:
                positions[1].append((COLUMN[pieceColumn + 1], pieceLine - 1))
            if pieceLine - 1 < CHESS_SIZE:
                positions[1].append((COLUMN[pieceColumn + 1], pieceLine + 1))
        if pieceColumn:
            positions.append([(COLUMN[pieceColumn - 1], pieceLine)])
            if pieceLine:
                positions[2].append((COLUMN[pieceColumn - 1], pieceLine - 1))
            if pieceLine - 1 < CHESS_SIZE:
                positions[2].append((COLUMN[pieceColumn - 1], pieceLine + 1))

        for axe in positions:
            for coordonnates in axe:
                position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree():
                    datas.append(position)
                else:
                    break
        
        return datas

class Rook(Piece):
    def __init__(self, color: Color, position: Position = Position(1, 1, True), state: bool = True):
        super().__init__(color, position, state)
    
    def getMoveList(self, board:dict[str, list[Position]]) -> list:
        datas = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column
        #creating coordonnate to check  
        positions = list()
        positions.append([(COLUMN[pieceColumn], i) for i in range(pieceLine-1, -1, -1)])
        positions.append([(COLUMN[pieceColumn], i) for i in range(pieceLine+1, +1, CHESS_SIZE)])
        positions.append([(COLUMN[i], pieceLine) for i in range(pieceColumn-1, -1, -1)])
        positions.append([(COLUMN[i], pieceLine) for i in range(pieceColumn+1, +1, CHESS_SIZE)])
        #check coordonnate
        for axe in positions:
            for coordonnates in axe:
                position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree():
                    datas.append(position)
                else:
                    break
        return datas

class Bishop(Piece):
    def __init__(self, color: Color, position: Position = Position(1, 1, True), state: bool = True):
        super().__init__(color, position, state)
    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column
        
        #creating coordonnate to check  
        positions:list = list()
        lower = min(pieceLine, pieceColumn)
        upper = max(pieceLine, pieceColumn)
        positions.append([(COLUMN[pieceColumn + i + 1], pieceLine + i + 1) for i in range(CHESS_SIZE - upper)])
        positions.append([(COLUMN[pieceColumn - i - 1], pieceLine - i - 1) for i in range(lower)])
        lower = min(pieceLine, CHESS_SIZE-pieceColumn)
        positions.append([(COLUMN[pieceColumn + i + 1], pieceLine - i - 1) for i in range(lower)])
        lower = (CHESS_SIZE - pieceLine, pieceColumn)
        positions.append([(COLUMN[pieceColumn - i - 1], pieceLine + i + 1) for i in range(lower)])
        
        #check coordonnate
        for axe in positions:
            for coordonnates in axe:
                position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree():
                    datas.append(position)
                else:
                    break
        return datas

class Knight(Piece):
    def __init__(self, color: Color, position: Position = Position(1, 1, True), state: bool = True):
        super().__init__(color, position, state)
    
    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column
        positions:list = list()
        if pieceLine < CHESS_SIZE - 2:
            positions.append([])
            if pieceColumn < CHESS_SIZE - 1:
                positions[0].append((COLUMN[pieceColumn + 1][pieceLine + 2]))
            if pieceColumn:
                positions[0].append((COLUMN[pieceColumn - 1][pieceLine + 2]))
        if pieceLine > 1:
            positions.append([])
            if pieceColumn < CHESS_SIZE - 1:
                positions[1].append((COLUMN[pieceColumn + 1][pieceLine - 2]))
            if pieceColumn:
                positions[1].append((COLUMN[pieceColumn - 1][pieceLine - 2]))

        if pieceColumn < CHESS_SIZE - 2:
            positions.append([])
            if pieceLine < CHESS_SIZE - 1:
                positions[2].append((COLUMN[pieceColumn + 2][pieceLine + 1 ]))
            if pieceLine:
                positions[2].append((COLUMN[pieceColumn + 2][pieceLine - 1]))
        if pieceColumn > 1:
            positions.append([])
            if pieceLine < CHESS_SIZE - 1:
                positions[3].append((COLUMN[pieceColumn - 2][pieceLine + 1]))
            if pieceLine:
                positions[3].append((COLUMN[pieceColumn - 2][pieceLine - 1]))

        #check coordonnate
        for axe in positions:
            for coordonnates in axe:
                position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree():
                    datas.append(position)
                else:
                    break
        
        return datas

class Queen(Piece):
    def __init__(self, color: Color, position: Position = Position(1, 1, True), state: bool = True):
        super().__init__(color, position, state)
        
    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas:list = list()
        pieceLine = self.position.line
        pieceColumn  = self.position.column
        
         #creating coordonnate to check  
        positions = list()
        positions.append([(COLUMN[pieceColumn], i) for i in range(pieceLine-1, -1, -1)])
        positions.append([(COLUMN[pieceColumn], i) for i in range(pieceLine+1, +1, CHESS_SIZE)])
        positions.append([(COLUMN[i], pieceLine) for i in range(pieceColumn-1, -1, -1)])
        positions.append([(COLUMN[i], pieceLine) for i in range(pieceColumn+1, +1, CHESS_SIZE)])
        
        lower = min(pieceLine, pieceColumn)
        upper = max(pieceLine, pieceColumn)
        positions.append([(COLUMN[pieceColumn + i + 1], pieceLine + i + 1) for i in range(CHESS_SIZE - upper)])
        positions.append([(COLUMN[pieceColumn - i - 1], pieceLine - i - 1) for i in range(lower)])
        lower = min(pieceLine, CHESS_SIZE-pieceColumn)
        positions.append([(COLUMN[pieceColumn + i + 1], pieceLine - i - 1) for i in range(lower)])
        lower = (CHESS_SIZE - pieceLine, pieceColumn)
        positions.append([(COLUMN[pieceColumn - i - 1], pieceLine + i + 1) for i in range(lower)])
        
        #check coordonnate
        for axe in positions:
            for coordonnates in axe:
                position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree():
                    datas.append(position)
                else:
                    break
        return datas

class Pawn(Piece):
    def __init__(self, position: Position = Position(1, 1, True), state: bool = True, moved:bool = False):
        self.moved = moved
        super().__init__(position, state)
    
    def move(self)->None:
        self.moved = False
        super().move()
    
    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas :list = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column
        
        position = board[COLUMN[pieceColumn]][pieceLine + 1]
        if position.isFree():
            datas.append(position)
        if pieceColumn:
            position = board[COLUMN[pieceColumn - 1]][pieceLine + 1]
            if not position.isFree():
                datas.append(position)
        if pieceColumn - 1 < CHESS_SIZE:
            position = board[COLUMN[pieceColumn + 1]][pieceLine + 1]
            if not position.isFree():
                datas.append(position)
        if not self.moved:
            position = board[COLUMN[pieceColumn]][pieceLine + 2]
            if position.isFree():
                datas.append(position)
        return datas

class Chess:
    """Class to handle the game play
    """
    def __init__(self, whitePieces:list[Piece] = None, blackPieces:list[Piece] = None, currentTurn = Color.WHITE) -> None:
        """create a chess game

        Args:
            whitePieces (list[Piece], optional): set of all white pieces. Defaults to None. leave it to none to create a default new game
            blackPieces (list[Piece], optional): set of all black pieces. Defaults to None.
            currentTurn (_type_, optional): color of the current player. Defaults to Color.WHITE.
        """
        #set current turn (white or black)
        self.turn:Color = currentTurn
        #creating the pieces(dict of list)
        self.pieces:dict[str, list[Piece]] = dict()
        #point on boot kings
        self.kings:dict[Color, King] = dict()
        #creating the board (dict of list 8*8)
        self.board:dict[str, list] = dict()
        for i in range(CHESS_SIZE):
            self.board[COLUMN[i]] = list()
            self.board[COLUMN[i]] = [Position(i, j) for j in range(CHESS_SIZE)]
        #init pieces. if whitePieces not defined then all pices are set by default
        if not whitePieces:
            for color in Color:
                #creating pawns
                line = 1 if color == Color.WHITE else 6
                for i in range(8):
                    position:Position = self.board[COLUMN[i]][line]
                    self.pieces[color.name].append(Pawn(color = color, position = position))
                    
                #creating Rooks
                colPosition = [0, 7]
                line = 0 if color == Color.WHITE else 7
                for i in range(2):
                    position:Position = self.board[COLUMN[colPosition[i]]][line]
                    self.pieces[color.name].append(Rook(color, position = position))
                
                #creating Knights
                colPosition = [1, 6]
                for i in range(2):
                    position:Position = self.board[COLUMN[colPosition[i]]][line]
                    self.pieces[color.name].append(Knight(color, position = position))
                
                #creating Bishops
                colPosition = [2, 5]
                for i in range(2):
                    position:Position = self.board[COLUMN[colPosition[i]]][line]
                    self.pieces[color.name].append(Bishop(color, position = position))
                
                #creating Queens
                position:Position = self.board[COLUMN[3]][line]
                self.pieces[color.name].append(Queen(color, position = position))
                
                #creating Kings
                position:Position = self.board[COLUMN[4]][line]
                self.kings[color] = King(color, position = position)
                self.pieces[color.name].append(self.kings[color])

        else:
            self.pieces[Color.WHITE] = whitePieces
            self.pieces[Color.BLACK] = blackPieces
    
    def isKingThreatened(self)->bool:
        opponentColor = Color.WHITE if self.turn == Color.BLACK else Color.WHITE
        pieces:list[Piece] = self.pieces[opponentColor]
        threat = False
        for piece in pieces:
            moves = piece.getMoveList()
            if self.kings[self.turn].position in moves:
                threat = True
                break
        return threat