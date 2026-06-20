# pyrefly: ignore [missing-import]
import pygame
import config


class BaseEnemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.max_hp = 30
		self.hp = self.max_hp
		self.image = pygame.Surface((40, 50))
		self.image.fill(config.COLOR_RED)
		self.rect = self.image.get_rect(topleft=(x, y))
		self.touch_damage_timer = 0.0
		self.touch_damage_interval = 1.0

	def take_damage(self, amount):
		self.hp = max(0, self.hp - amount)
		if self.hp == 0:
			self.kill()

	def update(self, dt=0.0):
		if self.touch_damage_timer > 0:
			self.touch_damage_timer = max(0.0, self.touch_damage_timer - dt)

	def can_touch_damage(self):
		return self.touch_damage_timer <= 0.0

	def reset_touch_damage_timer(self):
		self.touch_damage_timer = self.touch_damage_interval

	@property
	def is_alive(self):
		return self.hp > 0