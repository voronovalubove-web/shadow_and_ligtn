# pyrefly: ignore [missing-import]
import pygame
import config


class LightController:
	def __init__(self):
		self.base_timer = config.BASE_LIGHT_DURATION
		self.magic_timer = 0.0
		self.active_mode = "base"
		self.active_color = config.COLOR_AMBER
		self.attack_damage_bonus = 1.0
		self.defense_damage_multiplier = 1.0
		self.block_environment_damage = False

	@property
	def base_ratio(self):
		if config.BASE_LIGHT_DURATION <= 0:
			return 0.0
		return max(0.0, min(1.0, self.base_timer / config.BASE_LIGHT_DURATION))

	@property
	def base_radius(self):
		return config.BASE_LIGHT_RADIUS

	@property
	def overlay_alpha(self):
		if self.active_mode == "dark":
			return config.BASE_LIGHT_DARK_ALPHA
		if self.active_mode == "magic":
			return config.BASE_LIGHT_NORMAL_ALPHA
		return int(
			config.BASE_LIGHT_DARK_ALPHA
			- (config.BASE_LIGHT_DARK_ALPHA - config.BASE_LIGHT_NORMAL_ALPHA) * self.base_ratio
		)

	def recharge_base(self):
		self.base_timer = config.BASE_LIGHT_DURATION
		self.magic_timer = 0.0
		self.active_mode = "base"
		self.active_color = config.COLOR_AMBER
		self.attack_damage_bonus = 1.0
		self.defense_damage_multiplier = 1.0
		self.block_environment_damage = False

	def activate_red(self, mana):
		if self.base_timer <= 0 or mana < config.MANA_COST_SPELL:
			return mana, False

		self.magic_timer = config.MAGIC_LIGHT_DURATION
		self.active_mode = "magic"
		self.active_color = config.COLOR_RED
		self.attack_damage_bonus = 1.5
		self.defense_damage_multiplier = 1.0
		self.block_environment_damage = False
		return mana - config.MANA_COST_SPELL, True

	def activate_green(self, mana):
		if self.base_timer <= 0 or mana < config.MANA_COST_SPELL:
			return mana, False

		self.magic_timer = config.MAGIC_LIGHT_DURATION
		self.active_mode = "magic"
		self.active_color = config.COLOR_GREEN
		self.attack_damage_bonus = 1.0
		self.defense_damage_multiplier = 0.8
		self.block_environment_damage = True
		return mana - config.MANA_COST_SPELL, True

	def update(self, dt):
		if self.base_timer > 0:
			self.base_timer = max(0.0, self.base_timer - dt)

		if self.magic_timer > 0:
			self.magic_timer = max(0.0, self.magic_timer - dt)
			if self.magic_timer == 0:
				self.active_mode = "dark" if self.base_timer <= 0 else "base"
				self.active_color = config.COLOR_BLACK if self.active_mode == "dark" else config.COLOR_AMBER
				self.attack_damage_bonus = 1.0
				self.defense_damage_multiplier = 1.0
				self.block_environment_damage = False
		elif self.base_timer <= 0:
			self.active_mode = "dark"
			self.active_color = config.COLOR_BLACK

	def draw_overlay(self, surface, center):
		overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
		base_darkness = self.overlay_alpha

		if self.base_timer <= 0 and self.magic_timer <= 0:
			base_darkness = config.BASE_LIGHT_DARK_ALPHA

		overlay.fill((0, 0, 0, base_darkness))

		if self.active_mode == "magic":
			radius = config.RED_LIGHT_RADIUS if self.active_color == config.COLOR_RED else config.GREEN_LIGHT_RADIUS

			glow_surface = pygame.Surface((radius * 2 + 40, radius * 2 + 40), pygame.SRCALPHA)
			glow_center = (glow_surface.get_width() // 2, glow_surface.get_height() // 2)

			for step, alpha in ((radius + 16, 40), (radius + 8, 80), (radius, 180)):
				pygame.draw.circle(glow_surface, (*self.active_color, alpha), glow_center, step)

			overlay.blit(
				glow_surface,
				(center[0] - glow_center[0], center[1] - glow_center[1]),
				special_flags=pygame.BLEND_RGBA_ADD,
			)
			pygame.draw.circle(overlay, (*self.active_color, 40), center, radius)

		elif self.base_timer > 0:
			radius = self.base_radius
			glow_surface = pygame.Surface((radius * 2 + 60, radius * 2 + 60), pygame.SRCALPHA)
			glow_center = (glow_surface.get_width() // 2, glow_surface.get_height() // 2)

			for step, alpha in ((radius + 16, 40), (radius + 8, 80), (radius, 180)):
				pygame.draw.circle(glow_surface, (*config.COLOR_AMBER, alpha), glow_center, step)

			overlay.blit(
				glow_surface,
				(center[0] - glow_center[0], center[1] - glow_center[1]),
				special_flags=pygame.BLEND_RGBA_ADD,
			)
			pygame.draw.circle(overlay, (*config.COLOR_AMBER, 40), center, radius)

		surface.blit(overlay, (0, 0))