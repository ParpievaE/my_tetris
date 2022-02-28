import pygame
import random
import pygame_gui
import sys


def start_screen(screen):
    manager = pygame_gui.UIManager((500, 500), "style.json")
    pygame.display.set_caption("Start")
    intro_text = pygame.image.load("data/game_name_img.png")
    fon = pygame.transform.scale(pygame.image.load('data/fon_img.jpg'), (500, 500))
    difficult = "Легко"
    difficulty = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(  # выбор сложности
        options_list=['Легко', 'Средне', 'Сложно'],
        starting_option='Легко',
        relative_rect=pygame.Rect((110, 200), (100, 25)),
        manager=manager
    )
    name = ""
    entry_name = pygame_gui.elements.UITextEntryLine(  # никнейм
        relative_rect=pygame.Rect((110, 150), (100, 30)),
        manager=manager
    )
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((110, 250), (100, 50)),
        text='Старт',
        manager=manager,

    )
    while True:
        time_delta = pygame.time.Clock().tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED \
                    and event.ui_element == entry_name:
                name = event.text
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return (difficult, name)
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED \
                    and event.ui_element == difficulty:
                difficult = event.text
            if event.type == pygame.QUIT:
                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((130, 180), (300, 200)),
                    manager=manager,
                    window_title="Подтверждение",
                    action_long_desc="Вы уверены, что хотите выйти?",
                    action_short_name='OK',
                    blocking=True
                )

            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                sys.exit(0)
            manager.process_events(event)
        screen.blit(fon, (0, 0))
        screen.blit(pygame.transform.scale(intro_text, (222, 125)), (145, 10))
        fnt = pygame.font.Font(None, 22)
        text1 = fnt.render('Введите имя', True, (0, 0, 0))
        text2 = fnt.render('Сложность', True, (0, 0, 0))
        screen.blit(text1, (5, 155))
        screen.blit(text2, (5, 205))
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 20
        self.color = [(0, 0, 0), (0, 255, 0)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


class Tetris(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.points = 0
        self.shift = 3
        self.board = [[0] * (width + 2 * self.shift) for _ in range(height + 3)]
        for i in range(height, height + 3):
            for j in range(len(self.board[i])):
                self.board[i][j] = 1
        for i in range(height):
            for j in range(self.shift):
                self.board[i][j] = 1
                self.board[i][-j - 1] = 1

        self.board_for_next_f = [[0] * 4 for _ in range(4)]

        self.color = [(0, 0, 0), (0, 255, 255), (0, 0, 255), (255, 104, 0), (255, 255, 0),
                      (0, 255, 0), (255, 0, 0),
                      (255, 0, 255), (255, 255, 255)] + [(255, 255, 255)] * 20
        self.figurs = [
            [  # line
                [  # line1
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0]
                ],
                [  # line2
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            ],
            [  # г
                [  # г1
                    [1, 1, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # г2
                    [1, 0, 0, 0],
                    [1, 1, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # г3
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # г4
                    [0, 0, 0, 0],
                    [1, 1, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 0]
                ]
            ],
            [  # L
                [  # L1
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # L2
                    [0, 0, 1, 0],
                    [1, 1, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # L3
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # L4
                    [0, 0, 0, 0],
                    [1, 1, 1, 0],
                    [1, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            ],
            [  # 0
                [  # 01
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            ],
            [  # s
                [  # s1
                    [0, 1, 1, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # s2
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ]
            ],
            [  # z
                [  # z1
                    [1, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # z2
                    [0, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            ],
            [  # t
                [  # t1
                    [0, 0, 0, 0],
                    [1, 1, 1, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # t2
                    [0, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # t3
                    [0, 1, 0, 0],
                    [1, 1, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                [  # t4
                    [0, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ]
            ]
        ]
        self.current_figure = [[0, 5 + self.shift], 1, 0]
        self.next_tipe = random.randint(0, len(self.figurs) - 1)
        self.next_rotate = random.randint(0, len(self.figurs[self.next_tipe]) - 1)
        self.next_figure = [[0, 5 + self.shift], self.next_tipe, self.next_rotate]
        self.new_figure()

    def render(self, screen):
        manager = pygame_gui.UIManager((500, 500), "style.json")
        to_start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((110, 250), (100, 50)),
            text='Меню',
            manager=manager,
        )
        font = pygame.font.Font(None, 20)
        text = font.render("Points: " + str(self.points), True, (255, 255, 255))
        pos = [260, 140]
        screen.blit(text, (365, 40))
        instruction = ['Для поворота:  ^',
                       'Движения:  <  >',
                       'Ускоренного спускания:  v',
                       'Для паузы нажмите пробел',
                       'Для остановки музыки нажмите 1']
        for elem in instruction:
            font = pygame.font.Font(None, 20)
            text = font.render(elem, True, (255, 255, 255))
            screen.blit(text, (pos[0], pos[1]))
            pos[1] += 30

        x = self.left
        y = self.top
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x, y, self.cell_size, self.cell_size), width=1)
                pygame.draw.rect(screen, self.color[self.board[i][j + self.shift]],
                                 (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2), width=0)
                x += self.cell_size
            x = self.left
            y += self.cell_size

        x2 = self.left + (self.width + 1) * self.cell_size
        y2 = self.top
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x2, y2, self.cell_size, self.cell_size), width=1)
                pygame.draw.rect(screen, self.color[
                    (self.figurs[self.next_tipe][self.next_rotate][i][j]) * (self.next_tipe + 1)],
                                 (x2 + 1, y2 + 1, self.cell_size - 2, self.cell_size - 2), width=0)
                x2 += self.cell_size
            x2 = self.left + (self.width + 1) * self.cell_size
            y2 += self.cell_size

    def new_figure(self):
        self.current_figure = self.next_figure
        self.next_tipe = random.randint(0, len(self.figurs) - 1)
        self.next_rotate = random.randint(0, len(self.figurs[self.next_tipe]) - 1)
        self.next_figure = [[0, 5 + self.shift], self.next_tipe, self.next_rotate]
        if self.intersection():
            print('game over')
            pygame.mixer.music.stop()
            game_over.play()
            print(self.points)
            self.put()
            pygame.time.set_timer(MYEVENTTYPE, 0)
        else:
            self.put()

    def put(self):
        ci, cj = self.current_figure[0]
        type = self.current_figure[1]
        rotation = self.current_figure[2]
        color = type + 1
        for i in range(4):
            for j in range(4):
                self.board[ci + i][cj + j] += color * self.figurs[type][rotation][i][j]

    def erase(self):
        ci, cj = self.current_figure[0]
        type = self.current_figure[1]
        rotation = self.current_figure[2]
        color = type + 1
        for i in range(4):
            for j in range(4):
                self.board[ci + i][cj + j] -= color * self.figurs[type][rotation][i][j]

    def intersection(self):
        ci, cj = self.current_figure[0]
        type = self.current_figure[1]
        rotation = self.current_figure[2]
        color = type + 1
        is_intersection = False
        for i in range(4):
            for j in range(4):
                is_intersection = is_intersection \
                                  or (self.board[ci + i][cj + j] * self.figurs[type][rotation][i][
                    j] > 0)
        return is_intersection

    def move_down(self):
        self.erase()
        self.current_figure[0][0] += 1
        if self.intersection():
            self.current_figure[0][0] -= 1
            self.put()
            self.kill_line()
            self.new_figure()
        else:
            self.put()

    def rotation(self):
        self.erase()
        self.current_figure[2] = (self.current_figure[2] + 1) % len(
            self.figurs[self.current_figure[1]])
        if self.intersection():
            if self.current_figure[0][1] < self.shift:
                self.current_figure[0][1] += 1
            elif self.current_figure[0][1] > self.width - 5:
                self.current_figure[0][1] -= 1
                if self.intersection():
                    self.current_figure[0][1] -= 1
                    if self.intersection():
                        self.current_figure[0][1] += 2
                        self.current_figure[2] = (self.current_figure[2] - 1) % len(
                            self.figurs[self.current_figure[1]])
            else:
                self.current_figure[2] = (self.current_figure[2] - 1) % len(
                    self.figurs[self.current_figure[1]])
        self.put()

    def move_left(self):
        self.erase()
        self.current_figure[0][1] -= 1
        if self.intersection():
            self.current_figure[0][1] += 1
        self.put()

    def move_right(self):
        self.erase()
        self.current_figure[0][1] += 1
        if self.intersection():
            self.current_figure[0][1] -= 1
        self.put()

    def move_one_down(self):
        self.erase()
        self.current_figure[0][0] += 1
        if self.intersection():
            self.current_figure[0][0] -= 1
        self.put()

    def kill_line(self):
        line = 0
        for i in range(len(self.board) - 3):
            if min(self.board[i]) > 0:
                self.board.pop(i)
                self.board.insert(0, [1] * self.shift + [0] * self.width + [1] * self.shift)
                line += 1
        if line == 1:
            self.points += 100
        if line == 2:
            self.points += 300
        if line == 3:
            self.points += 700
        if line == 4:
            self.points += 1500
        if line:
            K_line.play()
        global MYEVENTTYPE
        pygame.time.set_timer(MYEVENTTYPE, self.faster())

    def faster(self):
        global difficulty
        if self.points > 3500:
            return int(105 / difficulty)
        if self.points > 2800:
            return int(150 / difficulty)
        if self.points > 2400:
            return int(200 / difficulty)
        if self.points > 1800:
            return int(250 / difficulty)
        if self.points > 1300:
            return int(300 / difficulty)
        if self.points > 900:
            return int(350 / difficulty)
        if self.points > 500:
            return int(400 / difficulty)
        if self.points > 100:
            return int(450 / difficulty)
        return int(500 / difficulty)


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_icon(pygame.image.load("data/game_name_img.bmp"))
    pygame.mixer.music.load("fon.mp3")
    game_over = pygame.mixer.Sound("game-over.ogg")
    K_line = pygame.mixer.Sound("line.ogg")
    pygame.mixer.music.play(-1)
    size = 500, 440
    screen = pygame.display.set_mode(size)
    difficulty, name = start_screen(screen)
    print(difficulty, name)
    pygame.display.set_caption('Тетрис')
    lst = {
        "Легко": 1,
        "Средне": 1.2,
        "Сложно": 4
    }
    difficulty = lst[difficulty]
    speed = int(500 / difficulty)
    tetris = Tetris(12, 20)

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, speed)
    pressed = pygame.key.get_pressed()
    running = True
    on_pause = False
    m_on_pause = False
    while running:
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE:
                tetris.move_down()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not on_pause:
                        tetris.rotation()
                if event.key == pygame.K_LEFT:
                    if not on_pause:
                        tetris.move_left()
                if event.key == pygame.K_RIGHT:
                    if not on_pause:
                        tetris.move_right()
                if event.key == pygame.K_DOWN:
                    if not on_pause:
                        tetris.move_one_down()
                if event.key == pygame.K_SPACE:
                    if on_pause:
                        pygame.time.set_timer(MYEVENTTYPE, tetris.faster())
                        pygame.mixer.music.unpause()
                    else:
                        pygame.time.set_timer(MYEVENTTYPE, 0)
                        pygame.mixer.music.pause()
                    on_pause = not on_pause
                if event.key == pygame.K_1:
                    if m_on_pause:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    m_on_pause = not m_on_pause

        screen.fill((0, 0, 0))
        tetris.render(screen)
        pygame.display.flip()
    pygame.quit()
