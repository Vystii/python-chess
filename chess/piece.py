from entities import *


class King(Piece):
    def __init__(
        self,
        color: Color,
        position: Position = Position(0, 0, True),
        state: bool = True,
    ):
        super().__init__(color, position, state)

    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas: list = list()

        # list of move modifications
        positions = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column

        positions.append([])
        if pieceLine:
            positions[0].append((COLUMN[pieceColumn], pieceLine - 1))
        if pieceLine - 1 < CHESS_SIZE:
            positions[0].append((COLUMN[pieceColumn], pieceLine + 1))

        if pieceColumn - 1 < CHESS_SIZE:
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
        print(positions)
        for axe in positions:
            for coordonnates in axe:
                position: Position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree():
                    datas.append(position)
                else:
                    if not position.piece.color == self.color:
                        datas.append(position)
                    break
        return datas


class Rook(Piece):
    def __init__(
        self,
        color: Color,
        position: Position = Position(1, 1, True),
        state: bool = True,
    ):
        super().__init__(color, position, state)

    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column
        # creating coordonnate to check
        positions = list()
        positions.append(
            [(COLUMN[pieceColumn], i) for i in range(pieceLine - 1, -1, -1)]
        )
        positions.append(
            [(COLUMN[pieceColumn], i) for i in range(pieceLine + 1, CHESS_SIZE, +1)]
        )
        positions.append(
            [(COLUMN[i], pieceLine) for i in range(pieceColumn - 1, -1, -1)]
        )
        positions.append(
            [(COLUMN[i], pieceLine) for i in range(pieceColumn + 1, CHESS_SIZE, +1)]
        )
        # check coordonnate
        for axe in positions:
            for coordonnates in axe:
                position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree():
                    datas.append(position)
                else:
                    if not position.piece.color == self.color:
                        datas.append(position)
                    break
        return datas


class Bishop(Piece):
    def __init__(
        self,
        color: Color,
        position: Position = Position(1, 1, True),
        state: bool = True,
    ):
        super().__init__(color, position, state)

    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column

        # creating coordonnate to check
        positions: list = list()
        lower = min(pieceLine, pieceColumn)
        upper = max(pieceLine, pieceColumn)
        positions.append(
            [
                (COLUMN[pieceColumn + i + 1], pieceLine + i + 1)
                for i in range(CHESS_SIZE - upper)
                if pieceColumn + i + 1 < CHESS_SIZE and pieceLine + i + 1 < CHESS_SIZE
            ]
        )
        positions.append(
            [
                (COLUMN[pieceColumn - i - 1], pieceLine - i - 1)
                for i in range(lower)
                if pieceColumn - i - 1 < CHESS_SIZE and pieceLine - i - 1 < CHESS_SIZE
            ]
        )
        lower = min(pieceLine, CHESS_SIZE - pieceColumn)
        positions.append(
            [
                (COLUMN[pieceColumn + i + 1], pieceLine - i - 1)
                for i in range(lower)
                if pieceColumn + i + 1 < CHESS_SIZE and pieceLine - i - 1 < CHESS_SIZE
            ]
        )
        lower = min(CHESS_SIZE - pieceLine, pieceColumn)
        positions.append(
            [
                (COLUMN[pieceColumn - i - 1], pieceLine + i + 1)
                for i in range(lower)
                if pieceColumn - i - 1 < CHESS_SIZE and pieceLine + i + 1 < CHESS_SIZE
            ]
        )
        # check coordonnate
        for axe in positions:
            for coordonnates in axe:
                position: Position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree():
                    datas.append(position)
                else:
                    if not position.piece.color == self.color:
                        datas.append(position)
                    break
        return datas


class Knight(Piece):
    def __init__(
        self,
        color: Color,
        position: Position = Position(1, 1, True),
        state: bool = True,
    ):
        super().__init__(color, position, state)

    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column
        positions: list = list()
        indice = len(positions) - 1
        if pieceLine < CHESS_SIZE - 2:
            positions.append([])
            if pieceColumn < CHESS_SIZE - 1:
                positions[indice].append((COLUMN[pieceColumn + 1], pieceLine + 2))
            if pieceColumn:
                positions[indice].append((COLUMN[pieceColumn - 1], pieceLine + 2))
        indice = len(positions) - 1
        if pieceLine > 1:
            positions.append([])
            if pieceColumn < CHESS_SIZE - 1:
                positions[indice].append((COLUMN[pieceColumn + 1], pieceLine - 2))
            if pieceColumn:
                positions[indice].append((COLUMN[pieceColumn - 1], pieceLine - 2))
        indice = len(positions) - 1
        if pieceColumn < CHESS_SIZE - 2:
            positions.append([])
            if pieceLine < CHESS_SIZE - 1:
                positions[indice].append((COLUMN[pieceColumn + 2], pieceLine + 1))
            if pieceLine:
                positions[indice].append((COLUMN[pieceColumn + 2], pieceLine - 1))
        indice = len(positions) - 1
        if pieceColumn > 1:
            positions.append([])
            if pieceLine < CHESS_SIZE - 1:
                positions[indice].append((COLUMN[pieceColumn - 2], pieceLine + 1))
            if pieceLine:
                positions[indice].append((COLUMN[pieceColumn - 2], pieceLine - 1))

        # check coordonnate
        for axe in positions:
            for coordonnates in axe:
                position: Position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree() or not position.piece.color == self.color:
                    datas.append(position)

        return datas


