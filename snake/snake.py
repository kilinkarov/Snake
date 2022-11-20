
import pygame
import pygame_menu
import numpy
from random import randrange
import copy
from time import sleep

RES = 800
SIZE = 50
fps = 60
fps_old = 60
fps_water = (3 * fps) // 2
fps_sand = (2 * fps) // 3
count = 0
time = -5000


class SNAKE:
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
        self.snake_now = copy.deepcopy(self.snake)

    count_split = 10
    dx_now = 0
    dy_now = 0
    flag_end = False

    def draw_rock(self):
        global surface
        for x, y in self.rock:
            surface.blit(self.image_rock, (x, y))
        for x, y in self.sand:
            surface.blit(self.image_sand, (x, y))
        for x, y in self.water:
            surface.blit(self.image_water, (x, y))

    def move_snake(self, size, dx, dy):
        global count
        if count == 0:
            self.dx_now = copy.deepcopy(dx)
            self.dy_now = copy.deepcopy(dy)
            self.snake_now = copy.deepcopy(self.snake)
        for i in range(len(self.snake) - 1):
            self.snake[i][0] += -numpy.sign(self.snake[i][0] - self.snake_now[i + 1][0]) * (size // self.count_split)
            self.snake[i][1] += -numpy.sign(self.snake[i][1] - self.snake_now[i + 1][1]) * (size // self.count_split)
        self.snake[-1][0] += self.dx_now * (SIZE // self.count_split)
        self.snake[-1][1] += self.dy_now * (SIZE // self.count_split)

    def scaling_snake(self, size):
        global flag, count
        if flag:
            if count == 0:
                self.snake.reverse()
                self.snake.append([self.snake[-1][0] - self.dx_now * size, self.snake[-1][1] - self.dy_now * size])
                self.snake.reverse()

    def draw_snake(self, size):
        global surface
        [pygame.draw.rect(surface, pygame.Color('green'), (i, j, size, size)) for i, j in self.snake]

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
        global fps, fps_water, fps_sand, fps_old
        count_water_spand = 0
        for x_s, y_s in self.snake:
            for x, y in self.water:
                if (abs(y_s - y) < size) and abs(x_s - x) < size:
                    fps = fps_water
                    count_water_spand += 1
        for x_s, y_s in self.snake:
            for x, y in self.sand:
                if (abs(y_s - y) < size) and abs(x_s - x) < size:
                    fps = fps_sand
                    count_water_spand += 1
        if count_water_spand == 0:
            fps = fps_old


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

    def crash(self, flagg):
        if flagg:
            self.x = 1000
            self.y = 1000

    def eating_apple(self, flagg, snake, size):
        if flagg:
            self.x = randrange(SIZE, RES - SIZE, SIZE)
            self.y = randrange(SIZE, RES - SIZE, SIZE)
            while True:
                counter = 0
                for x_s, y_s in snake:
                    if (self.x - x_s) ** 2 + (self.y - y_s) ** 2 <= size ** 2:
                        counter += 1
                for x_s, y_s in self.rock:
                    if (self.x - x_s) ** 2 + (self.y - y_s) ** 2 <= size ** 2:
                        counter += 1
                for x_s, y_s in self.sand:
                    if (self.x - x_s) ** 2 + (self.y - y_s) ** 2 <= size ** 2:
                        counter += 1
                for x_s, y_s in self.water:
                    if (self.x - x_s) ** 2 + (self.y - y_s) ** 2 <= size ** 2:
                        counter += 1
                if self.x == self.x_a and self.y == self.y_a:
                    counter += 1
                if counter == 0:
                    break
                self.x = randrange(SIZE, RES - SIZE, SIZE)
                self.y = randrange(SIZE, RES - SIZE, SIZE)

    def draw_apple(self):
        global surface
        surface.blit(self.image, (self.x, self.y))


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


count_game = 0
table_record = []
score = 0
flag = False
flag_end = False
flag_snowflake = False


Rock1 = ()
Rock2 = ([3 * SIZE, 5 * SIZE], [9 * SIZE, 1 * SIZE], [11 * SIZE, 12 * SIZE])
Rock3 = Rock2 + tuple([i * SIZE, 7 * SIZE] for i in range(2, 9)) + tuple([i * SIZE, 5 * SIZE] for i in range(13, 16))\
        + tuple([i * SIZE, 6 * SIZE] for i in range(13, 16))
Rock4 = tuple([7 * SIZE, i * SIZE] for i in range(6)) + tuple([7 * SIZE, i * SIZE] for i in range(9, 16)) + Rock2
Rock5 = tuple([i * SIZE, 6 * SIZE] for i in range(1, 9)) + tuple([12 * SIZE, i * SIZE] for i in range(4, 13))\
        + tuple([i * SIZE, 10 * SIZE] for i in range(1, 9)) + ([2 * SIZE, 2 * SIZE], [4 * SIZE, 13 * SIZE])
lavel = {1: Rock1, 2: Rock2, 3: Rock3, 4: Rock4, 5: Rock5}

Sand1 = ()
Sand2 = ([4 * SIZE, 6 * SIZE], [12 * SIZE, 4 * SIZE], [5 * SIZE, 12 * SIZE])
Sand3 = tuple(([(i + 1) * SIZE, i * SIZE] for i in range(2, 7))) + \
        tuple(([(i + 2) * SIZE, i * SIZE] for i in range(2, 7)))
Sand4 = ([4 * SIZE, 6 * SIZE], [12 * SIZE, 4 * SIZE], [5 * SIZE, 12 * SIZE])
Sand5 = ([15 * SIZE, 0], [14 * SIZE, 0], [15 * SIZE, 1 * SIZE], [15 * SIZE, 15 * SIZE], [15 * SIZE, 14 * SIZE],
         [14 * SIZE, 15 * SIZE]) + ([9 * SIZE, 6 * SIZE], [8 * SIZE, 5 * SIZE], [8 * SIZE, 7 * SIZE],
                                    [9 * SIZE, 10 * SIZE], [8 * SIZE, 9 * SIZE], [8 * SIZE, 11 * SIZE])
lavel_sand = {1: Sand1, 2: Sand2, 3: Sand3, 4: Sand4, 5: Sand5}
Water1 = ()
Water2 = ([7 * SIZE, 1 * SIZE], [13 * SIZE, 7 * SIZE], [2 * SIZE, 7 * SIZE])
Water3 = tuple([i * SIZE, 13 * SIZE] for i in range(7)) + tuple([i * SIZE, 14 * SIZE] for i in range(8))\
         + tuple([i * SIZE, 15 * SIZE] for i in range(9))
Water4 = ([5 * SIZE, 1 * SIZE], [13 * SIZE, 7 * SIZE], [2 * SIZE, 7 * SIZE])
Water5 = tuple([13 * SIZE, i * SIZE] for i in range(4, 13)) + tuple([14 * SIZE, i * SIZE] for i in range(5, 12))\
         + tuple([15 * SIZE, i * SIZE] for i in range(7, 10))
lavel_water = {1: Water1, 2: Water2, 3: Water3, 4: Water4, 5: Water5}

pygame.init()
surface = pygame.display.set_mode([RES, RES])
surface_table = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()

font_score = pygame.font.SysFont('New Times Roman', 45, bold=True)
font_table = pygame.font.SysFont('New Times Roman', 70, bold=True)

img = pygame.image.load('images.jpeg').convert()
img = pygame.transform.scale(img, (RES, RES))
img_table = pygame.image.load('02-e3e62bae.png')
image_rock = pygame.image.load('rock.png')
image_rock = pygame.transform.scale(image_rock, (SIZE, SIZE))
image_sand = pygame.image.load('sand.png')
image_sand = pygame.transform.scale(image_sand, (SIZE, SIZE))
image_water = pygame.image.load('water.png')
image_water = pygame.transform.scale(image_water, (SIZE, SIZE))
apple_image = pygame.image.load('02-e3e62bae.png')
apple_image = pygame.transform.scale(apple_image, (SIZE, SIZE))

snowflake_image = pygame.image.load('snejinka.png')
snowflake_image = pygame.transform.scale(snowflake_image, (50, 50))

x_apple = randrange(SIZE, RES - SIZE, SIZE)
y_apple = randrange(SIZE, RES - SIZE, SIZE)

x_snowflake = randrange(SIZE, RES - SIZE, SIZE)
y_snowflake = randrange(SIZE, RES - SIZE, SIZE)

difficult = 1


def set_difficulty(value, difficulty):
    global difficult, fps, fps_old, fps_water, fps_sand
    difficult = difficulty
    fps = 50 + difficult * 10
    fps_old = 50 + difficult * 10
    fps_water = fps * 1.5
    fps_sand = fps // 1.5
    pass


def make_string_table(names_input):
    name = names_input.get_value()
    return name


def table_records_append(names):
    global score
    table_record.append([names, score])
    table_record.sort(key=lambda x: -x[1])


def table_records():
    global surface_table, count_game
    surface_table.blit(img, (0, 0))
    for i in range(min(count_game, 5)):
        record = str(table_record[i][0]) + ':' + str(table_record[i][1])
        render_table = font_table.render(f' {record}', True, pygame.Color('black'))
        surface_table.blit(render_table, (50, 100 + 100 * i))
    sleep(5)


def start_the_game():
    global score, count, fps, SIZE, RES, flag, surface,\
        flag_end, flag_snowflake, time, count_game, fps_old, fps_water, fps_sand
    apple = APPLE(x_apple, y_apple, apple_image, lavel[difficult], lavel_sand[difficult],
                  lavel_water[difficult], 1000, 1000)
    apple.eating_apple(True, [[750, 750]], SIZE)
    snowflake = APPLE(1000, 1000, snowflake_image, lavel[difficult],
                      lavel_sand[difficult], lavel_water[difficult], apple.x, apple.y)
    snake = SNAKE(750, 750, lavel[difficult], lavel_sand[difficult],
                  lavel_water[difficult], image_rock, image_sand, image_water)
    button = BUTTON()

    while True:
        surface.blit(img, (0, 0))
        render_score = font_score.render(f'SCORE: {score}', True, pygame.Color('white'))
        surface.blit(render_score, (5, 5))
        apple.draw_apple()
        snake.draw_rock()
        snake.draw_snake(SIZE)
        snowflake.draw_apple()
        button.orientation(snake.dx_now, snake.dy_now)
        if time == -1:
            snowflake = APPLE(randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE),
                              snowflake_image, lavel[difficult], lavel_sand[difficult],
                              lavel_water[difficult], apple.x, apple.y)
        if (snake.snake[-1][0] + SIZE - 1 >= apple.x >= snake.snake[-1][0] - SIZE + 1) and (
                snake.snake[-1][1] + SIZE - 1 >= apple.y >= snake.snake[-1][1] - SIZE + 1):
            if count == 0:
                score += 1
                fps += 5
                fps_old += 5
                fps_water = 3 * fps_old // 2
                fps_sand = 2 * fps_old // 3
                flag = True

        if (snake.snake[-1][0] + SIZE - 1 >= snowflake.x >= snake.snake[-1][0] - SIZE + 1) and (
                snake.snake[-1][1] + SIZE - 1 >= snowflake.y >= snake.snake[-1][1] - SIZE + 1):
            if count == 0:
                if fps > 30:
                    fps -= max(fps // 3, 30)
                    fps_old = max(fps_old // 3, 30)
                fps_water = (3 * fps_old) // 2
                fps_sand = (2 * fps_old) // 3
                score = max(0, score - 3)
                flag_snowflake = True
                snowflake.crash(flag_snowflake)
                apple.chanche(1000, 1000)
                time = 0
        snake.scaling_snake(SIZE)
        snake.move_snake(SIZE, button.dx, button.dy)
        if count == 0:
            apple.eating_apple(flag, snake.snake, SIZE)
            snowflake.chanche(apple.x, apple.y)
            flag = False
        count += 1
        time += 1
        snake.check_spand_or_water(SIZE)
        if count == 9:
            count = 0
        if time >= 5000:
            snowflake.eating_apple(flag_snowflake, snake.snake, SIZE)
            apple.chanche(snowflake.x, snowflake.y)
            flag_snowflake = False
            time = 0
        if snake.check_game_over(SIZE, RES):
            break
        pygame.display.flip()
        clock.tick(fps)
        snake.close_game()

    sleep(1)
    count_game += 1
    make_string_table(name_input)
    table_records_append(make_string_table(name_input))
    fps = fps_old
    fps = 50 + difficult * 10
    fps_old = 50 + difficult * 10
    fps_water = fps_old * 1.5
    fps_sand = fps_old // 1.5
    score = 0
    time = -5000


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

menu.mainloop(surface)
