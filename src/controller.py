import pygame
import config
from model import GameModel
from ui import GameUI
from sprites.player import Player

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.model = GameModel()
        self.ui = GameUI(screen)

    def handle_events(self):
        """Отвечает за обработку событий, таких как нажатия клавиш и закрытие окна"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.model.is_running = False
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.model.state in ["GAME", "WIN_1", "WIN_2"]:
                        self.model.state = "MENU"
                    elif self.model.state == "DEAD":
                        self.model.state = "MENU"
                    elif self.model.state == "MENU":
                        self.model.is_running = False
                        return False

                elif event.key == pygame.K_m and self.model.state in ["GAME", "PLOT"]:
                    self.model.state = "PLOT" if self.model.state == "GAME" else "GAME"

                elif event.key == pygame.K_TAB and self.model.state in ["GAME", "INVENTORY"]:
                    self.model.state = "INVENTORY" if self.model.state == "GAME" else "GAME"

                elif event.key == pygame.K_RETURN and self.model.state == "MENU":
                    self.model.current_level = 0
                    self.model._build_level()
                    self.model.player = Player(*self.model.player_spawn)
                    self.model.checkpoint_level = 0
                    self.model.checkpoint_pos = self.model.player_spawn
                    self.model.has_saved = False
                    self.model.state = "GAME"

                elif event.key == pygame.K_RETURN and self.model.state == "DEAD":
                    self.model._build_level()
                    self.model.player = None
                    self.model.state = "MENU"

                elif event.key == pygame.K_z and self.model.state == "GAME" and self.model.player:
                    self.model.player.activate_red_light()

                elif event.key == pygame.K_x and self.model.state == "GAME" and self.model.player:
                    self.model.player.activate_green_light()

                elif event.key == pygame.K_e and self.model.state == "GAME" and self.model.player:
                    self.model.player.attack(self.model.enemies)

                elif event.key == pygame.K_f and self.model.state == "GAME" and self.model.player:
                    self.model._try_open_chest()

                elif event.key == pygame.K_r and self.model.state == "GAME" and self.model.player:
                    self.model._try_activate_savepoint()

        if self.model.state == "GAME" and self.model.player:
            self._handle_player_movement(events)
            self.model.enemies = pygame.sprite.Group(*[enemy for enemy in self.model.enemies if enemy.is_alive])
            self.model.chests = pygame.sprite.Group(*[chest for chest in self.model.chests if not chest.opened])

            if self.model.player.rect.x < 0:
                if self.model.current_level == 1:
                    self.model.state = "WIN_1"
                else:
                    self.model.player.rect.x = 0
            elif self.model.player.rect.x > config.SCREEN_WIDTH:
                if self.model.current_level == 0:
                    self.model.current_level = 1
                    self.model._build_level()
                    self.model.player.rect.topleft = (10, 300)
                    self.model.player.velocity_x = 0
                    self.model.player.velocity_y = 0
                elif self.model.current_level == 1:
                    self.model.current_level = 2
                    self.model._build_level()
                    self.model.player.rect.topleft = (10, 300)
                    self.model.player.velocity_x = 0
                    self.model.player.velocity_y = 0
                elif self.model.current_level == 2:
                    if self.model.boss_defeated:
                        self.model.state = "WIN_2"
                    else:
                        self.model.player.rect.right = config.SCREEN_WIDTH

            if self.model.player.hp <= 0:
                if not self.model.has_saved:
                    self.model.state = "DEAD"
                else:
                    self.model._respawn_at_checkpoint()

        return True

    def _handle_player_movement(self, events):
        '''отвечает за движение игрока'''
        if not self.model.player:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.model.player.move_left()
        elif keys[pygame.K_d]:
            self.model.player.move_right()
        else:
            self.model.player.stop_horizontal()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.model.player.jump()

    def update(self, dt):
        self.model.update(dt)

    def render(self):
        self.ui.render(self.model)
