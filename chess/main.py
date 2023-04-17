from entities import *
import pygame
from pygame.locals import *
BACKGROUND = (250, 250, 250)
TITLE = "CHESS by Vysti"
HEIGHT = 800
WIDTH  = 800
SCREEN = (WIDTH, HEIGHT)

pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode(SCREEN)
screen.fill(BACKGROUND)
pygame.display.update()

chess = Chess()
print(chess.board.values())
for i in range(8):
    for column in chess.board.values():
        print(f"{column[i].piece}\t", end=" ")
        # print(f"{column}")
    print("")
raise TypeError("check")
print(len(chess.board))  

pygame.init()

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()