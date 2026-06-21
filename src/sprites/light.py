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
		'''рассчитывает отношение текущего времени свечения к максимальному'''
		if config.BASE_LIGHT_DURATION <= 0:
			return 0.0
		return max(0.0, min(1.0, self.base_timer / config.BASE_LIGHT_DURATION))

	@property
	def overlay_alpha(self):
		'''расчитывает уровень прозрачности черного слоя'''
		if self.active_mode == "dark":
			return config.BASE_LIGHT_DARK_ALPHA
		if self.active_mode == "magic":
			return config.BASE_LIGHT_NORMAL_ALPHA
		return int(
			config.BASE_LIGHT_DARK_ALPHA
			- (config.BASE_LIGHT_DARK_ALPHA - config.BASE_LIGHT_NORMAL_ALPHA) * self.base_ratio
		)

	def recharge_base(self):
		'''перезаряжает свет'''
		self.base_timer = config.BASE_LIGHT_DURATION
		self.magic_timer = 0.0
		self.active_mode = "base"
		self.active_color = config.COLOR_AMBER
		self.attack_damage_bonus = 1.0
		self.defense_damage_multiplier = 1.0
		self.block_environment_damage = False

	def activate_red(self, mana):
		'''активирует красный свет'''
		if self.base_timer <= 0 or mana < config.MANA_COST_SPELL:
			return mana, False

		self.magic_timer = config.MAGIC_LIGHT_DURATION
		self.active_mode = "magic"
		self.active_color = config.COLOR_RED
		self.attack_damage_bonus = config.BUFF_DAMAGE
		self.defense_damage_multiplier = 1.0
		self.block_environment_damage = False
		return mana - config.MANA_COST_SPELL, True

	def activate_green(self, mana):
		'''активирует зеленый свет'''
		if self.base_timer <= 0 or mana < config.MANA_COST_SPELL:
			return mana, False

		self.magic_timer = config.MAGIC_LIGHT_DURATION
		self.active_mode = "magic"
		self.active_color = config.COLOR_GREEN
		self.attack_damage_bonus = 1.0
		self.defense_damage_multiplier = config.BUFF_DEFENSE
		self.block_environment_damage = True
		return mana - config.MANA_COST_SPELL, True

	def update(self, dt):
		'''обновляет состояние света'''
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
