#движение, инвентарь, мана, здоровье
# pyrefly: ignore [missing-import]
import pygame
import config
from sprites.light import LightController

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 30))
        self.image.fill(config.COLOR_WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        

        self.velocity_x = 0
        self.velocity_y = 0
        self.move_speed = config.PLAYER_SPEED
        self.on_ground = False
        self.facing_right = True
        self.attack_damage = config.BASE_DAMAGE

        self.hp = config.MAX_HP
        self.mana = config.MAX_MANA
        self.light = LightController()

        self.inventory = [
            "Подстричь ногти",
            "Атаковать",
            "Защититься"
        ]
    
    def handle_imput(self, events=None):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        if keys[pygame.K_a]:
            self.velocity_x = -self.move_speed
            self.facing_right = False
        if keys[pygame.K_d]:
            self.velocity_x = self.move_speed
            self.facing_right = True

        if events:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_w, pygame.K_SPACE) and self.on_ground:
                    self.velocity_y = -config.PLAYER_JUMP_POWER
                    self.on_ground = False

    def activate_red_light(self):
        self.mana, activated = self.light.activate_red(self.mana)
        return activated

    def activate_green_light(self):
        self.mana, activated = self.light.activate_green(self.mana)
        return activated

    def take_damage(self, amount):
        if self.light.block_environment_damage:
            return 0

        reduced_amount = int(round(amount * self.light.defense_damage_multiplier))
        reduced_amount = max(0, reduced_amount)
        self.hp = max(0, self.hp - reduced_amount)
        return reduced_amount

    def attack(self, enemies):
        attack_width = 35
        attack_height = 20
        if self.facing_right:
            attack_rect = pygame.Rect(self.rect.right, self.rect.centery - attack_height // 2, attack_width, attack_height)
        else:
            attack_rect = pygame.Rect(self.rect.left - attack_width, self.rect.centery - attack_height // 2, attack_width, attack_height)

        hit_enemy = False
        attack_damage = int(round(self.attack_damage * self.light.attack_damage_bonus))
        for enemy in enemies:
            if attack_rect.colliderect(enemy.rect):
                enemy.take_damage(attack_damage)
                hit_enemy = True

        return hit_enemy
    
    def update_logic(self, dt, platforms):
        self.light.update(dt)
        
        self.on_ground = False
        self.velocity_y += config.GRAVITY
        if self.velocity_y > 15:
            self.velocity_y = 15

        self.rect.x += self.velocity_x
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.velocity_x > 0:
                    self.rect.right = p.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = p.rect.right

        self.rect.y += self.velocity_y
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = p.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = p.rect.bottom
                    self.velocity_y = 0