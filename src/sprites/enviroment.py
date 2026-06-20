#платформы, базы, шипы, сундуки и пр.
# pyrefly: ignore [missing-import]
import pygame
import config
from pathlib import Path
from sprites.enemies import BaseEnemy



LEVEL_FILE = Path(__file__).resolve().parents[2] / "levels" / "level1.txt"

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


def _load_level_grid(level_path=LEVEL_FILE):
    with open(level_path, "r", encoding="utf-8") as level_file:
        return [line.rstrip("\n") for line in level_file if line.strip()]


def _tile_rect(column, row):
    return pygame.Rect(column * config.LEVEL_SIZE , row * config.LEVEL_SIZE , config.LEVEL_SIZE , config.LEVEL_SIZE )


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, spell_name, mana_restore):
        super().__init__()
        self.image = pygame.Surface((32, 24))
        self.image.fill(config.COLOR_YELLOW)
        pygame.draw.rect(self.image, config.COLOR_GRAY, (0, 0, 32, 24), 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spell_name = spell_name
        self.mana_restore = mana_restore
        self.opened = False

    def open(self):
        if self.opened:
            return None

        self.opened = True
        self.image.fill(config.COLOR_GRAY)
        pygame.draw.rect(self.image, config.COLOR_BLACK, (0, 0, 32, 24), 2)
        return {
            "spell_name": self.spell_name,
            "mana_restore": self.mana_restore,
        }


class SavePoint(pygame.sprite.Sprite):
    def __init__(self, x, y, story_text):
        super().__init__()
        self.image = pygame.Surface((36, 48))
        self.image.fill(config.COLOR_AMBER)
        pygame.draw.rect(self.image, config.COLOR_WHITE, (0, 0, 36, 48), 2)
        pygame.draw.circle(self.image, config.COLOR_RED, (18, 18), 8)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.story_text = story_text
        self.activated = False

    def activate(self):
        self.activated = True
        self.image.fill(config.COLOR_GREEN)
        pygame.draw.rect(self.image, config.COLOR_WHITE, (0, 0, 36, 48), 2)
        pygame.draw.circle(self.image, config.COLOR_YELLOW, (18, 18), 8)
        return {
            "story_text": self.story_text,
        }


def build_level_objects(level_path=LEVEL_FILE):
    grid = _load_level_grid(level_path)
    platforms = []
    enemies = []
    chests = []
    savepoints = []
    player_spawn = (150, 400)
    has_custom_objects = False

    level_name = Path(level_path).stem
    level_idx = 0
    for char in level_name:
        if char.isdigit():
            level_idx = int(char)
            break

    for row_index, row in enumerate(grid):
        for column_index, cell in enumerate(row):
            tile_rect = _tile_rect(column_index, row_index)

            if cell == "W":
                platforms.append(Platform(tile_rect.x, tile_rect.y, tile_rect.width, tile_rect.height, config.COLOR_GRAY))
            elif cell == "P":
                player_spawn = (tile_rect.x, tile_rect.y - 40)
            elif cell.lower() == "c":
                cx = tile_rect.x + (config.LEVEL_SIZE - 32) // 2
                cy = tile_rect.y + config.LEVEL_SIZE - 24
                chest_idx = level_idx + len(chests)
                spell_name, mana_restore = config.FUNNY_SPELLS[chest_idx]
                chests.append(Chest(cx, cy, spell_name, mana_restore))
                has_custom_objects = True
            elif cell.lower() == "f":
                sx = tile_rect.x + (config.LEVEL_SIZE - 36) // 2
                sy = tile_rect.y + config.LEVEL_SIZE - 48
                sp_idx = level_idx + len(savepoints)
                story_text = config.STORY_TEXTS[sp_idx]
                savepoints.append(SavePoint(sx, sy, story_text))
                has_custom_objects = True
            elif cell.lower() == "e":
                ex = tile_rect.x + (config.LEVEL_SIZE - 40) // 2
                ey = tile_rect.y + config.LEVEL_SIZE - 50
                enemies.append(BaseEnemy(ex, ey))
                has_custom_objects = True

    return platforms, enemies, chests, savepoints, player_spawn


def build_level_groups(level_path=LEVEL_FILE):
    platforms, enemies, chests, savepoints, player_spawn = build_level_objects(level_path)

    platform_group = pygame.sprite.Group(*platforms)
    enemy_group = pygame.sprite.Group(*enemies)
    chest_group = pygame.sprite.Group(*chests)
    savepoint_group = pygame.sprite.Group(*savepoints)

    return platform_group, enemy_group, chest_group, savepoint_group, player_spawn