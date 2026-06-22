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
        self.boss_notification_timer = 0.0

        self.inventory = config.BASE_INVENTORY
    
    def move_left(self):
        self.velocity_x = -self.move_speed
        self.facing_right = False

    def move_right(self):
        self.velocity_x = self.move_speed
        self.facing_right = True

    def stop_horizontal(self):
        self.velocity_x = 0

    def jump(self):
        if self.on_ground:
            self.velocity_y = -config.PLAYER_JUMP_POWER
            self.on_ground = False

    def activate_red_light(self):
        self.mana, activated = self.light.activate_red(self.mana)
        return activated

    def activate_green_light(self):
        self.mana, activated = self.light.activate_green(self.mana)
        return activated

    def take_damage(self, amount):
        '''получение урона'''
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
    
    def show_boss_notification(self, duration=1.5):
        self.boss_notification_timer = duration

    def update_logic(self, dt, platforms):
        self.light.update(dt)
        if hasattr(self, 'boss_notification_timer') and self.boss_notification_timer > 0:
            self.boss_notification_timer = max(0.0, self.boss_notification_timer - dt)
        
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