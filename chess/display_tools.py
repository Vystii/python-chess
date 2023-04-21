from entities import Position, Piece, CHESS_SIZE, COLUMN
from chess import Chess
import pygame

# vars definitions
TITLE = "CHESS by Vysti"
SCREEN = WIDTH, HEIGHT = (700, 600)
BOARD_W, BOARD_H = (int(WIDTH / 1.4), int(WIDTH / 1.4))
BOARD_X, BOARD_Y = (int((WIDTH - BOARD_W) / 2), int((HEIGHT - BOARD_H) / 2))
BOARD_RECT = (BOARD_X, BOARD_Y, BOARD_W, BOARD_H)
BOARD_PADDING = BOARD_W * 0.04
BOARD_BG = (50, 50, 50)
WIN_BACKGROUND = (250, 250, 250)
LIGHT_BOX_BG = WIN_BACKGROUND
DARK_BOX_BG = (200, 200, 200)
BOX_LEN = int((BOARD_W - BOARD_PADDING) / CHESS_SIZE)
BOX_PADDING = BOX_LEN * 0.2
PIECE_LEN = BOX_LEN - BOX_PADDING

IMAGE_SIZE = 128
SCALE = PIECE_LEN / IMAGE_SIZE

IMG_LOC = "sprites/JohnPablok_Cburnett_Chess_set/PNGs/128h"


# Useful function
def getCaseIndex(
    position: tuple[int, int], board: dict[str, list[Position]]
) -> tuple[str, int]:
    """function to get indexes of the box that have been clicked on

    Args:
        position (tuple[int]): relative coordonnate of the cursor when the clic happened
        board (dict[str, list[Position]]): board containing all the position

    Returns:
        tuple: indexes of the box we are looking for
        None: if the given position were'nt somewhere on the board

    """
    if (
        BOARD_X + BOARD_PADDING / 2 > position[0]
        or BOARD_X + BOARD_W - BOARD_PADDING / 2 < position[0]
        or BOARD_Y + BOARD_PADDING / 2 > position[1]
        or BOARD_Y + BOARD_H - BOARD_PADDING < position[1]
    ):
        return None
    column_keys = [key for key in board.keys()]
    column_index = (position[0] - BOARD_X - BOARD_PADDING) // BOX_LEN
    line_index = (position[1] - BOARD_Y - BOARD_PADDING) // BOX_LEN
    return (COLUMN[int(column_index)], CHESS_SIZE - 1 - int(line_index))


def blit_piece(piece: Piece, screen: pygame.Surface) -> None:
    line = piece.position.line
    column = piece.position.column
    position_x = int(BOARD_X + BOARD_PADDING / 2 + column * BOX_LEN + BOX_PADDING / 2)
    position_y = int(BOARD_Y + BOARD_PADDING / 2 + line * BOX_LEN + BOX_PADDING / 2)
    screen.blit(
        pieces_images[color][piece.__class__.__name__], (position_x, position_y)
    )


def blit_box(
    position: Position, boxColor: tuple[int, int, int], screen: pygame.Surface
) -> None:
    position_x = int(BOARD_X + BOARD_PADDING / 2 + position.column * BOX_LEN)
    position_y = int(BOARD_Y + BOARD_PADDING / 2 + position.line * BOX_LEN)
    box_rect = position_x, position_y, BOX_LEN, BOX_LEN
    pygame.draw.rect(screen, boxColor, box_rect)


# functions definitions
def printBoard(board: dict[str, list]) -> None:
    for i in range(8):
        for column in board.values():
            print(f"{column[i].piece}\t", end=" ")
        print("")
