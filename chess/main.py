from entities import *
import pygame
from pygame.locals import *

#vars definitions
WIN_BACKGROUND = (250, 250, 250)
LIGHT_BOX_BG = WIN_BACKGROUND
DARK_BOX_BG = (200, 200, 200)
TITLE = "CHESS by Vysti"
SCREEN = WIDTH, HEIGHT = (700, 600)
BOARD_W, BOARD_H = (int(WIDTH/1.4), int(HEIGHT/1.2))
BOARD_X, BOARD_Y = (int((WIDTH-BOARD_W)/2), int((HEIGHT-BOARD_H)/2))
BOARD_RECT = (BOARD_X, BOARD_Y, BOARD_W, BOARD_H)
BOARD_BG= (50, 50, 50)
IMG_LOC = "sprites/JohnPablok_Cburnett_Chess_set/PNGs/128h"

pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode(SCREEN)


#load images
white_pawn = pygame.image.load(f"{IMG_LOC}/w_pawn_png_128px.png")
white_pawn.convert()
black_pawn = pygame.image.load(f"{IMG_LOC}/b_pawn_png_128px.png")
# black_pawn.convert()

white_rook = pygame.image.load(f"{IMG_LOC}/w_rook_png_128px.png")
white_rook.convert()
black_rook = pygame.image.load(f"{IMG_LOC}/b_rook_png_128px.png")
black_rook.convert()

white_bishop = pygame.image.load(f"{IMG_LOC}/w_bishop_png_128px.png")
white_bishop.convert()
black_bishop = pygame.image.load(f"{IMG_LOC}/b_bishop_png_128px.png")
black_bishop.convert()

white_knight = pygame.image.load(f"{IMG_LOC}/w_knight_png_128px.png")
white_knight.convert()
black_knight = pygame.image.load(f"{IMG_LOC}/b_knight_png_128px.png")
black_knight.convert()

white_king = pygame.image.load(f"{IMG_LOC}/w_king_png_128px.png")
white_king.convert()
black_king = pygame.image.load(f"{IMG_LOC}/b_king_png_128px.png")
black_king.convert()

white_queen = pygame.image.load(f"{IMG_LOC}/w_queen_png_128px.png")
white_queen.convert()
black_queen = pygame.image.load(f"{IMG_LOC}/b_queen_png_128px.png")
black_queen.convert()


#funcitons definitions
def printBoard(board:dict[str, list])->None:
    for i in range(8):
        for column in board.values():
            print(f"{column[i].piece}\t", end=" ")
        print("")    

# position = black_pawn.get_rect()
position = 50, 50
#initialisations
pygame.init()

running = True





chess = Chess()
printBoard(chess.board)

while running:
    screen.fill(WIN_BACKGROUND)
    pygame.draw.rect(
        screen,
        BOARD_BG,
        BOARD_RECT
    )
    screen.blit(black_pawn, position)
    screen.blit(black_pawn, (100,100))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()