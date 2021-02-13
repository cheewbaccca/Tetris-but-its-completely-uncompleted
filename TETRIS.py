from copy import deepcopy
from random import randint

import pygame
import pygame_menu


class Tetris:
    KADR = 60
    KLETKA = 33
    size = (10, 20)
    figures_list = [[(0, 1), (-1, 0), (0, 0), (1, 1)],  # координаты фигур
                    [(0, 0), (0, 1), (0, -1), (-1, 1)],
                    [(0, 0), (-1, 0), (0, -1), (1, -1)],
                    [(0, 0), (0, 1), (0, -1), (1, 1)],
                    [(-1, 0), (-2, 0), (0, 0), (1, 0)],
                    [(0, 0), (0, -1), (1, 0), (-1, 0)],
                    [(0, -1), (-1, -1), (-1, 0), (0, 0)]]

    def __init__(self, screen, game_screen):
        self.level = 8  # текущий уровень
        self.screen, self.game_screen = screen, game_screen
        self.scores_dict = {0: 0, 1: 100 * self.level, 2: 300 * self.level, 3: 500 * self.level,
                            4: 800 * self.level}  # очки за сожженые линии
        self.moving_speed, self.delay_capacity = 360, 5600
        self.new_figure = True
        self.x, self.y = self.size[0] * self.KLETKA, self.size[1] * self.KLETKA
        self.pause = True
        self.delay = 0
        self.delay_x = 0
        self.board = [[0] * self.size[0] for y in range(self.size[1])]  # игровое поле
        self.score = 0  # очки
        self.max_score = 0
        self.timer = pygame.time.Clock()
        self.all_lines = 0  # количество всех сожженых линий
        self.background_image = pygame.image.load(r'Design\tetramino.jpg').convert()
        self.figure = Shape(randint(0, 6))  # первая рандомная фигура
        self.font_for_title = pygame.font.Font(r'Design\10967.otf', 40)
        self.font_for_score = pygame.font.Font(r'Design\10967.otf', 20)
        self.tetris_title = self.font_for_title.render("Tetris", True, (255, 200, 0))
        self.color = (randint(40, 255), randint(40, 255), randint(40, 255))  # рандомный цвет первой фигуры
        self.line = 0  # количество линий,сожженых единоразово

    def granica(self, x, y):  # определение границ поля
        if x < 0 or x == self.x or y + self.KLETKA >= self.y or self.board[y // self.KLETKA + 1][x // self.KLETKA]:
            return True
        return False

    def moving_y(self, shape, before_move):  # Движение по Y

        self.delay += self.moving_speed
        if self.delay > self.delay_capacity:
            self.delay = 0
            for i in range(4):
                shape.figures[i].y += self.KLETKA
                if self.granica(shape.figures[i].x, shape.figures[i].y - 1):
                    for s in range(4):
                        self.board[before_move.figures[s].y // self.KLETKA][
                            before_move.figures[s].x // self.KLETKA] = self.color
                    self.new_figure = True
                    return True

    def redraw_board(self):  # отрисовка поля
        for num, i in enumerate(self.board):
            for num1, j in enumerate(i):
                if j:
                    pygame.draw.rect(self.game_screen, j,
                                     (num1 * self.KLETKA, num * self.KLETKA, self.KLETKA, self.KLETKA))

    def burn(self):  # сжигание линий
        last_one = self.size[1] - 1
        for row in range(len(self.board) - 1, -1, -1):
            count = 0  # счетик клеток
            for x in range(self.size[0]):
                if self.board[row][x]:
                    count += 1

                self.board[last_one][x] = self.board[row][x]
            if count < self.size[0]:
                last_one -= 1
            else:
                self.line += 1
                self.all_lines += 1

    def main_loop(self):  # основной цикл игры
        while True:

            self.blit()
            moving_x = 0
            self.line = 0

            if self.new_figure:  # новая фигура
                self.new_figure = False

                next_figure = Shape(randint(0, 6))  # следующая фигура
                next_color = (randint(40, 255), randint(40, 255), randint(40, 255))
            self.game_screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.figure.right_left['left'] = True
                    elif event.key == pygame.K_RIGHT:
                        self.figure.right_left['right'] = True
                    elif event.key == pygame.K_SPACE:
                        if self.pause:
                            self.pause = False
                        else:
                            self.pause = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.figure.right_left['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        self.figure.right_left['right'] = False
                if event.type == pygame.KEYUP:

                    if self.figure.number != 6:  # поворот фигур(алгоритм на форумах)
                        if event.key == pygame.K_x:
                            self.figure.rotate_po(self.figure)
                            for i in range(4):
                                if self.granica(self.figure.figures[i].x, self.figure.figures[i].y):
                                    self.figure = deepcopy(before_move)
                        elif event.key == pygame.K_z:
                            self.figure.rotate_protiv(self.figure)
                            for i in range(4):
                                if self.granica(self.figure.figures[i].x, self.figure.figures[i].y):
                                    self.figure = deepcopy(before_move)
            if self.figure.right_left['right']:
                moving_x += self.KLETKA
            elif self.figure.right_left['left']:
                moving_x -= self.KLETKA
            before_move = deepcopy(self.figure)
            self.delay_x += 560  # задержка по X
            if self.delay_x > 2400:
                self.delay_x = 0
                for i in range(4):
                    self.figure.figures[i].x += moving_x
                    if self.granica(self.figure.figures[i].x, self.figure.figures[i].y):
                        self.figure = deepcopy(before_move)
                        break

            self.moving_y(self.figure, before_move)  # движение по Y

            if self.moving_y(self.figure, before_move):  # если фигура упала,рисуется следующая
                self.figure = deepcopy(next_figure)
                self.figure = deepcopy(next_figure)
                next_figure = Shape(randint(0, 6))
                self.color = next_color
                next_color = (randint(40, 255), randint(40, 255), randint(40, 255))

            self.burn()
            self.score += self.scores_dict[self.line]

            for rect in range(4):  # рисование фигуры
                pygame.draw.rect(self.game_screen, self.color, before_move.figures[rect])
            for rect in range(4):  # рисование следующей фигуры
                pygame.draw.rect(self.screen, next_color, (
                    next_figure.figures[rect].x + 250, next_figure.figures[rect].y + 400, self.KLETKA - 1,
                    self.KLETKA - 1))

            self.redraw_board()  # рисование поля

            self.endgame()
            # сетка
            [pygame.draw.rect(self.game_screen, (120, 120, 120),
                              (x * self.KLETKA, y * self.KLETKA, self.KLETKA, self.KLETKA), 1)
             for x in range(self.size[0]) for y in range(self.size[1])]

            pygame.display.flip()
            self.timer.tick(self.KADR)

    def main_menu(self):  # главное меню
        myimage = pygame_menu.baseimage.BaseImage(
            image_path=r'Design\TEST.jpg',
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_SIMPLE,
            drawing_offset=(0, 0))
        mytheme = pygame_menu.themes.Theme(background_color=myimage,  # Тема
                                           title_shadow=True)
        mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        mytheme.widget_font_color = 200, 200, 200
        mytheme.widget_font = pygame_menu.font.FONT_8BIT
        menu = pygame_menu.Menu(675, 600, '',
                                theme=mytheme)

        label = pygame_menu.widgets.Label('TETRIS')
        label.set_position(100, 100)
        label.set_background_color((255, 255, 255))
        menu.add_text_input('Your name is ', default='123')
        menu.add_button('START THE GAME', self.start_the_game)
        menu.add_selector('Select level',
                          [('8', 320), ('9', 360),
                           ('10', 400), ('11', 440),
                           ('12', 480), ('13', 520),
                           ('14', 540), ('15', 580)], onchange=self.level_change)
        menu.add_button('QUIT', pygame_menu.events.EXIT, button_id='Exit')
        menu.mainloop(self.screen)

    def start_the_game(self):
        self.screen.fill((0, 0, 0))
        self.main_loop()

    def endgame(self):  # конец игры
        for i in range(self.size[0]):
            if self.board[0][i]:
                self.board = [[0] * self.size[0] for y in range(self.size[1])]
                self.pause = True
        if self.pause:
            pygame.time.wait(100)

    def level_change(self, level, speed):  # смена уровня
        self.moving_speed = speed
        self.level = int(level[0][0])
        self.scores_dict = {0: 0, 1: 100 * self.level, 2: 300 * self.level, 3: 500 * self.level, 4: 800 * self.level}

    def blit(self):
        self.screen.blit(self.background_image, (-450, -400))
        self.screen.blit(self.game_screen, (10, 10))
        self.screen.blit(self.tetris_title, (350, 5))
        self.screen.blit(self.font_for_score.render(f"Score {self.score}", True, (0, 255, 0)), (350, 600))
        self.screen.blit(self.font_for_score.render(f"Max Score {self.max_score}", True, (0, 255, 0)), (350, 630))
        self.screen.blit(self.font_for_score.render(f"Next shape", True, (0, 255, 0)), (350, 370))
        self.screen.blit(self.font_for_score.render(f"Lines {self.all_lines}", True, (0, 255, 0)), (350, 300))

class Shape:
    KLETKA = 33

    def __init__(self, number):
        self.number = number
        self.figures = []  # список Rect-ов,из которых состоят фигура
        self.right_left = {'right': False, 'left': False}
        for pos_x, pos_y in Tetris.figures_list[number]:
            self.figures.append(
                pygame.Rect(pos_x * self.KLETKA + self.KLETKA * 5, pos_y * self.KLETKA + self.KLETKA, self.KLETKA,
                            self.KLETKA))

    def rotate_po(self, figure):  # вращение по часовой стрелке
        pxy = figure.figures[0]  # центр вращения
        for i in range(4):
            x = pxy.x + pxy.y - figure.figures[i].y
            y = pxy.y + figure.figures[i].x - pxy.x
            figure.figures[i].x = x
            figure.figures[i].y = y

    def rotate_protiv(self, figure):  # вращение против часовой стрелки
        pxy = figure.figures[0]  # центр вращения
        for i in range(4):
            x = figure.figures[i].y + pxy.x - pxy.y
            y = pxy.x + pxy.y - figure.figures[i].x
            figure.figures[i].x = x
            figure.figures[i].y = y


