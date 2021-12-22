from pygame import event, time
from game.asset_manager import Assets
from .laser import SLaser
from .ship import Ship


class Enemy(Ship):
    """basic enemy class"""

    __size: tuple = (64, 64)

    def __init__(self, attack_speed: int = 1000) -> None:
        super().__init__(Assets.get_image("enemy"))

        self.health: int = 4
        self.alpha: int = 255
        self.alpha_inc: int = -50

        self.basicatk_event: event.Event = event.Event(
            event.custom_type(),
            {
                "sprite": self,
                "speed": attack_speed,
            },
        )
        self.specialatk_event: event.Event = event.Event(
            event.custom_type(),
            {
                "sprite": self,
                "speed": int(attack_speed * 2.25),
            },
        )

    def __track(self, start: int, dest: int, speed: int = 40) -> float:
        """
        calculate a gradual movement from
        start ----> dest
        increase speed variable to track slower
        decrease to track faster
        """
        return (dest - start) / speed

    @property.getter
    def get_size(self):
        return self.__size

    def take_damage(self, value):
        super().take_damage(value)
        if self.dying:
            self.cancel_timers()

    def cancel_timers(self):
        """cancel all of the enemy's timers"""
        time.set_timer(self.basicatk_event, 0)
        time.set_timer(self.specialatk_event, 0)
        event.clear(eventtype=[self.basicatk_event.type, self.specialatk_event.type])

    def create_laser(self):
        super().create_laser(1, self.rect.bottom)

    def create_special_laser(self):
        """
        Create a special attack laser object and add it to a sprite group
        """
        s_laser: SLaser = SLaser(1)
        s_laser.set_position(self.rect.midbottom[0], self.rect.midbottom[1])
        self.lasers.add(s_laser)

    def update_particles(self) -> None:
        super().update_particles()
        self.lasers.update()

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
