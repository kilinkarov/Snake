from copy import deepcopy
from globals import Globals
from numpy import sign
import pygame
import pygame_menu
from random import randrange
from time import sleep

globals = Globals()
pygame.init()
clock = pygame.time.Clock()


class SNAKE:
    count_split = 10
    dx_now = 0
    dy_now = 0
    flag_end = False

    def __init__(self, x, y, rock, sand, water, img_rock, img_sand, img_water):
        self.x = x
        self.y = y
        self.rock = rock
        self.sand = sand
        self.water = water
        self.image_rock = img_rock
        self.image_sand = img_sand
        self.image_water = img_water
        self.snake = [[x, y]]
        self.snake_now = deepcopy(self.snake)

    def draw_rock(self):
        for x, y in self.rock:
            globals.surface.blit(self.image_rock, (x, y))
        for x, y in self.sand:
            globals.surface.blit(self.image_sand, (x, y))
        for x, y in self.water:
            globals.surface.blit(self.image_water, (x, y))

    def move_snake(self, size, dx, dy):
        if globals.count == 0:
            self.dx_now = deepcopy(dx)
            self.dy_now = deepcopy(dy)
            self.snake_now = deepcopy(self.snake)
        for i in range(len(self.snake) - 1):
            self.snake[i][0] += -sign(self.snake[i][0] - self.snake_now[i + 1][0]) * (size // self.count_split)
            self.snake[i][1] += -sign(self.snake[i][1] - self.snake_now[i + 1][1]) * (size // self.count_split)
        self.snake[-1][0] += self.dx_now * (globals.SIZE // self.count_split)
        self.snake[-1][1] += self.dy_now * (globals.SIZE // self.count_split)

    def scaling_snake(self, size):
        if globals.flag:
            if globals.count == 0:
                self.snake.reverse()
                self.snake.append([self.snake[-1][0] - self.dx_now * size, self.snake[-1][1] - self.dy_now * size])
                self.snake.reverse()

    def draw_snake(self, size):
        [pygame.draw.rect(globals.surface, pygame.Color('pink'), (i, j, size, size)) for i, j in self.snake]

    def close_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def check_game_over(self, size, res):
        for i in range(len(self.snake) - 1):
            if (abs(self.snake[-1][0] - self.snake[i][0]) < size // 2
                    and abs(self.snake[-1][1] - self.snake[i][1]) < (size // self.count_split)):
                self.flag_end = True
            if (abs(self.snake[-1][1] - self.snake[i][1]) < (size // 2)
                    and abs(self.snake[-1][0] - self.snake[i][0]) < (size // self.count_split)):
                self.flag_end = True
        for x, y in self.rock:
            if (x == self.snake[-1][0]) and (abs(self.snake[-1][1] - y) < size) or \
                    (y == self.snake[-1][1]) and (abs(self.snake[-1][0] - x) < size):
                self.flag_end = True
        if self.snake[-1][0] < 0 or self.snake[-1][0] > res - size or \
                self.snake[-1][1] < 0 or self.snake[-1][1] > res - size:
            self.flag_end = True
        if self.flag_end:
            return 1
        return 0

    def check_spand_or_water(self, size):
        count_water_spand = 0
        for x_s, y_s in self.snake:
            for x, y in self.water:
                if (abs(y_s - y) < size) and abs(x_s - x) < size:
                    globals.fps = globals.fps_water
                    count_water_spand += 1
        for x_s, y_s in self.snake:
            for x, y in self.sand:
                if (abs(y_s - y) < size) and abs(x_s - x) < size:
                    globals.fps = globals.fps_sand
                    count_water_spand += 1
        if count_water_spand == 0:
            globals.fps = globals.fps_old


class APPLE:
    def __init__(self, x, y, image, rock, sand, water, x_a, y_a):
        self.x = x
        self.y = y
        self.image = image
        self.rock = rock
        self.sand = sand
        self.water = water
        self.x_a = x_a
        self.y_a = y_a

    def chanche(self, x, y):
        self.x_a = x
        self.y_a = y

    def chanche_x(self, x, y):
        self.x = x
        self.y = y

    def crash(self, flagg):
        if flagg:
            self.x = globals.snowflake_xx
            self.y = globals.snowflake_xx

    def check(self, array, size):
        for x_s, y_s in array:
            if (self.x - x_s) ** 2 + (self.y - y_s) ** 2 <= size ** 2:
                return 1
        return 0

    def eating_apple(self, flagg, snake, size):
        if flagg:
            self.x = randrange(globals.SIZE, globals.RES - globals.SIZE, globals.SIZE)
            self.y = randrange(globals.SIZE, globals.RES - globals.SIZE, globals.SIZE)
            while True:
                counter = 0
                counter += self.check(snake, size)
                counter += self.check(self.rock, size)
                counter += self.check(self.water, size)
                counter += self.check(self.sand, size)
                if self.x == self.x_a and self.y == self.y_a:
                    counter += 1
                if counter == 0:
                    break
                self.x = randrange(globals.SIZE, globals.RES - globals.SIZE, globals.SIZE)
                self.y = randrange(globals.SIZE, globals.RES - globals.SIZE, globals.SIZE)

    def draw_apple(self):
        globals.surface.blit(self.image, (self.x, self.y))


class BUTTON:
    buttons = {'W': 1, 'S': 1, 'A': 1, 'D': 1, }
    dx = 0
    dy = 0

    def orientation(self, dx_now, dy_now):
        if self.dx != dx_now or self.dy != dy_now:
            return
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            if self.buttons['W']:
                self.dx, self.dy = 0, -1
                self.buttons = {'W': 1, 'S': 0, 'A': 1, 'D': 1, }
        elif key[pygame.K_s]:
            if self.buttons['S']:
                self.dx, self.dy = 0, 1
                self.buttons = {'W': 0, 'S': 1, 'A': 1, 'D': 1, }
        elif key[pygame.K_a]:
            if self.buttons['A']:
                self.dx, self.dy = -1, 0
                self.buttons = {'W': 1, 'S': 1, 'A': 1, 'D': 0, }
        elif key[pygame.K_d]:
            if self.buttons['D']:
                self.dx, self.dy = 1, 0
                self.buttons = {'W': 1, 'S': 1, 'A': 0, 'D': 1, }


def set_difficulty(value, difficulty):
    globals.difficult = difficulty
    globals.fps = globals.ffps + globals.difficult * globals.count_splitt
    globals.fps_old = globals.ffps + globals.difficult * globals.count_splitt
    globals.fps_water = globals.fps * 1.5
    globals.fps_sand = globals.fps // 1.5
    pass


def make_string_table(names_input):
    name = names_input.get_value()
    return name


def table_records_append(names):
    globals.table_record.append([names, globals.score])
    globals.table_record.sort(key=lambda x: -x[1])


def table_records():
    globals.surface_table.blit(globals.img, (0, 0))
    for i in range(min(globals.count_game, 5)):
        record = str(globals.table_record[i][0]) + ':' + str(globals.table_record[i][1])
        render_table = globals.font_table.render(f' {record}', True, pygame.Color('black'))
        globals.surface_table.blit(render_table, (globals.SIZE, 2 * globals.SIZE + 2 * globals.SIZE * i))
    sleep(5)


def draw_all(apple, snake, snowflake, button):
    globals.surface.blit(globals.img, (0, 0))
    render_score = globals.font_score.render(f'SCORE: {globals.score}', True, pygame.Color('white'))
    globals.surface.blit(render_score, (5, 5))
    apple.draw_apple()
    snake.draw_rock()
    snake.draw_snake(globals.SIZE)
    snowflake.draw_apple()
    button.orientation(snake.dx_now, snake.dy_now)


def put_fps_apple(snake, apple):
    if (snake.snake[-1][0] + globals.SIZE - 1 >= apple.x >= snake.snake[-1][0] - globals.SIZE + 1) and (
            snake.snake[-1][1] + globals.SIZE - 1 >= apple.y >= snake.snake[-1][1] - globals.SIZE + 1):
        if globals.count == 0:
            globals.score += 1
            globals.fps += globals.count_splitt // 2
            globals.fps_old += globals.count_splitt // 2
            globals.fps_water = 3 * globals.fps_old // 2
            globals.fps_sand = 2 * globals.fps_old // 3
            globals.flag = True


def put_fps_snowflake(snake, snowflake, apple):
    if (snake.snake[-1][0] + globals.SIZE - 1 >= snowflake.x >= snake.snake[-1][0] - globals.SIZE + 1) and (
            snake.snake[-1][1] + globals.SIZE - 1 >= snowflake.y >= snake.snake[-1][1] - globals.SIZE + 1):
        if globals.count == 0:
            if globals.fps > 30:
                globals.fps -= globals.fps // 3
                globals.fps_old -= globals.fps_old // 3
            globals.fps_water = (3 * globals.fps_old) // 2
            globals.fps_sand = (2 * globals.fps_old) // 3
            globals.score = max(0, globals.score - 3)
            globals.flag_snowflake = True
            snowflake.crash(globals.flag_snowflake)
            apple.chanche(globals.snowflake_xx, globals.snowflake_xx)
            globals.time = 0


def iteration(snake, apple, snowflake):
    if globals.count == 0:
        apple.eating_apple(globals.flag, snake.snake, globals.SIZE)
        snowflake.chanche(apple.x, apple.y)
        globals.flag = False
    globals.count += 1
    globals.time += 1
    snake.check_spand_or_water(globals.SIZE)
    if globals.count == (globals.count_splitt - 1):
        globals.count = 0
    if globals.time >= globals.max_time:
        snowflake.eating_apple(globals.flag_snowflake, snake.snake, globals.SIZE)
        apple.chanche(snowflake.x, snowflake.y)
        globals.flag_snowflake = False
        globals.time = 0


def game_over():
    sleep(1)
    globals.count_game += 1
    make_string_table(name_input)
    table_records_append(make_string_table(name_input))
    globals.fps = globals.fps_old
    globals.fps = globals.ffps + globals.difficult * globals.count_splitt
    globals.fps_old = globals.ffps + globals.difficult * globals.count_splitt
    globals.fps_water = globals.fps_old * 1.5
    globals.fps_sand = globals.fps_old // 1.5
    globals.score = 0
    globals.time = -globals.max_time


def body_game(snake, apple, snowflake, button):
    draw_all(apple, snake, snowflake, button)
    if globals.time == -1:
        snowflake.eating_apple(True, snake.snake, globals.SIZE)
        apple.chanche(snowflake.x, snowflake.y)
    put_fps_apple(snake, apple)
    put_fps_snowflake(snake, snowflake, apple)
    snake.scaling_snake(globals.SIZE)
    snake.move_snake(globals.SIZE, button.dx, button.dy)
    iteration(snake, apple, snowflake)


def start_the_game():
    apple = APPLE(globals.x_apple, globals.y_apple, globals.apple_image, globals.lavel[globals.difficult],
                  globals.lavel_sand[globals.difficult],
                  globals.lavel_water[globals.difficult], globals.snowflake_xx, globals.snowflake_xx)
    apple.eating_apple(True, [[globals.RES - globals.SIZE, globals.RES - globals.SIZE]], globals.SIZE)
    snowflake = APPLE(globals.snowflake_xx, globals.snowflake_xx, globals.snowflake_image,
                      globals.lavel[globals.difficult],
                      globals.lavel_sand[globals.difficult], globals.lavel_water[globals.difficult], apple.x, apple.y)
    snake = SNAKE(globals.RES - globals.SIZE, globals.RES - globals.SIZE, globals.lavel[globals.difficult],
                  globals.lavel_sand[globals.difficult],
                  globals.lavel_water[globals.difficult], globals.image_rock, globals.image_sand, globals.image_water)
    button = BUTTON()
    while True:
        body_game(snake, apple, snowflake, button)
        if snake.check_game_over(globals.SIZE, globals.RES):
            break
        pygame.display.flip()
        clock.tick(globals.fps)
        snake.close_game()
    game_over()


font = pygame_menu.font.FONT_DIGITAL
mytheme = pygame_menu.Theme(
                background_color=(0, 0, 0, 0),
                widget_font=font,
                title_background_color=(0, 0, 0),
                title_font_shadow=True,
                widget_padding=3,
)

menu = pygame_menu.Menu('', 600, 600, theme=mytheme)
name_input = menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Lavel :', [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Table Records', table_records)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(globals.surface)
