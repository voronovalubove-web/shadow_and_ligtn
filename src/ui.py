import pygame
import config


class GameUI:
	def __init__(self, screen):
		self.screen = screen

	def render(self, engine):
		self.screen.fill(config.COLOR_BLACK)

		if engine.state == "MENU":
			self._render_menu()
		elif engine.state == "GAME":
			self._render_game(engine)
		elif engine.state == "PLOT":
			self._render_plot(engine)
		elif engine.state == "INVENTORY":
			self._render_inventory(engine)
		elif engine.state == "WIN_1":
			self._render_win_1()
		elif engine.state == "DEAD":
			self._render_dead()

		pygame.display.flip()

	def _render_level_scene(self, engine):
		engine.platforms.draw(self.screen)
		engine.savepoints.draw(self.screen)
		engine.chests.draw(self.screen)
		engine.enemies.draw(self.screen)

		if engine.player:
			self.screen.blit(engine.player.image, engine.player.rect)

	def _render_light(self, engine):
		if engine.player:
			engine.player.light.draw_overlay(self.screen, engine.player.rect.center)

	def _render_menu(self):
		font = pygame.font.Font(None, 48)
		text = font.render("ТЕНЬ И СВЕТ: НАЖМИТЕ ENTER ДЛЯ СТАРТА", True, config.COLOR_AMBER)
		rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
		self.screen.blit(text, rect)

	def _render_hud(self, engine, font):
		if not engine.player:
			return

		hp_ratio = max(0.0, min(1.0, engine.player.hp / config.MAX_HP))
		mana_ratio = max(0.0, min(1.0, engine.player.mana / config.MAX_MANA))
		light_ratio = engine.player.light.base_ratio

		self.screen.blit(font.render("HP", True, config.COLOR_WHITE), (20, 20))
		pygame.draw.rect(self.screen, config.COLOR_GRAY, (70, 20, 160, 18))
		pygame.draw.rect(self.screen, config.COLOR_GREEN, (70, 20, int(160 * hp_ratio), 18))

		self.screen.blit(font.render("СВЕТ", True, config.COLOR_WHITE), (20, 45))
		pygame.draw.rect(self.screen, config.COLOR_GRAY, (70, 45, 160, 18))
		pygame.draw.rect(self.screen, config.COLOR_AMBER, (70, 45, int(160 * light_ratio), 18))

		self.screen.blit(font.render("МАНА", True, config.COLOR_WHITE), (20, 70))
		pygame.draw.rect(self.screen, config.COLOR_GRAY, (70, 70, 160, 18))
		pygame.draw.rect(self.screen, config.COLOR_BLUE, (70, 70, int(160 * mana_ratio), 18))

		hint_text = font.render("E - атака, F - сундук, R - сохранение, Z - красный свет, X - зеленый свет, M - сюжет, Tab - инвентарь", True, config.COLOR_WHITE)
		self.screen.blit(hint_text, (20, 96))

	def _render_game(self, engine):
		self._render_level_scene(engine)
		self._render_light(engine)

		font = pygame.font.Font(None, 24)
		self._render_hud(engine, font)

		if engine.enemies:
			enemy = next(iter(engine.enemies))
			hp_text = font.render(f"Враг HP: {enemy.hp}/{enemy.max_hp}", True, config.COLOR_WHITE)
			self.screen.blit(hp_text, (20, 120))

	def _render_dead(self):
		dark_overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
		dark_overlay.fill((0, 0, 0, 210))
		self.screen.blit(dark_overlay, (0, 0))

		font = pygame.font.Font(None, 64)
		title = font.render("СТРАННИК ПАЛ", True, config.COLOR_RED)
		title_rect = title.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 60))
		self.screen.blit(title, title_rect)

		button_font = pygame.font.Font(None, 44)
		button_text = button_font.render("НАЧАТЬ СНАЧАЛА", True, config.COLOR_WHITE)
		button_rect = button_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 20))
		pygame.draw.rect(self.screen, config.COLOR_GRAY, button_rect.inflate(40, 24), border_radius=10)
		self.screen.blit(button_text, button_rect)

		hint_font = pygame.font.Font(None, 28)
		hint = hint_font.render("Нажмите Enter, чтобы вернуться в меню", True, config.COLOR_WHITE)
		hint_rect = hint.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 70))
		self.screen.blit(hint, hint_rect)

	def _render_text_wrapped(self, text, font, color, rect):
		words = text.split(' ')
		space_width, space_height = font.size(' ')
		max_width = rect.width
		x, y = rect.topleft
		
		line = []
		for word in words:
			test_line = line + [word]
			test_line_str = ' '.join(test_line)
			line_width, line_height = font.size(test_line_str)
			if line_width > max_width:
				line_str = ' '.join(line)
				line_surface = font.render(line_str, True, color)
				self.screen.blit(line_surface, (x, y))
				y += line_height + 4
				line = [word]
			else:
				line = test_line
		
		if line:
			line_str = ' '.join(line)
			line_surface = font.render(line_str, True, color)
			self.screen.blit(line_surface, (x, y))
			y += space_height + 4
		
		return y

	def _render_plot(self, engine):
		pygame.draw.rect(self.screen, (20, 20, 35), (80, 50, config.SCREEN_WIDTH - 160, config.SCREEN_HEIGHT - 100), border_radius=15)
		pygame.draw.rect(self.screen, config.COLOR_BLUE, (80, 50, config.SCREEN_WIDTH - 160, config.SCREEN_HEIGHT - 100), 2, border_radius=15)

		font_title = pygame.font.Font(None, 44)
		text_title = font_title.render("СЮЖЕТ ИГРЫ (M - Выход)", True, (120, 220, 255))
		self.screen.blit(text_title, (110, 80))

		pygame.draw.line(self.screen, (86, 86, 252, 100), (110, 130), (config.SCREEN_WIDTH - 110, 130), 1)

		if not engine.unlocked_stories:
			font_placeholder = pygame.font.Font(None, 32)
			text = font_placeholder.render("История пока пуста. Активируйте костры (Базы) на уровнях, чтобы открыть главы сюжета.", True, (150, 150, 150))
			text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
			self.screen.blit(text, text_rect)
		else:
			y = 160
			font_story = pygame.font.Font(None, 28)
			for i, story in enumerate(engine.unlocked_stories):
				bullet_text = f"Глава {i + 1}:"
				bullet_surf = font_story.render(bullet_text, True, config.COLOR_AMBER)
				self.screen.blit(bullet_surf, (120, y))
				
				rect = pygame.Rect(220, y, config.SCREEN_WIDTH - 360, 200)
				y = self._render_text_wrapped(story, font_story, config.COLOR_WHITE, rect)
				y += 20

	def _render_inventory(self, engine):
		font_title = pygame.font.Font(None, 48)
		font_item = pygame.font.Font(None, 36)
		title_text = font_title.render("СВИТКИ ЗАКЛИНАНИЙ (Tab - Выход):", True, config.COLOR_GREEN)
		self.screen.blit(title_text, (50, 50))

		if engine.player:
			start_y = 150
			for i, item in enumerate(engine.player.inventory):
				item_text = font_item.render(f"{i + 1}. {item}", True, config.COLOR_WHITE)
				self.screen.blit(item_text, (80, start_y + (i * 50)))

	def _render_win_1(self):
		font = pygame.font.Font(None, 48)
		text = font.render("КОНЦОВКА №1: СТРАННИК УШЕЛ ДОМОЙ", True, config.COLOR_GREEN)
		rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
		self.screen.blit(text, rect)