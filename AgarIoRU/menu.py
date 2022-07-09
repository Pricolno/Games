import pygame
import sys

from button import Button

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
        SETTINGS['OPEN_MENU'] = False
        SETTINGS['OPEN_MAIN_MENU'] = False
    else:
        print('PLAY and I"m death')
        SETTINGS['OPEN_MAIN_MENU'] = False
        SETTINGS['OPEN_MENU'] = False

        SETTINGS['USER'].reborn()






def options(SETTINGS):
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

    SETTINGS['SCREEN'].fill("white")

    OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SETTINGS['WIDTH_WINDOW'] // 2, MARGIN_HEIGHT))
    SETTINGS['SCREEN'].blit(OPTIONS_TEXT, OPTIONS_RECT)

    OPTIONS_BACK = Button(image=None, pos=(SETTINGS['WIDTH_WINDOW'] // 2, 3 * MARGIN_HEIGHT),
                          text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

    OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
    OPTIONS_BACK.update(SETTINGS['SCREEN'])

    #print("Я в настройках")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SETTINGS['SERVER_WORK'] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                SETTINGS['OPEN_OPTIONS'] = False
                SETTINGS['OPEN_MAIN_MENU'] = True


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

    if SETTINGS['OPEN_OPTIONS']:
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
