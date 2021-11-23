from pygame import Vector2, sprite
from typing import Tuple
from ..settings import screen_dims
from .laser import Laser


class Ship(sprite.Sprite):
    """
    A base class for all of the ship sprites
    """

    def __init__(self, surface: dict):
        super().__init__()
        self.screen_dims = screen_dims

        self.image = surface["image"]
        self.colors = surface["colors"]
        self.rect = self.image.get_rect()
        self.x, self.y = float(self.rect.centerx), float(self.rect.centery)
        self.moving_left, self.moving_right = False, False
        self.base_speed: float = 5.5
        self.movement_speed: float = 5.5
        self.alpha: int = 255
        self.alpha_switch: int = 1
        self.image.set_alpha(self.alpha)
        self.animation_counter: int = 1
        self.side_switch: bool = True
        self.damaged: bool = False
        self.dying: bool = False

        self.lasers = sprite.Group()

    def __generate_particles(self) -> list:
        """
        Take a list of colors and generate a list of particles
        """
        particles: list = []
        for n, color in enumerate(self.colors):
            particles.append(
                _Particle(
                    color=color,
                    radius=(self.rect.w / 4) - n,
                    velocity=0.8 * (n + 1),
                    offset=(n, n),
                    center=self.rect.center,
                )
            )
        return particles

    def __animate(self) -> None:
        """
        animate sprite when hit
        """
        self.alpha += 50 * self.alpha_switch

        if not 0 <= self.alpha <= 255:
            self.alpha_switch *= -1
            self.animation_counter += 1
            self.alpha += 100 * self.alpha_switch

            if self.animation_counter == 6:
                self.__recover()
            self.image.set_alpha(self.alpha)

    def __recover(self) -> None:
        """
        reset after being damaged
        """
        self.damaged = False
        self.animation_counter = 1
        self.alpha = 255
        self.movement_speed = self.base_speed

    def create_laser(self, direction: int, pos_y: int) -> None:
        """
        create lasers and add it to the group
        """
        laser: Laser = Laser(direction)

        left_wing_position: int = self.rect.x + 13
        right_wing_position: int = self.rect.x + (self.rect.width - 18)

        if self.side_switch:
            laser.set_position(left_wing_position, pos_y)
            self.side_switch = False
        else:
            laser.set_position(right_wing_position, pos_y)
            self.side_switch = True

        self.lasers.add(laser)

    def take_damage(self, value) -> None:
        """
        Reduce player health and set bool
        """
        if not self.dying:
            self.__recover()
            self.health -= value
            if self.health <= 0:
                self.dying = True
                self.color_particles = self.__generate_particles()
            else:
                self.damaged = True
                self.movement_speed /= 2

    def set_position(self, x: float, y: float) -> None:
        """set player positions"""
        self.x, self.y = x, y
        self.rect.centerx, self.rect.centery = int(self.x), int(self.y)

    def update_particles(self) -> None:
        for particle in self.color_particles:
            particle.update()

    def update(self) -> None:
        """check for player updates"""
        if self.damaged:
            self.__animate()


class _Particle:

    directions: tuple = (
        # left
        (-1, 0),
        # right
        (1, 0),
        # up
        (0, -1),
        # down
        (0, 1),
        # top left
        (-1, -1),
        # bottom left
        (-1, 1),
        # top right
        (1, -1),
        # bottom right
        (1, 1),
    )

    def __init__(
        self,
        color: tuple,
        radius: int,
        velocity: float,
        offset: tuple,
        center: Tuple[int, int],
    ):

        self.color: tuple = color
        self.radius: int = radius
        self.velocity: float = velocity
        self.offset: tuple = offset

        self.alpha: float = 255.0
        Vector2()

        self.positions: list = [Vector2((0, 0)) for _ in self.directions]

        self.alpha: float = 255.0
        self.color[3] = int(self.alpha)
        for i, position in enumerate(self.positions):
            position.x = int(center[0] + (self.offset[0] * self.directions[i][0]))
            position.y = int(center[1] + (self.offset[1] * self.directions[i][1]))

    def update(self):
        """
        Move the particle
        Lower the alpha
        Lower the radius
        """
        for i in range(len(self.positions)):
            self.positions[i].x += int(self.velocity * self.directions[i][0])
            self.positions[i].y += int(self.velocity * self.directions[i][1])

        if self.alpha > 0.0:
            self.alpha -= self.velocity
        elif self.alpha < 0.0:
            self.alpha = 0.0

        self.color[3] = int(self.alpha)
        self.radius -= 0.2
