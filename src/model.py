import pygame
import config
import random
from pathlib import Path
from sprites.player import Player
from sprites.environment import build_level_groups, load_level_grid, Chest
from sprites.enemies import BossEnemy

class GameModel:
    def __init__(self):
        self.player = None
        self.state = 'MENU'
        self.is_running = True
        self.current_level = 0
        self.unlocked_stories = []
        self.checkpoint_level = 0
        self.checkpoint_pos = None
        self.has_saved = False

        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.savepoints = pygame.sprite.Group()
        self._build_level()
        self.checkpoint_pos = self.player_spawn

    def _build_level(self):
        """Создаем окружение пещеры"""
        level_path = Path(__file__).resolve().parent / ".." / "levels" / f"level{self.current_level}.txt"
        self.platforms, self.enemies, self.chests, self.savepoints, self.player_spawn = build_level_groups(level_path)
        self.level_grid = load_level_grid(level_path)

        self.boss_spawned = False
        self.boss_defeated = False
        self.boss_last_pos = None
        for enemy in self.enemies:
            if isinstance(enemy, BossEnemy):
                self.boss_spawned = True
                self.boss_last_pos = (enemy.rect.centerx - 16, enemy.rect.bottom - 24)

    def _try_open_chest(self):
        '''отвечает за корректное открытие сундуков и добавление строки в инвентарь'''
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
        '''отвечает за корректную активацию чекпоинта и сохранение игрока'''
        if not self.player:
            return

        for savepoint in self.savepoints:
            if not self.player.rect.colliderect(savepoint.rect):
                continue

            reward = savepoint.activate()
            if reward and "story_text" in reward:
                if reward["story_text"] not in self.unlocked_stories:
                    self.unlocked_stories.append(reward["story_text"])
            self.checkpoint_pos = (savepoint.rect.left - 20, savepoint.rect.top - 10)
            self.checkpoint_level = self.current_level
            self.has_saved = True
            self.player.hp = config.MAX_HP
            self.player.mana = config.MAX_MANA
            self.player.light.recharge_base()
            break

    def _respawn_at_checkpoint(self):
        '''отвечает за возрождение игрока после смерти'''
        if not self.player:
            return

        if self.checkpoint_level != self.current_level:
            self.current_level = self.checkpoint_level
            self._build_level()

        respawn_x, respawn_y = self.checkpoint_pos
        self.player.rect.topleft = (respawn_x, respawn_y)
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        self.player.hp = config.MAX_HP
        self.player.mana = config.MAX_MANA
        self.player.light.recharge_base()

    def update(self, dt):
        '''отвечает за обновление игрового процесса'''
        if self.state == "GAME" and self.player:
            self.player.update_logic(dt, self.platforms)
            self.enemies.update(dt, self.platforms, self.player, getattr(self, 'level_grid', None))

            if self.boss_spawned and not self.boss_defeated:
                boss_alive = False
                for enemy in self.enemies:
                    if getattr(enemy, 'is_boss', False):
                        self.boss_last_pos = (enemy.rect.centerx - 16, enemy.rect.bottom - 24)
                        boss_alive = True
                        break
                
                if not boss_alive:
                    self.boss_defeated = True
                    cx, cy = self.boss_last_pos if self.boss_last_pos else (200, 300)
                    chest = Chest(cx, cy, "Магия создания попкорна со вкусом вонючих ночков", 5)
                    self.chests.add(chest)

            for enemy in self.enemies:
                if not self.player.rect.colliderect(enemy.rect):
                    continue

                if enemy.can_touch_damage():
                    is_boss = getattr(enemy, 'is_boss', False)
                     
                    if is_boss:
                        base_damage = config.BOSS_TOUCH_DAMAGE
                    else:
                        base_damage = config.ENEMY_TOUCH_DAMAGE
                    
                    if self.player.light.active_mode == "dark":
                        base_damage = int(round(base_damage * config.ENEMY_DARK_DAMAGE_MULTIPLIER))
                    
                    if random.random() < config.ENEMY_CRIT_CHANCE:
                        base_damage = int(round(base_damage * config.ENEMY_CRIT_MULTIPLIER))
                        
                    self.player.take_damage(base_damage, is_enemy=True)
                    enemy.reset_touch_damage_timer()
