import pygame

WIDTH, HEIGHT = 500, 500

FPS = 40
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 60
SPEED = 5

X = WIDTH * 2 / 3
Y = HEIGHT - SPACESHIP_HEIGHT - 20

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

RUNNING = True

LEFT_BOARD, RIGHT_BOARD = 10, 10
UP_BOARD, DOWN_BOARD = 10, 15

IS_JUMP = False
JUMP_COUNT = 10

walkRight, walkLeft = None, None
bg, playerStand = None, None

LEFT_DIR, RIGHT_DIR = False, False
ANIM_COUNT = 0

CLOCK = None

DIR_LAST_MOVE = "right"
BULLET_FACING = 1

BULLETS = []
OCCUR_UNDER_FOOT = 7


class Platform:
    def __init__(self, left, top, width, height, label="Первый борт"):
        self.label = label
        self.rect = pygame.Rect(left, top, width, height)

    def draw(self):
        LIGHT_OLIVE = (148, 93, 11)
        pygame.draw.rect(WIN, LIGHT_OLIVE, self.rect)

    def info(self):
        print("PLATFORM, " + self.label + " : " + str(self.rect.left) + " " + str(self.rect.right) + " " + str(self.rect.top) + " " + str(self.rect.bottom))

    def is_collide(self, x, y):
        return self.rect.collidepoint(x, y)

    def is_collide_line(self, x, y):
        return self.rect.clipline(x, y, X, Y)

# rectangle is like line
class FabricPlatforms:
    def __init__(self):
        self.PLATFORMS = [
            Platform(round(WIDTH * 2 / 3), HEIGHT - 2 * SPACESHIP_HEIGHT + 20,
                     round(SPACESHIP_WIDTH * 4 / 3), 5)
        ]

    def info_fabric(self):
        for platform in self.PLATFORMS:
            platform.info()

    def is_exist_collide(self, x, y):
        for rect_now in self.PLATFORMS:
            if rect_now.is_collide(x, y):
                print("COLLIDE: TRUE ({0}, {1})".format(X, Y))
                return True, rect_now
        print("COLLIDE: FALSE ({0}, {1})".format(X, Y))
        return False, None

    def is_exist_collide_line(self, x, y):
        for rect_now in self.PLATFORMS:
            if rect_now.is_collide_line(x, y):
                print("COLLIDE_LINE: TRUE ({0}, {1})".format(X, Y))
                return True, rect_now
        print("COLLIDE_LINE: FALSE ({0}, {1})".format(X, Y))
        return False, None


FABRIC_PLATFORM = FabricPlatforms()


class Spread:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)


def load_start():
    global walkRight, walkLeft, bg, playerStand, CLOCK, FABRIC_PLATFORM

    FABRIC_PLATFORM.info_fabric()

    walkRight = [pygame.image.load('photos/yellow_hair/pygame_right_1.png'),
                 pygame.image.load('photos/yellow_hair/pygame_right_2.png'),
                 pygame.image.load('photos/yellow_hair/pygame_right_3.png'),
                 pygame.image.load('photos/yellow_hair/pygame_right_4.png'),
                 pygame.image.load('photos/yellow_hair/pygame_right_5.png'),
                 pygame.image.load('photos/yellow_hair/pygame_right_6.png')]

    walkLeft = [pygame.image.load('photos/yellow_hair/pygame_left_1.png'),
                pygame.image.load('photos/yellow_hair/pygame_left_2.png'),
                pygame.image.load('photos/yellow_hair/pygame_left_3.png'),
                pygame.image.load('photos/yellow_hair/pygame_left_4.png'),
                pygame.image.load('photos/yellow_hair/pygame_left_5.png'),
                pygame.image.load('photos/yellow_hair/pygame_left_6.png')]

    bg = pygame.image.load('photos/yellow_hair/pygame_bg.jpg')
    playerStand = pygame.image.load('photos/yellow_hair/pygame_idle.png')

    CLOCK = pygame.time.Clock()

    # FABRIC_PLATFORM = FabricPlatforms()


