column = "a b c d e f g h"
COLUMN = column.split(sep=" ")
line = [i+1 for i in range(8)]


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
        self.column = COLUMN[column]
        self.free = isFree
        pass
    def isFree(self)->bool:
        """State of a position (free or not)

        Returns:
            bool: True when the position is available an false otherwise
        """
        return self.free
    

class Piece:
    def __init__(self, position:Position = Position(1, 1, True), state:bool = True):
        """initialize a piece

        Args:
            position (Position, optional): initial position of the piece. Defaults to Position(1, 1, True).
            state (bool, optional): True if the piece is alive False if it's dead. Defaults to True.

        Raises:
            TypeError: the position of the piece your trying to save is currently occupied
        """
        
        if not position.isFree():
            raise TypeError(f"position not available")
        self.state :bool = True
        self.position :Position = position
        pass