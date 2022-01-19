from pygame import Surface, font, RLEACCEL, SRCALPHA

from typing import Union


class Button:
    button_color: tuple = (144, 144, 144, 255)
    text_color: tuple = (255, 255, 255, 255)

    def __init__(
        self,
        button_text: str,
        size: tuple = (150, 50),
        font_size: int = 40,
        pos: tuple[int, int] = (0, 0),
    ):
        """
        surface: Surface -> Menu image,
        button_text: str -> text to display on top of button,
        size: tuple -> (width, height),
        font_size: int -> size of the text font,
        name: str -> uniqe string identifier
        """
        self.width, self.height = size

        self.image = Surface(size, flags=SRCALPHA).convert_alpha()
        self.image.fill(self.button_color)
        self.rect = self.image.get_rect()
        self.name = button_text

        self.set_text(button_text, font_size)
        self.set_position(pos)

    def set_text(self, text: str, font_size: int):
        """set the buttons msg_text and msg_text_rect"""
        text_font = font.SysFont(None, font_size, bold=True)
        self.msg_image = text_font.render(
            text, True, self.text_color, self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def check_button(self, mouse_pos, mouse_up: bool = False) -> bool:
        """check for button collision"""
        # If cursor is over the button when clicked
        if self.rect.collidepoint(mouse_pos):
            # if the mouse button was released over the button
            # and the button was the one pressed down on
            if mouse_up:
                if self.image.get_alpha() < 255:
                    self.reset_alpha()
                    return True
                # if the mouse button was release over this button
                # but a different button was clicked
                return False
            else:
                self.image.set_alpha(25, RLEACCEL)
                self.msg_image.set_alpha(25, RLEACCEL)
        # if user releases the mouse button and this button
        # was the one that was pressed
        elif self.image.get_alpha() < 255 and mouse_up:
            self.reset_alpha()

    def reset_alpha(self):
        self.image.set_alpha(255, RLEACCEL)
        self.msg_image.set_alpha(255, RLEACCEL)

    def set_position(self, x_pos: Union[int, tuple], y_pos: int = None):
        """Set the position of the rect"""
        if isinstance(x_pos, tuple):
            self.rect.center = x_pos
        else:
            if x_pos:
                self.rect.x = x_pos
            if y_pos:
                self.rect.y = y_pos
        self.msg_image_rect.center = self.rect.center
