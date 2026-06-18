#движение, инвентарь, мана, здоровье
import pygame
import config

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(config.COLOR_WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        

        self.velocity_x = 0
        self.velocity_y = 0
        self.move_speed = 5

        self.hp = 100
        self.mana = 50
        self.base_light_timer = 60.0

        self.inventory = [
            "Подстричь ногти",
            "Атаковать",
            "Защититься"
        ]
    
    def handle_imput(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        if keys[pygame.K_a]:
            self.velocity_x = -self.move_speed
        if keys[pygame.K_d]:
            self.velocity_x = self.move_speed
        if keys[pygame.K_w]:
            self.velocity_y = -self.move_speed
    
    def update_logic(self, dt, platforms):
        if self.base_light_timer > 0:
            self.base_light_timer -= dt
            if self.base_light_timer < 0:
                self.base_light_timer = 0
        
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
                elif self.velocity_y < 0:
                    self.rect.top = p.rect.bottom
                    self.velocity_y = 0