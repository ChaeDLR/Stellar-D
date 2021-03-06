from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame import mouse, event

from ...base import MenuBase
from ...assets import keys


class MainMenu(MenuBase):
    def __init__(self):
        super().__init__("Stellar-D", [keys.buttons.play, keys.buttons.quit])
        self.next_screen: str = "level"
        mouse.set_visible(True)

    def check_events(self, _event):
        if _event.type == MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.check_button(_event.pos)
        elif _event.type == MOUSEBUTTONUP:
            for button in self.buttons:
                if button.check_button(_event.pos, True):
                    if button.key == keys.buttons.play:
                        event.post(event.Event(self.CHANGESCREEN))
                    elif button.key == keys.buttons.quit:
                        event.clear()
                        event.post(event.Event(QUIT))

    def update(self):
        self.image.fill((0, 0, 0))
        self.image.blits(self.button_blit_seq)
        self.image.blit(self.title, self.title_rect)