class Queen(Piece):
    def __init__(
        self,
        color: Color,
        position: Position = Position(1, 1, True),
        state: bool = True,
    ):
        super().__init__(color, position=position, state=state)

    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas: list = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column

        # creating coordonnate to check
        positions = list()
        lower = min(pieceLine, pieceColumn)
        upper = max(pieceLine, pieceColumn)
        positions.append(
            [
                (COLUMN[pieceColumn + i + 1], pieceLine + i + 1)
                for i in range(CHESS_SIZE - upper)
                if pieceColumn + i + 1 < CHESS_SIZE and pieceLine + i + 1 < CHESS_SIZE
            ]
        )
        positions.append(
            [
                (COLUMN[pieceColumn - i - 1], pieceLine - i - 1)
                for i in range(lower)
                if pieceColumn - i - 1 < CHESS_SIZE and pieceLine - i - 1 < CHESS_SIZE
            ]
        )
        lower = min(pieceLine, CHESS_SIZE - pieceColumn)
        positions.append(
            [
                (COLUMN[pieceColumn + i + 1], pieceLine - i - 1)
                for i in range(lower)
                if pieceColumn + i + 1 < CHESS_SIZE and pieceLine - i - 1 < CHESS_SIZE
            ]
        )
        lower = min(CHESS_SIZE - pieceLine, pieceColumn)
        positions.append(
            [
                (COLUMN[pieceColumn - i - 1], pieceLine + i + 1)
                for i in range(lower)
                if pieceColumn - i - 1 < CHESS_SIZE and pieceLine + i + 1 < CHESS_SIZE
            ]
        )

        positions.append(
            [(COLUMN[pieceColumn], i) for i in range(pieceLine - 1, -1, -1)]
        )
        positions.append(
            [(COLUMN[pieceColumn], i) for i in range(pieceLine + 1, CHESS_SIZE, +1)]
        )
        positions.append(
            [(COLUMN[i], pieceLine) for i in range(pieceColumn - 1, -1, -1)]
        )
        positions.append(
            [(COLUMN[i], pieceLine) for i in range(pieceColumn + 1, CHESS_SIZE, +1)]
        )
        # check coordonnate
        for axe in positions:
            for coordonnates in axe:
                position: Position = board[coordonnates[0]][coordonnates[1]]
                if position.isFree():
                    datas.append(position)
                else:
                    if not position.piece.color == self.color:
                        datas.append(position)
                    break
        return datas


class Pawn(Piece):
    def __init__(
        self,
        color: Color,
        position: Position = Position(0, 0, True),
        state: bool = True,
        moved: bool = False,
    ):
        self.moved = moved
        super().__init__(color, position, state)

    def move(self, newPosition: Position, board: dict[str, list[Position]]) -> None:
        self.moved = False
        super().move(newPosition, board)

    def getMoveList(self, board: dict[str, list[Position]]) -> list:
        datas: list = list()
        pieceLine = self.position.line
        pieceColumn = self.position.column
        direction = 1 if self.color == Color.WHITE else -1
        # the box right in front of the pawn
        position: Position = board[COLUMN[pieceColumn]][pieceLine + direction]
        if position.isFree():
            datas.append(position)

        if pieceColumn:
            position = board[COLUMN[pieceColumn - 1]][pieceLine + direction]
            if not position.isFree():
                datas.append(position)
        if pieceColumn + 1 < CHESS_SIZE:
            position = board[COLUMN[pieceColumn + 1]][pieceLine + direction]
            if not position.isFree():
                datas.append(position)
        if not self.moved:
            position = board[COLUMN[pieceColumn]][pieceLine + 2 * direction]
            if position.isFree():
                datas.append(position)
        return datas
