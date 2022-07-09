import pygame as pg


class InputBox:

    def __init__(self, x, y, w, h, COLOR_INACTIVE_, COLOR_ACTIVE_, FONT_, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color_inactive = COLOR_INACTIVE_
        self.color_active = COLOR_ACTIVE_

        self.color = self.color_inactive

        self.font = FONT_

        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        result = None
        if event.type == pg.MOUSEBUTTONDOWN:


            #print(str(event.pos) + " " + str(self.rect.x) + " " + str(self.rect.y) +
            #      " " + str(self.rect.w) + " " + str(self.rect.h))
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print("Юзер ввел: {0}".format(self.text))
                    result = self.text
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)
        return result

    def update(self):
        # Resize the box if the text is too long.
        width = max(800, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))
    COLOR_INACTIVE = pg.Color('lightskyblue3')
    COLOR_ACTIVE = pg.Color('dodgerblue2')
    FONT = pg.font.Font(None, 32)


    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 10000, 32, COLOR_INACTIVE, COLOR_ACTIVE, FONT)
    #input_box2 = InputBox(100, 300, 140, 32, COLOR_INACTIVE, COLOR_ACTIVE, FONT)
    #input_boxes = [input_box1, input_box2]
    input_boxes = [input_box1]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()
