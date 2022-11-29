import pygame
from random import randrange
class Globals:
    SIZE = 50
    RES = 800
    ffps = 50
    fps = 60
    fps_old = 60
    fps_water = (3 * fps) // 2
    fps_sand = (2 * fps) // 3
    count = 0
    max_time = 5000
    time = - max_time
    count_splitt = 10
    count_game = 0
    table_record = []
    score = 0
    flag = False
    flag_end = False
    flag_snowflake = False
    snowflake_xx = 1000

    Rock1 = ()
    Rock2 = ([3 * 50, 5 * 50], [9 * 50, 1 * 50], [11 * 50, 12 * 50])
    Rock3 = Rock2 + tuple([i * 50, 7 * 50] for i in range(2, 9)) + \
        tuple([i * 50, 5 * 50] for i in range(13, 16)) + \
        tuple([i * 50, 6 * 50] for i in range(13, 16))
    Rock4 = tuple([7 * 50, i * 50] for i in range(6)) + tuple([7 * 50, i * 50] for i in range(9, 16)) + Rock2
    Rock5 = tuple([i * 50, 6 * 50] for i in range(1, 9)) + tuple([12 * 50, i * 50] for i in range(4, 13)) \
        + tuple([i * 50, 10 * 50] for i in range(1, 9)) + ([2 * 50, 2 * 50], [4 * 50, 13 * 50])
    lavel = {1: Rock1, 2: Rock2, 3: Rock3, 4: Rock4, 5: Rock5}

    Sand1 = ()
    Sand2 = ([4 * 50, 6 * 50], [12 * 50, 4 * 50], [5 * 50, 12 * 50])
    Sand3 = tuple(([(i + 1) * 50, i * 50] for i in range(2, 7))) + \
        tuple(([(i + 2) * 50, i * 50] for i in range(2, 7)))
    Sand4 = ([4 * 50, 6 * 50], [12 * 50, 4 * 50], [5 * 50, 12 * 50])
    Sand5 = ([15 * 50, 0], [14 * 50, 0], [15 * 50, 1 * 50], [15 * 50, 15 * 50], [14 * 50, 15 * 50], [9 * 50, 6 * 50],
             [8 * 50, 5 * 50], [8 * 50, 7 * 50], [9 * 50, 10 * 50], [8 * 50, 9 * 50], [8 * 50, 11 * 50],
             [15 * 50, 14 * 50])
    lavel_sand = {1: Sand1, 2: Sand2, 3: Sand3, 4: Sand4, 5: Sand5}
    Water1 = ()
    Water2 = ([7 * 50, 1 * 50], [13 * 50, 7 * 50], [2 * 50, 7 * 50])
    Water3 = tuple([i * 50, 13 * 50] for i in range(7)) + tuple([i * 50, 14 * 50] for i in range(8)) \
        + tuple([i * 50, 15 * 50] for i in range(9))
    Water4 = ([5 * 50, 1 * 50], [13 * 50, 7 * 50], [2 * 50, 7 * 50])
    Water5 = tuple([13 * 50, i * 50] for i in range(4, 13)) + tuple([14 * 50, i * 50] for i in range(5, 12)) \
        + tuple([15 * 50, i * 50] for i in range(7, 10))
    lavel_water = {1: Water1, 2: Water2, 3: Water3, 4: Water4, 5: Water5}

    pygame.init()
    surface = pygame.display.set_mode([800, 800])
    surface_table = pygame.display.set_mode([800, 800])

    font_score = pygame.font.SysFont('New Times Roman', 45, bold=True)
    font_table = pygame.font.SysFont('New Times Roman', 70, bold=True)

    img = pygame.image.load('images.jpeg').convert()
    img = pygame.transform.scale(img, (800, 800))
    img_table = pygame.image.load('02-e3e62bae.png')
    image_rock = pygame.image.load('rock.png')
    image_rock = pygame.transform.scale(image_rock, (50, 50))
    image_sand = pygame.image.load('sand.png')
    image_sand = pygame.transform.scale(image_sand, (50, 50))
    image_water = pygame.image.load('water.png')
    image_water = pygame.transform.scale(image_water, (50, 50))
    apple_image = pygame.image.load('02-e3e62bae.png')
    apple_image = pygame.transform.scale(apple_image, (50, 50))

    snowflake_image = pygame.image.load('snejinka.png')
    snowflake_image = pygame.transform.scale(snowflake_image, (50, 50))

    x_apple = randrange(50, 800 - 50, 50)
    y_apple = randrange(50, 800 - 50, 50)

    x_snowflake = randrange(50, 800 - 50, 50)
    y_snowflake = randrange(50, 800 - 50, 50)

    difficult = 1