def draw_window():
    global ANIM_COUNT, FABRIC_PLATFORM
    WIN.blit(bg, (0, 0))

    if ANIM_COUNT + 1 >= 30:
        ANIM_COUNT = 0

    if LEFT_DIR:
        WIN.blit(walkLeft[ANIM_COUNT // 5], (X, Y))
        ANIM_COUNT += 1
    elif RIGHT_DIR:
        WIN.blit(walkRight[ANIM_COUNT // 5], (X, Y))
        ANIM_COUNT += 1
    else:
        WIN.blit(playerStand, (X, Y))

    for bullet in BULLETS:
        bullet.draw()
        # print("DRAW BULLET")

    for platform in FABRIC_PLATFORM.PLATFORMS:
        # platform.info()
        # print(platform)

        platform.draw()
        # pygame.draw.rect(WIN, BLUE, (X, Y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    pygame.display.update()


# (bool, rect)
def is_empty_foot(to_x, to_y):
    global FABRIC_PLATFORM
    print("DIFFF: " + str(to_y - HEIGHT + DOWN_BOARD))
    if to_y > HEIGHT - DOWN_BOARD :
        print("HELLOOOOOOOO")
        return True, None
    print("GOOOODBBBBYYYYE")
    return FABRIC_PLATFORM.is_exist_collide_line(to_x, to_y)


def handle_movement(keys_pressed):
    global X, Y, IS_JUMP, JUMP_COUNT, LEFT_DIR, \
        RIGHT_DIR, BULLET_FACING, DIR_LAST_MOVE, BLUE, BULLETS, \
        FABRIC_PLATFORM, OCCUR_UNDER_FOOT

    for bullet in BULLETS:
        if WIDTH > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            BULLETS.pop(BULLETS.index(bullet))

    MAX_COUNT_BULLETS = 5
    RADIUS_BULLETS = 5
    COLOR_BULLETS = BLUE

    if keys_pressed[pygame.K_f]:
        # print("Pressed F")
        if DIR_LAST_MOVE == "right":
            BULLET_FACING = 1
        else:
            BULLET_FACING = -1

        if len(BULLETS) < MAX_COUNT_BULLETS:
            BULLETS.append(Spread(
                round(X + (SPACESHIP_WIDTH // 2)),
                round(Y + (SPACESHIP_HEIGHT // 2)),
                RADIUS_BULLETS,
                COLOR_BULLETS,
                BULLET_FACING)
            )

    if keys_pressed[pygame.K_LEFT] and X - SPEED > 0 + LEFT_BOARD:
        X -= SPEED
        LEFT_DIR = True
        RIGHT_DIR = False
        DIR_LAST_MOVE = "left"
    elif keys_pressed[pygame.K_RIGHT] and X + SPACESHIP_WIDTH + SPEED < WIDTH - RIGHT_BOARD:
        X += SPEED
        RIGHT_DIR = True
        LEFT_DIR = False
        DIR_LAST_MOVE = "right"
    else:
        RIGHT_DIR = False
        LEFT_DIR = False

    if not IS_JUMP:
        # if keys[pygame.K_UP] and Y - SPEED > 0 + UP_BOARD:
        #   Y -= SPEED
        # if keys[pygame.K_DOWN] and Y + SPEED + SPACESHIP_HEIGHT < HEIGHT - DOWN_BOARD:
        #    Y += SPEED
        under_foot, rect = is_empty_foot(X + (SPACESHIP_WIDTH // 2), Y + SPACESHIP_HEIGHT + OCCUR_UNDER_FOOT)
        if not under_foot:
            print("Under foot is empty!!!")
            IS_JUMP = True
            JUMP_COUNT = 0
        elif keys_pressed[pygame.K_SPACE]:
            IS_JUMP = True
    else:

        def jump_update():
            global JUMP_COUNT, IS_JUMP
            IS_JUMP = False
            JUMP_COUNT = 10
            return

        JUMP_COEFF = 3

        if JUMP_COUNT >= -10:

            CANCEL_INCR = False

            if JUMP_COUNT < 0:

                Y_NEW = Y + (JUMP_COUNT ** 2) / JUMP_COEFF

                flag_left, rect_left = is_empty_foot(X, Y_NEW + SPACESHIP_HEIGHT + OCCUR_UNDER_FOOT)
                flag_right, rect_right = is_empty_foot(X + SPACESHIP_WIDTH, Y_NEW + SPACESHIP_HEIGHT + OCCUR_UNDER_FOOT)
                if not flag_left and not flag_right:
                    Y = Y_NEW
                    print("Y_NEW = {0}".format(Y))
                    #print("NOT Collide!")
                    #print(Y)
                else:
                    foot_rect = None
                    if flag_left:
                        foot_rect = rect_left
                    if flag_right:
                        foot_rect = rect_right

                    #foot_rect.info()

                    print("Collide!")
                    jump_update()
                    CANCEL_INCR = True

            else:
                Y -= (JUMP_COUNT ** 2) / JUMP_COEFF
            if not CANCEL_INCR:
                JUMP_COUNT -= 1
        else:
            jump_update()


def handle_is_quit():
    global RUNNING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            RUNNING = False


if __name__ == '__main__':
    print("Игра запускается")
    load_start()

    while RUNNING:
        CLOCK.tick(FPS)
        # pygame.time.delay(20)
        handle_is_quit()

        keys_pressed = pygame.key.get_pressed()
        # print(BULLETS)
        handle_movement(keys_pressed)
        draw_window()

    print("Игра завершена")
