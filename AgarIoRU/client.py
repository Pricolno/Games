import socket
from pprint import pprint

import pygame

SERVER_IP = 'localhost'
MAIN_PORT = 10000

WIDTH_WINDOW, HEIGHT_WINDOW = 1200, 800
colours = {'0': (255, 255, 0), '1': (255, 0, 0), '2': (0, 255, 0), '3': (0, 255, 255), '4': (128, 0, 128)}
MY_NAME = 'Naumtsev'
GRID_COLOUR = (150, 150, 150)


class User:
    def __init__(self, user_data):
        user_data = user_data.split()
        self.r = int(user_data[0])
        self.colour = user_data[1]

    def update(self, new_r):
        self.r = new_r

    def draw(self):
        if self.r != 0:
            pygame.draw.circle(screen, colours[self.colour],
                               (WIDTH_WINDOW // 2, HEIGHT_WINDOW // 2), self.r)

            write_name(WIDTH_WINDOW // 2, HEIGHT_WINDOW // 2, self.r, MY_NAME)


class Grid:
    def __init__(self, screen_):
        self.screen = screen_
        self.start_size = 200
        self.size = self.start_size

        self.x = -self.size
        self.y = -self.size

    def update(self, r_x, r_y, L):
        self.size = self.start_size // L
        self.x = -self.size + (-r_x) % self.size
        self.y = -self.size + (-r_y) % self.size

    def draw(self):
        for i in range(WIDTH_WINDOW // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [self.x + i * self.size, 0],  # координаты верхнего конца отрезка
                             [self.x + i * self.size, HEIGHT_WINDOW],  # координаты нижнего конца отрезка
                             1)

        for i in range(HEIGHT_WINDOW // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [0, self.y + i * self.size],
                             [WIDTH_WINDOW, self.y + i * self.size],
                             1)


# создание окна игры
pygame.init()
screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
pygame.display.set_caption('Agario.RU')

# подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect((SERVER_IP, MAIN_PORT))

# отправляем серверу свой ник и размеры окна
sock.send(('.' + MY_NAME + ' ' + str(WIDTH_WINDOW) + ' ' + str(HEIGHT_WINDOW) + '.').encode())

# получаем свой размер и цвет
data = sock.recv(64).decode()

# подтверждаем получение
sock.send('!'.encode())


def find_correct_data_str(mess):
    open_br = None
    for i in range(len(mess)):
        if mess[i] == '<':
            open_br = i
        if mess[i] == '>' and open_br is not None:
            close_br = i
            res = mess[open_br + 1:close_br]

            return res
    return ''


def write_name(x, y, r, name):
    font = pygame.font.Font(None, r)
    text = font.render(name, True, (0, 0, 0))
    rect = text.get_rect(center=(x, y))
    screen.blit(text, rect)


def draw_opponents(data):
    print("DATA:", end="")
    pprint(data)
    for opp_str in data:
        opp = opp_str.split(' ')

        x = WIDTH_WINDOW // 2 + int(opp[0])
        y = HEIGHT_WINDOW // 2 + int(opp[1])
        r = int(opp[2])
        c = colours[opp[3]]
        pygame.draw.circle(screen, c, (x, y), r)

        if len(opp) == 5:
            write_name(x, y, r, opp[4])


user = User(data)
grid = Grid(screen)
server_work = True

v_dir = (0, 0)
old_v_dir = (0, 0)
while server_work:
    # обработка событий

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_work = False

    # считаем положение мыши игрока
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        v_dir = (pos[0] - WIDTH_WINDOW // 2, pos[1] - HEIGHT_WINDOW // 2)

        if (v_dir[0]) ** 2 + (v_dir[1]) ** 2 <= user.r ** 2:
            v_dir = (0, 0)

    # отправляем вектор желаемого направления движения,
    # если он поменялся
    if v_dir != old_v_dir:
        old_v_dir = v_dir
        message = '<' + str(v_dir[0]) + ',' + str(v_dir[1]) + '>'
        sock.send(message.encode())

        print("Направление мышки: ", v_dir)

    # получение нового состояния игрового поля
    try:
        data = sock.recv(2 ** 20)
    except:
        running = False
        continue
    data = data.decode()
    # data = find_correct_data(data)
    # data = data.split(',')

    parametrs = find_correct_data_str(data).split(',')

    # обработка сообщения с сервера
    if parametrs != ['']:
        parametrs_for_user = list(map(int, parametrs[0].split(' ')))
        user.update(parametrs_for_user[0])
        grid.update(parametrs_for_user[1], parametrs_for_user[2], parametrs_for_user[3])

        # Рисуем новое состояние игрового поля
        screen.fill('gray25')
        grid.draw()
        draw_opponents(parametrs[1:])
        user.draw()

    pygame.display.update()
pygame.quit()
