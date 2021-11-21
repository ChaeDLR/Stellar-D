from pygame import Surface, event, time
from .laser import SLaser
from .ship import Ship


class Enemy(Ship):
    """basic enemy class"""

    def __init__(self, surface: Surface) -> None:
        super().__init__(surface)

        self.health: int = 4
        self.alpha: int = 255
        self.alpha_inc: int = -50

        self.BASIC_ATK = event.custom_type()
        self.SPECIAL_ATK = event.custom_type()

        self.basic_atk_event: event.Event = event.Event(
            self.BASIC_ATK, {"sprite": self}
        )
        self.special_atk_event: event.Event = event.Event(
            self.SPECIAL_ATK, {"sprite": self}
        )

    def __track(self, start: int, dest: int, speed: int = 40) -> float:
        """
        calculate a gradual movement from
        start ----> dest
        increase speed variable to track slower
        decrease to track faster
        """
        return (dest - start) / speed

    def cancel_timers(self):
        """cancel all of the enemy's timers"""
        time.set_timer(self.basic_atk_event, 0)
        time.set_timer(self.special_atk_event, 0)
        event.clear(eventtype=[self.basic_atk_event.type, self.special_atk_event.type])

    def create_laser(self):
        super().create_laser(1, self.rect.bottom)

    def create_special_laser(self):
        """
        Create a special attack laser object and add it to a sprite group
        """
        s_laser: SLaser = SLaser(1)
        s_laser.set_position(self.rect.midbottom[0], self.rect.midbottom[1])
        self.lasers.add(s_laser)

    def update(self, x: int, y: int):
        """
        Update enemy sprite
        """
        if x:
            self.x += self.__track(self.rect.centerx, x)
            self.rect.centerx = int(self.x)
        if y:
            self.y += self.__track(self.rect.centery, y)
            self.rect.centery = int(self.y)

        self.lasers.update()
        super().update()
