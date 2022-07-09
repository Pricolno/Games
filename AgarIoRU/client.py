import socket
from pprint import pprint
from menu import *

import pygame

SETTINGS = {'WIDTH_WINDOW': 1500,
            'HEIGHT_WINDOW': 900,
            'MENU_PASSED': False,
            'OPEN_MAIN_MENU': False,
            'OPTIONS_PASSED': False,
            'OPEN_OPTIONS': False,
            'SCREEN': None,
            'SERVER_WORK': True,
            'USER': None

            }

SERVER_IP = 'localhost'
# SERVER_IP = '45.10.245.3'

MAIN_PORT = 10000

colours = {'0': (255, 255, 0), '1': (255, 0, 0), '2': (0, 255, 0), '3': (0, 255, 255), '4': (128, 0, 128)}

GRID_COLOUR = (150, 150, 150)
START_MY_NAME = 'NAUMTSEV'

# создание окна игры
pygame.init()
SETTINGS['SCREEN'] = pygame.display.set_mode((SETTINGS['WIDTH_WINDOW'], SETTINGS['HEIGHT_WINDOW']))
pygame.display.set_caption('Agario.RU')


class User:
    def __init__(self, my_name_, sock_, user_data):
        user_data = user_data.split()
        self.r = int(user_data[0])
        self.colour = user_data[1]
        self.time_after_death = 0
        self.sock = sock_
        self.name = my_name_

    def update(self, new_r):
        self.r = new_r
        if self.r == 0:
            self.time_after_death = min(self.time_after_death + 1, 1000)

    def need_open_menu(self):
        return self.time_after_death >= 200

    def reborn(self):
        self.send_server_ready()
        self.time_after_death = 0

    def is_alive(self):
        return not self.r == 0

    # сервер получил все данные и я готов начать играть
    def send_server_ready(self):
        # переродиться а данные о нас у него уже есть
        self.sock.send('#'.encode())

    def draw(self):
        if self.r != 0:
            pygame.draw.circle(SETTINGS['SCREEN'], colours[self.colour],
                               (SETTINGS['WIDTH_WINDOW'] // 2, SETTINGS['HEIGHT_WINDOW'] // 2), self.r)

            write_name(SETTINGS['WIDTH_WINDOW'] // 2, SETTINGS['HEIGHT_WINDOW'] // 2, self.r, self.name)



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
        for i in range(SETTINGS['WIDTH_WINDOW'] // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [self.x + i * self.size, 0],  # координаты верхнего конца отрезка
                             [self.x + i * self.size, SETTINGS['HEIGHT_WINDOW']],  # координаты нижнего конца отрезка
                             1)

        for i in range(SETTINGS['HEIGHT_WINDOW'] // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [0, self.y + i * self.size],
                             [SETTINGS['WIDTH_WINDOW'], self.y + i * self.size],
                             1)





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

# ****?name?****
# return (property, data_without_property)
def find_property(data):
    open_br = None
    for i in range(len(data)):
        if data[i] == '?' and open_br is not None:
            close_br = i
            #print("FIND_PROPERTY: data={0}, open_br={1}, close_br={2}".format(data, open_br, close_br))
            prop = data[open_br + 1:close_br]
            other = data[:open_br] + data[close_br + 1:]
            return prop, other

        if data[i] == '?':
            open_br = i
    return '', data


def write_name(x, y, r, name):
    font = pygame.font.Font(None, r)
    text = font.render(name, True, (0, 0, 0))
    rect = text.get_rect(center=(x, y))
    SETTINGS['SCREEN'].blit(text, rect)


def draw_opponents(data):
    # print("DATA:", end="")
    # pprint(data)
    for opp_str in data:
        opp = opp_str.split(' ')

        x = SETTINGS['WIDTH_WINDOW'] // 2 + int(opp[0])
        y = SETTINGS['HEIGHT_WINDOW'] // 2 + int(opp[1])
        r = int(opp[2])
        c = colours[opp[3]]
        pygame.draw.circle(SETTINGS['SCREEN'], c, (x, y), r)

        if len(opp) == 5:
            write_name(x, y, r, opp[4])


# подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect((SERVER_IP, MAIN_PORT))


# отправляем серверу свой ник и размеры окна
sock.send(('.' + START_MY_NAME + ' ' + str(SETTINGS['WIDTH_WINDOW']) + ' ' + str(SETTINGS['HEIGHT_WINDOW']) + '.').encode())

# получаем свой размер и цвет
data = sock.recv(64).decode()

# подтверждаем получение
sock.send('!'.encode())

SETTINGS['USER'] = User(START_MY_NAME, sock, data)



grid = Grid(SETTINGS['SCREEN'])

v_dir = (0, 0)
old_v_dir = (0, 0)

print("Игра начинается")
while SETTINGS['SERVER_WORK']:


    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SETTINGS['SERVER_WORK'] = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            SETTINGS['MENU_PASSED'] = True
            SETTINGS['OPEN_MAIN_MENU'] = True
            # двойное нажатие проблема !

    if SETTINGS['USER'].need_open_menu():
        if not SETTINGS['MENU_PASSED']:
            SETTINGS['MENU_PASSED'] = True
            SETTINGS['OPEN_MAIN_MENU'] = True



    if not SETTINGS['MENU_PASSED']:
        # считаем положение мыши игрока
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            v_dir = (pos[0] - SETTINGS['WIDTH_WINDOW'] // 2, pos[1] - SETTINGS['HEIGHT_WINDOW'] // 2)

            if (v_dir[0]) ** 2 + (v_dir[1]) ** 2 <= SETTINGS['USER'].r ** 2:
                v_dir = (0, 0)

        # отправляем вектор желаемого направления движения,
        # если он поменялся
        if v_dir != old_v_dir:
            old_v_dir = v_dir
            message = '<' + str(v_dir[0]) + ',' + str(v_dir[1]) + '>'
            sock.send(message.encode())

            # print("Направление мышки: ", v_dir)

    # получение нового состояния игрового поля
    try:
        data = sock.recv(2 ** 20)
    except:
        SETTINGS['SERVER_WORK'] = False
        continue
    data = data.decode()
    propp, move_data = find_property(data)
    if '?' in data:
        print(data + " | " + propp + " | " + move_data)
    # проверка на обновление характеристик (не позициионки)
    if propp != '':
        print("Пришло новое имя: " + propp)
        SETTINGS['USER'].name = propp


    parametrs = find_correct_data_str(move_data).split(',')

    # обработка сообщения с сервера (движение)
    if parametrs != ['']:
        parametrs_for_user = list(map(int, parametrs[0].split(' ')))
        #print("PARAMETR_FOR_USER: " + str(parametrs_for_user))

        SETTINGS['USER'].update(parametrs_for_user[0])

        grid.update(parametrs_for_user[1], parametrs_for_user[2], parametrs_for_user[3])

        # Рисуем новое состояние игрового поля
        SETTINGS['SCREEN'].fill('gray25')
        grid.draw()
        draw_opponents(parametrs[1:])
        SETTINGS['USER'].draw()

    if SETTINGS['MENU_PASSED']:
        main_menu(SETTINGS)

    pygame.display.update()

pygame.quit()
print("Игра завершена")