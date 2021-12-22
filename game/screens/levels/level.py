import pygame

from .states import LevelOne
from ...sprites import Player
from ..screen_base import ScreenBase


class Level(ScreenBase):
    GAME_OVER = pygame.event.custom_type()

    def __init__(self) -> None:
        self.state = LevelOne()
        self.paused: bool = False

        self.player = Player()

        self.player.set_position(
            self.width / 2 - self.player.rect.width / 2,
            self.height - self.player.rect.height,
        )

        self.sprites = pygame.sprite.Group(self.player)

        pygame.mouse.set_cursor(pygame.cursors.broken_x)

    def __check_collisions(self):
        """check for collision between sprites"""
        for enemy in self.state.group.sprites():
            if enemy.health > 0:
                if p_lasers := pygame.sprite.spritecollide(
                    enemy, self.player.lasers, True
                ):
                    for laser in p_lasers:
                        enemy.take_damage(laser.damage)

            if e_lasers := pygame.sprite.spritecollide(self.player, enemy.lasers, True):
                for laser in e_lasers:
                    self.player.take_damage(laser.damage)
                    if self.player.health <= 0:
                        enemy.cancel_timers()
                        pygame.time.set_timer(self.GAME_OVER, 1500, True)

    def __player_keydown_controller(self, event):
        """respond to player inputs"""
        if hasattr(event, "button"):
            if self.player.health > 0 and event.button == 1:
                self.player.firing = True

        if hasattr(event, "key"):
            if event.key == pygame.K_a:
                self.player.moving_left = True

            if event.key == pygame.K_d:
                self.player.moving_right = True

    def __player_keyup_controller(self, event):
        if hasattr(event, "button"):
            if event.button == 1:
                self.player.firing = False

        if hasattr(event, "key"):
            if event.key == pygame.K_a:
                self.player.moving_left = False

            if event.key == pygame.K_d:
                self.player.moving_right = False

    def __update(self):
        """updates and displays game objects"""
        self.state.update(player_x=self.player.rect.centerx)
        self.__check_collisions()
        self.background.update()

        for sprite in self.sprites:
            if sprite.health > 0:
                sprite.update(play_x=self.player.rect.centerx)
            elif sprite.dying:
                sprite.update_particles()

    def __draw(self):
        self.image.blit(self.background.image, self.background.rect)

        for sprite in [*self.sprites.sprites(), *self.state.group.sprites()]:

            for laser in sprite.lasers:
                if 0 - laser.rect.height < laser.rect.y < self.height:
                    self.image.blit(laser.image, laser.rect)
                else:
                    laser.kill()

            if sprite.health > 0:
                self.image.blit(sprite.image, sprite.rect)
            elif sprite.dying:
                # switch to true if any particle still has an alpha > 0
                visible: bool = False
                for particle in sprite.color_particles:
                    if particle.alpha > 20.0:
                        visible = True
                        self.image.lock()
                        for position in particle.positions:
                            pygame.draw.circle(
                                self.image,
                                particle.color,
                                position,
                                particle.radius,
                            )
                        self.image.unlock()
                # if all of the particles have an alpha
                # less than zero remove sprite from all groups
                if not visible:
                    sprite.kill()

    def check_events(self, event: pygame.event.Event):
        """Check level events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = False if self.paused else True
            if self.paused:
                return
            self.__player_keydown_controller(event)

        elif event.type == pygame.KEYUP:
            self.__player_keyup_controller(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.__player_keydown_controller(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.__player_keyup_controller(event)

        if hasattr(event, "sprite"):
            self.state.check_events(event)

        if event.type == self.GAME_OVER:
            pygame.mouse.set_cursor(pygame.cursors.arrow)
            self.change_screen = True
            self.new_screen = "game_over"

    def update(self):
        """Update level elements and draw to level's main surface"""
        self.__update()
        self.__draw()
