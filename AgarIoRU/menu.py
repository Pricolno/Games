import pygame
import sys

from button import Button
from input_button import InputBox

pygame.init()

MARGIN_HEIGHT = 100

pygame.display.set_caption("Menu")


# Returns Press-Start-2P in the desired size
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


BG = pygame.image.load("assets/Background.png")


def play(SETTINGS):
    if SETTINGS['USER'].is_alive():
        print('PLAY and I"m allive')
        SETTINGS['MENU_PASSED'] = False
        SETTINGS['OPEN_MAIN_MENU'] = False
    else:
        print('PLAY and I"m death')
        SETTINGS['OPEN_MAIN_MENU'] = False
        SETTINGS['MENU_PASSED'] = False

        SETTINGS['USER'].reborn()


def change_name(SETTINGS):
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

    OPTIONS_TEXT = get_font(45).render("Your name: {0}".format(SETTINGS['USER'].name), True, "Black")
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SETTINGS['WIDTH_WINDOW'] // 2, MARGIN_HEIGHT))
    SETTINGS['SCREEN'].blit(OPTIONS_TEXT, OPTIONS_RECT)

    OPTIONS_CHANGE_NAME = Button(image=None, pos=(SETTINGS['WIDTH_WINDOW'] // 2, 3 * MARGIN_HEIGHT),
                                 text_input="WINDOW FOR INPUT", font=get_font(75), base_color="BLACK",
                                 hovering_color="Green")

    if 'BUTTON_INPUT_NAME' not in dir(change_name):
        change_name.BUTTON_INPUT_NAME = InputBox(x=SETTINGS['WIDTH_WINDOW'] // 4, y=5 * MARGIN_HEIGHT,
                                                 w=round(SETTINGS['WIDTH_WINDOW'] * 3 / 4),
                                                 h=MARGIN_HEIGHT,
                                                 COLOR_INACTIVE_=(255, 117, 20),
                                                 COLOR_ACTIVE_=(200, 162, 200),
                                                 FONT_=get_font(75)
                                                 )

    OPTIONS_BACK = Button(image=None, pos=(SETTINGS['WIDTH_WINDOW'] // 2, 7 * MARGIN_HEIGHT),
                          text_input="BACK",
                          font=get_font(75),
                          base_color="Black",
                          hovering_color="Green")

    for button in [OPTIONS_CHANGE_NAME, OPTIONS_BACK]:
        button.changeColor(OPTIONS_MOUSE_POS)
        button.update(SETTINGS['SCREEN'])

    for event in pygame.event.get():
        new_name = change_name.BUTTON_INPUT_NAME.handle_event(event)
        if new_name is not None and new_name != '':
            # отправить серверу о просьбе поменять имя
            print("REQUEST: NEW_NAME={0}".format(new_name))
            SETTINGS['USER'].sock.send(('?' + new_name + '?').encode())


        if event.type == pygame.QUIT:
            SETTINGS['SERVER_WORK'] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                SETTINGS['OPEN_CHANGE_NAME'] = False
                SETTINGS['OPEN_OPTIONS'] = True
                SETTINGS['OPTIONS_PASSED'] = False
            if OPTIONS_CHANGE_NAME.checkForInput(OPTIONS_MOUSE_POS):
                # input реализовать
                pass

    change_name.BUTTON_INPUT_NAME.update()
    change_name.BUTTON_INPUT_NAME.draw(SETTINGS['SCREEN'])


def options(SETTINGS):
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

    OPTIONS_TEXT = get_font(45).render("Your name: {0}".format(SETTINGS['USER'].name), True, "Black")
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SETTINGS['WIDTH_WINDOW'] // 2, MARGIN_HEIGHT))
    SETTINGS['SCREEN'].blit(OPTIONS_TEXT, OPTIONS_RECT)

    OPTIONS_CHANGE_NAME = Button(image=None, pos=(SETTINGS['WIDTH_WINDOW'] // 2, 3 * MARGIN_HEIGHT),
                                 text_input="CHANGE NAME", font=get_font(75), base_color="BLACK",
                                 hovering_color="Green")

    OPTIONS_BACK = Button(image=None, pos=(SETTINGS['WIDTH_WINDOW'] // 2, 7 * MARGIN_HEIGHT),
                          text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

    if SETTINGS['OPTIONS_PASSED'] and SETTINGS['OPEN_CHANGE_NAME']:
        change_name(SETTINGS)
    else:
        for button in [OPTIONS_CHANGE_NAME, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SETTINGS['SCREEN'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SETTINGS['SERVER_WORK'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    SETTINGS['OPEN_OPTIONS'] = False
                    SETTINGS['OPEN_MAIN_MENU'] = True
                if OPTIONS_CHANGE_NAME.checkForInput(OPTIONS_MOUSE_POS):
                    # какую ту менюшку с сменой ника вернуть
                    SETTINGS['OPEN_CHANGE_NAME'] = True
                    SETTINGS['OPTIONS_PASSED'] = True
                    SETTINGS['OPEN_OPTIONS'] = False


def main_menu(SETTINGS):
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    # открыта главное меню
    if SETTINGS['OPEN_MAIN_MENU']:
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SETTINGS['WIDTH_WINDOW'] // 2, MARGIN_HEIGHT))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"),
                             pos=(SETTINGS['WIDTH_WINDOW'] // 2, 3 * MARGIN_HEIGHT),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"),
                                pos=(SETTINGS['WIDTH_WINDOW'] // 2, 5 * MARGIN_HEIGHT),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"),
                             pos=(SETTINGS['WIDTH_WINDOW'] // 2, 7 * MARGIN_HEIGHT),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SETTINGS['SCREEN'].blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SETTINGS['SCREEN'])

    if SETTINGS['OPTIONS_PASSED'] or SETTINGS['OPEN_OPTIONS']:
        options(SETTINGS)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SETTINGS['SERVER_WORK'] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if SETTINGS['OPEN_MAIN_MENU']:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        # нужно вернутсья в игру
                        # или начать заново
                        play(SETTINGS)

                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        SETTINGS['OPEN_OPTIONS'] = True
                        SETTINGS['OPEN_MAIN_MENU'] = False

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        SETTINGS['SERVER_WORK'] = False

    # pygame.display.update()


if __name__ == "__main__":
    # main_menu()
    pass
