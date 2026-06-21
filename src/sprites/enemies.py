import pygame
import random
import config
from collections import deque


def find_path_bfs(grid, start, target):
	'''поиск пути с помощью алгоритма A*'''
	if not grid:
		return None

	rows = len(grid)
	cols = len(grid[0]) if rows > 0 else 0
	if cols == 0:
		return None

	def is_solid(c, r):
		if c < 0 or c >= cols or r < 0 or r >= rows:
			return True
		return grid[r][c] == 'W'

	queue = deque([(start, [start])])
	visited = {start}

	while queue:
		curr, path = queue.popleft()
		if curr == target:
			return path

		c, r = curr
		on_ground = is_solid(c, r + 1)

		possible_moves = []

		for dc in [-1, 1]:
			nc = c + dc
			nr = r
			if not is_solid(nc, nr):
				possible_moves.append((nc, nr))

		if on_ground:
			for dc in [-1, 0, 1]:
				for h in [1, 2, 3]:
					nc = c + dc
					nr = r - h
					blocked = False
					for step in range(1, h + 1):
						if is_solid(c, r - step):
							blocked = True
							break
					if not blocked and not is_solid(nc, nr):
						possible_moves.append((nc, nr))

		if not on_ground:
			nc = c
			nr = r + 1
			if not is_solid(nc, nr):
				possible_moves.append((nc, nr))

		for move in possible_moves:
			if move not in visited:
				visited.add(move)
				queue.append((move, path + [move]))

	return None


class BaseEnemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.max_hp = 50
		self.hp = self.max_hp
		self.image = pygame.Surface((40, 50))
		self.image.fill(config.COLOR_RED)
		self.rect = self.image.get_rect(topleft=(x, y))
		self.touch_damage_timer = 0.0
		self.touch_damage_interval = 1.0
		self.spawn_x = x
		self.spawn_y = y
		self.velocity_x = 0
		self.velocity_y = 0
		self.direction = 1
		self.on_ground = False

	def take_damage(self, amount):
		'''урон по врагу'''
		self.hp = max(0, self.hp - amount)
		if self.hp == 0:
			self.kill()

	def update(self, dt=0.0, platforms=None, player=None, level_grid=None):
		'''основная механика врага'''
		if self.touch_damage_timer > 0:
			self.touch_damage_timer = max(0.0, self.touch_damage_timer - dt)

		if platforms is None or player is None:
			return

		dx = player.rect.centerx - self.rect.centerx
		dy = player.rect.centery - self.rect.centery
		distance = (dx**2 + dy**2) ** 0.5

		state = "PATROL"
		if distance < config.ENEMY_DETECTION_RADIUS:
			state = "CHASE"

		if state == "CHASE":
			grid_size = config.LEVEL_SIZE
			rows_count = len(level_grid) if level_grid else 17
			cols_count = len(level_grid[0]) if (level_grid and rows_count > 0) else 32

			start_col = int(max(0, min(cols_count - 1, self.rect.centerx // grid_size)))
			start_row = int(max(0, min(rows_count - 1, (self.rect.bottom - 5) // grid_size)))

			target_col = int(max(0, min(cols_count - 1, player.rect.centerx // grid_size)))
			target_row = int(max(0, min(rows_count - 1, (player.rect.bottom - 5) // grid_size)))

			path = None
			if level_grid:
				path = find_path_bfs(level_grid, (start_col, start_row), (target_col, target_row))

			if path and len(path) > 1:
				next_c, next_r = path[1]

				if next_c > start_col:
					self.direction = 1
				elif next_c < start_col:
					self.direction = -1
				else:
					target_x = next_c * grid_size + grid_size // 2
					if self.rect.centerx < target_x - 4:
						self.direction = 1
					elif self.rect.centerx > target_x + 4:
						self.direction = -1

				if next_r < start_row and self.on_ground:
					self.velocity_y = -config.PLAYER_JUMP_POWER * 1.05
					self.on_ground = False
			else:
				if dx > 0:
					self.direction = 1
				else:
					self.direction = -1
		else:
			if self.direction == 1 and self.rect.centerx > self.spawn_x + config.ENEMY_PATROL_RADIUS:
				self.direction = -1
			elif self.direction == -1 and self.rect.centerx < self.spawn_x - config.ENEMY_PATROL_RADIUS:
				self.direction = 1

		active_speed = config.ENEMY_CHASE_SPEED if state == "CHASE" else config.ENEMY_PATROL_SPEED

		if player.light.active_mode == "dark":
			active_speed += config.ENEMY_DARK_SPEED_MULTIPLIER

		self.velocity_x = self.direction * active_speed

		self.velocity_y += config.GRAVITY
		if self.velocity_y > 15:
			self.velocity_y = 15
		self.rect.x += self.velocity_x
		for p in platforms:
			if self.rect.colliderect(p.rect):
				if self.velocity_x > 0:
					self.rect.right = p.rect.left
					if state != "CHASE":
						self.direction = -1
				elif self.velocity_x < 0:
					self.rect.left = p.rect.right
					if state != "CHASE":
						self.direction = 1
				self.velocity_x = 0

				if state == "CHASE" and self.on_ground:
					self.velocity_y = -config.PLAYER_JUMP_POWER * 1.05
					self.on_ground = False

		self.rect.y += self.velocity_y
		self.on_ground = False
		for p in platforms:
			if self.rect.colliderect(p.rect):
				if self.velocity_y > 0:
					self.rect.bottom = p.rect.top
					self.velocity_y = 0
					self.on_ground = True
				elif self.velocity_y < 0:
					self.rect.top = p.rect.bottom
					self.velocity_y = 0

	def can_touch_damage(self):
		return self.touch_damage_timer <= 0.0

	def reset_touch_damage_timer(self):
		self.touch_damage_timer = self.touch_damage_interval

	@property
	def is_alive(self):
		return self.hp > 0


class BossEnemy(BaseEnemy):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.max_hp = 100
		self.hp = self.max_hp
		self.image = pygame.Surface((50, 60))
		self.image.fill(config.COLOR_PURPLE)
		self.rect = self.image.get_rect(topleft=(x, y))
		self.touch_damage_interval = 0.8
		self.devour_timer = 15.0
		self.is_boss = True

	def update(self, dt=0.0, platforms=None, player=None, level_grid=None):
		'''основная механика босса'''
		super().update(dt, platforms, player, level_grid)

		if player and self.hp > 0:
			self.devour_timer -= dt
			if self.devour_timer <= 0:
				self.devour_timer = 8.0
				dx = player.rect.centerx - self.rect.centerx
				dy = player.rect.centery - self.rect.centery
				distance = (dx**2 + dy**2) ** 0.5
				if distance < config.ENEMY_DETECTION_RADIUS:
					if random.random() < 0.5:
						player.light.base_timer = max(0.0, player.light.base_timer - config.BASE_LIGHT_DURATION * 0.3)
						if hasattr(player, 'show_boss_notification'):
							player.show_boss_notification(duration=1.5)