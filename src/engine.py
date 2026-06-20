# pyrefly: ignore [missing-import]
import pygame
import config
from pathlib import Path
from sprites.player import Player
from sprites.enviroment import build_level_groups
from ui import GameUI


class GameEngine:
    def __init__(self, screen):
        self.screen = screen
        self.player = None
        self.state = 'MENU'
        self.is_running = True
        self.current_level = 0
        self.unlocked_stories = []

        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.savepoints = pygame.sprite.Group()        
        self.ui = GameUI(screen)
        self._build_level()


    def handle_events(self):
        """Отвечает за обработку событий, таких как нажатия клавиш и закрытие окна"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state in ["GAME", "WIN_1"]:
                        self.state = "MENU"
                    elif self.state == "DEAD":
                        self.state = "MENU"
                    elif self.state == "MENU":
                        self.is_running = False
                        return False

                elif event.key == pygame.K_m and self.state in ["GAME", "PLOT"]:
                    self.state = "PLOT" if self.state == "GAME" else "GAME"

                elif event.key == pygame.K_TAB and self.state in ["GAME", "INVENTORY"]:
                    self.state = "INVENTORY" if self.state == "GAME" else "GAME"

                elif event.key == pygame.K_RETURN and self.state == "MENU":
                    self.current_level = 0
                    self._build_level()
                    self.player = Player(*self.player_spawn)
                    self.checkpoint = self.player_spawn
                    self.state = "GAME"

                elif event.key == pygame.K_RETURN and self.state == "DEAD":
                    self._build_level()
                    self.player = None
                    self.state = "MENU"

                elif event.key == pygame.K_z and self.state == "GAME" and self.player:
                    self.player.activate_red_light()

                elif event.key == pygame.K_x and self.state == "GAME" and self.player:
                    self.player.activate_green_light()

                elif event.key == pygame.K_e and self.state == "GAME" and self.player:
                    self.player.attack(self.enemies)

                elif event.key == pygame.K_f and self.state == "GAME" and self.player:
                    self._try_open_chest()

                elif event.key == pygame.K_r and self.state == "GAME" and self.player:
                    self._try_activate_savepoint()

        if self.state == "GAME" and self.player:
            self.player.handle_imput(events)
            self.enemies = pygame.sprite.Group(*[enemy for enemy in self.enemies if enemy.is_alive])
            self.chests = pygame.sprite.Group(*[chest for chest in self.chests if not chest.opened])

            if self.player.rect.x < 0:
                if self.current_level == 1:
                    self.state = "WIN_1"
                else:
                    self.player.rect.x = 0
            elif self.player.rect.x > config.SCREEN_WIDTH:
                if self.current_level == 0:
                    self.current_level = 1
                    self._build_level()
                    self.player.rect.topleft = (10, 300)
                    self.player.velocity_x = 0
                    self.player.velocity_y = 0
                    self.checkpoint = (10, 300)
                elif self.current_level == 1:
                    self.current_level = 2
                    self._build_level()
                    self.player.rect.topleft = (10, 300)
                    self.player.velocity_x = 0
                    self.player.velocity_y = 0
                    self.checkpoint = (10, 300)
                elif self.current_level == 2:
                    self.player.rect.right = config.SCREEN_WIDTH

            if self.player.hp <= 0:
                self._respawn_at_checkpoint()

        return True


    def _try_open_chest(self):
        if not self.player:
            return

        for chest in self.chests:
            if not self.player.rect.colliderect(chest.rect):
                continue

            reward = chest.open()
            if reward is None:
                continue

            self.player.inventory.append(reward["spell_name"])
            self.player.mana = min(config.MAX_MANA, self.player.mana + reward["mana_restore"])
            break


    def _try_activate_savepoint(self):
        if not self.player:
            return

        for savepoint in self.savepoints:
            if not self.player.rect.colliderect(savepoint.rect):
                continue

            reward = savepoint.activate()
            if reward and "story_text" in reward:
                if reward["story_text"] not in self.unlocked_stories:
                    self.unlocked_stories.append(reward["story_text"])
            self.checkpoint = (savepoint.rect.left - 20, savepoint.rect.top - 10)
            self.player.hp = config.MAX_HP
            self.player.mana = config.MAX_MANA
            self.player.light.recharge_base()
            break


    def _respawn_at_checkpoint(self):
        if not self.player:
            return

        respawn_x, respawn_y = self.checkpoint
        self.player.rect.topleft = (respawn_x, respawn_y)
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        self.player.hp = config.MAX_HP
        self.player.mana = config.MAX_MANA
        self.player.light.recharge_base()


    def _build_level(self):
        """Создаем окружение пещеры"""
        level_path = Path(__file__).resolve().parent / ".." / "levels" / f"level{self.current_level}.txt"
        self.platforms, self.enemies, self.chests, self.savepoints, self.player_spawn = build_level_groups(level_path)


    def update(self, dt):
        if self.state == "GAME" and self.player:
            self.player.update_logic(dt, self.platforms)
            self.enemies.update(dt)

            for enemy in self.enemies:
                if not self.player.rect.colliderect(enemy.rect):
                    continue

                if enemy.can_touch_damage():
                    self.player.take_damage(config.ENEMY_TOUCH_DAMAGE)
                    enemy.reset_touch_damage_timer()

    def render(self):
        self.ui.render(self)