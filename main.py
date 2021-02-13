import pygame
from TETRIS import Tetris


pygame.init()
screen = pygame.display.set_mode((600,675))
game_screen = pygame.Surface((10 * 33, 20 * 33))
Tetris = Tetris(screen,game_screen)
Tetris.main_menu()
# ffff