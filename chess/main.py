import pygame

from entities import *
from display_tools import *
from pygame.locals import *
from entities import Color as entities_color
from chess import Chess
from piece import *


chess = Chess()
# printBoard(chess.board)
chess.selected(("e", 1), chess.board)
chess.selected(("e", 3), chess.board)
chess.selected(("f", 6), chess.board)
chess.selected(("f", 4), chess.board)
chess.selected(("f", 0), chess.board)
chess.selected(("e", 1), chess.board)
chess.selected(("g", 6), chess.board)
chess.selected(("g", 4), chess.board)
chess.selected(("e", 1), chess.board)
chess.selected(("h", 4), chess.board)
gameOver, message = chess.testGameOver()
# print(f"gameOver = {gameOver}\n{message}")
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode(SCREEN)
print(BOARD_PADDING)

# load images
pieces_images: dict[entities_color, dict] = dict()
pieces_images[entities_color.WHITE] = dict()
pieces_images[entities_color.BLACK] = dict()

pieces_images[entities_color.WHITE][Pawn.__name__] = pygame.image.load(
    f"{IMG_LOC}/w_pawn_png_128px.png"
)
pieces_images[entities_color.BLACK][Pawn.__name__] = pygame.image.load(
    f"{IMG_LOC}/b_pawn_png_128px.png"
)

pieces_images[entities_color.WHITE][Rook.__name__] = pygame.image.load(
    f"{IMG_LOC}/w_rook_png_128px.png"
)
pieces_images[entities_color.BLACK][Rook.__name__] = pygame.image.load(
    f"{IMG_LOC}/b_rook_png_128px.png"
)

pieces_images[entities_color.WHITE][Bishop.__name__] = pygame.image.load(
    f"{IMG_LOC}/w_bishop_png_128px.png"
)
pieces_images[entities_color.BLACK][Bishop.__name__] = pygame.image.load(
    f"{IMG_LOC}/b_bishop_png_128px.png"
)

pieces_images[entities_color.WHITE][Knight.__name__] = pygame.image.load(
    f"{IMG_LOC}/w_knight_png_128px.png"
)
pieces_images[entities_color.BLACK][Knight.__name__] = pygame.image.load(
    f"{IMG_LOC}/b_knight_png_128px.png"
)

pieces_images[entities_color.WHITE][King.__name__] = pygame.image.load(
    f"{IMG_LOC}/w_king_png_128px.png"
)
pieces_images[entities_color.BLACK][King.__name__] = pygame.image.load(
    f"{IMG_LOC}/b_king_png_128px.png"
)

pieces_images[entities_color.WHITE][Queen.__name__] = pygame.image.load(
    f"{IMG_LOC}/w_queen_png_128px.png"
)
pieces_images[entities_color.BLACK][Queen.__name__] = pygame.image.load(
    f"{IMG_LOC}/b_queen_png_128px.png"
)


for color in entities_color:
    for pieces_key in pieces_images[color]:
        pieces_images[color][pieces_key] = pygame.transform.scale(
            pieces_images[color][pieces_key], (PIECE_LEN, PIECE_LEN)
        )


# initialisations


pygame.init()

running = True

while running:
    # set the background color
    screen.fill(WIN_BACKGROUND)
    # set the play zone background color
    pygame.draw.rect(screen, BOARD_BG, BOARD_RECT)

    # display the game
    for i in range(len(COLUMN)):
        for j in range(CHESS_SIZE):
            position = chess.board[COLUMN[i]][j]
            boxColor = LIGHT_BOX_BG if not (i + j) % 2 else DARK_BOX_BG
            blit_box(position, boxColor, screen)

            # position_x = int(BOARD_X + BOARD_PADDING / 2 + i * BOX_LEN)
            # position_y = int(BOARD_Y + BOARD_PADDING / 2 + j * BOX_LEN)
            # box_rect = position_x, position_y, BOX_LEN, BOX_LEN
            # pygame.draw.rect(screen, box_color, box_rect)
    for color in entities_color:
        for piece in chess.pieces[color.name]:
            line = piece.position.line
            column = piece.position.column
            position_x = int(
                BOARD_X + BOARD_PADDING / 2 + column * BOX_LEN + BOX_PADDING / 2
            )
            position_y = int(
                BOARD_H
                + BOARD_Y
                - BOARD_PADDING / 2
                - (line + 1) * BOX_LEN
                + BOX_PADDING / 2
            )
            screen.blit(
                pieces_images[color][piece.__class__.__name__], (position_x, position_y)
            )
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            print(position)
            position = getCaseIndex(position, chess.board)
            print(type(chess.board))
            print(position)
            chess.selected(position, chess.board)
            print(chess.gameOver)
            if chess.gameOver:
                print("game over")

                pygame.display.set_caption(chess.message)


pygame.quit()
