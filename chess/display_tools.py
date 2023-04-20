from entities import Chess, Position, Piece

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
    position: tuple[int], board: dict[str, list[Position]]
) -> tuple(str, int):
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
        or BOARD_X - BOARD_PADDING / 2 < position[0]
        or BOARD_Y + BOARD_PADDING / 2 > position[1]
        or BOARD_Y - BOARD_PADDING < position[1]
    ):
        return None
    column_keys = [key for key in board.keys()]
    column_index = (position[0] - BOARD_X - BOARD_PADDING) // len(column_keys)
    line_index = (position[1] - BOARD_Y - BOARD_PADDING) // len(column_keys)
    return (column_index, line_index)
