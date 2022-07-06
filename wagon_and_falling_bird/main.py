import pygame
from ball import Ball
from random import randint

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1400)

BLACK = (0, 0, 0)

WIDTH, HEIGHT = 1000, 570
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BACKGROUND = pygame.image.load('images/back1.jpg').convert()

CLOCK = pygame.time.Clock()
FPS = 60



SCORE_IMAGE = pygame.image.load('images/score_fon.png').convert_alpha()
FONT = pygame.font.SysFont('arial', 30)

USER_CART = pygame.image.load('images/telega.png').convert_alpha()
CART_RECT = USER_CART.get_rect(centerx=WIDTH//2, bottom=HEIGHT-5)
CART_SPEED = 10

FALLING_BALLS = pygame.sprite.Group()

BALLS_DATA = ({'path': 'ball_bear.png', 'score': 100},
              {'path': 'ball_fox.png', 'score': 150},
              {'path': 'ball_panda.png', 'score': 200})

BALLS_SURF = [pygame.image.load('images/'+data['path']).convert_alpha() for data in BALLS_DATA]


def createBall(group):
    indx = randint(0, len(BALLS_SURF) - 1)
    x = randint(20, WIDTH - 20)
    speed_now = randint(2, 5)

    return Ball(x, speed_now, BALLS_SURF[indx], BALLS_DATA[indx]['score'], group)

game_score = 0

RUNNING = True


def collideBalls():
    global game_score
    for ball in FALLING_BALLS:
        if CART_RECT.collidepoint(ball.rect.center):
            #  s_catch.play()
            game_score += ball.score
            ball.kill()


def handle_quit(event):
    global RUNNING
    if event.type == pygame.QUIT:
        RUNNING = False


    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        RUNNING = False



def draw_window():
    WIN.blit(BACKGROUND, (0, 0))
    # score
    WIN.blit(SCORE_IMAGE, (0, 0))
    sc_text = FONT.render(str(game_score), True, (94, 138, 14))
    WIN.blit(sc_text, (20, 10))

    #print(balls)
    FALLING_BALLS.draw(WIN)
    WIN.blit(USER_CART, CART_RECT)

    pygame.display.update()



def handle_event():
    for event in pygame.event.get():
        handle_quit(event)
        if event.type == pygame.USEREVENT:
            createBall(FALLING_BALLS)



    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        CART_RECT.x -= CART_SPEED
        if CART_RECT.x < 0:
            CART_RECT.x = 0
    elif keys[pygame.K_RIGHT]:
        CART_RECT.x += CART_SPEED
        if CART_RECT.x > WIDTH - CART_RECT.width:
            CART_RECT.x = WIDTH - CART_RECT.width
    collideBalls()

    FALLING_BALLS.update(HEIGHT)



if __name__ == '__main__':
    print("Игра загружается")

    while RUNNING:
        CLOCK.tick(FPS)


        handle_event()

        draw_window()

    print("Игра завершена")
