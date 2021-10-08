from .background import Background
from ..settings import screen_dims

from abc import ABCMeta
from pygame import Surface
from pygame.constants import SRCALPHA


class ScreenBase(metaclass=ABCMeta):
    """
    Store all of the code every screen in the game will need access to
    """

    # bool to tell the main loop to reassign the active screen
    change_screen: bool = False
    # next active screen's key | First active screen is main menu
    # screen's key will be the file name of the screen without ".py"
    new_screen: str = "main_menu"

    background = Background(screen_dims)
    width, height = screen_dims

    image = Surface(screen_dims, flags=SRCALPHA)
    rect = image.get_rect()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "check_events")
            and callable(subclass.check_events)
            and hasattr(subclass, "update")
            and callable(subclass.update)
        )
