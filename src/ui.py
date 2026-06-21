import pygame
import config


class GameUI:
	'''полностью отчевает за отрисовку окон, персонажа, врагов и пр.'''
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
		elif engine.state == "WIN_2":
			self._render_win_2()
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
		if not engine.player:
			return

		light = engine.player.light
		center = engine.player.rect.center
		overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
		base_darkness = light.overlay_alpha

		if light.base_timer <= 0 and light.magic_timer <= 0:
			base_darkness = config.BASE_LIGHT_DARK_ALPHA

		overlay.fill((0, 0, 0, base_darkness))

		if light.active_mode == "magic":
			radius = config.RED_LIGHT_RADIUS if light.active_color == config.COLOR_RED else config.GREEN_LIGHT_RADIUS

			glow_surface = pygame.Surface((radius * 2 + 40, radius * 2 + 40), pygame.SRCALPHA)
			glow_center = (glow_surface.get_width() // 2, glow_surface.get_height() // 2)

			for step, alpha in ((radius + 16, 40), (radius + 8, 80), (radius, 180)):
				pygame.draw.circle(glow_surface, (*light.active_color, alpha), glow_center, step)

			overlay.blit(
				glow_surface,
				(center[0] - glow_center[0], center[1] - glow_center[1]),
				special_flags=pygame.BLEND_RGBA_ADD,
			)
			pygame.draw.circle(overlay, (*light.active_color, 40), center, radius)

		elif light.base_timer > 0:
			radius = config.BASE_LIGHT_RADIUS
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

		self.screen.blit(overlay, (0, 0))

	def _render_menu(self):
		glow_surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
		center_x = config.SCREEN_WIDTH // 2
		center_y = config.SCREEN_HEIGHT // 2
		
		for r in range(400, 0, -8):
			alpha = int((1 - r / 400.0) ** 2 * 90)
			pygame.draw.circle(glow_surf, (*config.COLOR_AMBER, alpha), (center_x, center_y), r)
		self.screen.blit(glow_surf, (0, 0))

		pygame.draw.rect(self.screen, config.COLOR_AMBER, (50, 50, config.SCREEN_WIDTH - 100, config.SCREEN_HEIGHT - 100), 3, border_radius=15)
		
		font_title = pygame.font.Font(None, 64)
		title_text = "ТЕНЬ И СВЕТ"
		for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3)]:
			shadow_surf = font_title.render(title_text, True, (80, 50, 0))
			shadow_rect = shadow_surf.get_rect(center=(center_x + dx, center_y - 120 + dy))
			self.screen.blit(shadow_surf, shadow_rect)
			
		title_surf = font_title.render(title_text, True, config.COLOR_AMBER)
		title_rect = title_surf.get_rect(center=(center_x, center_y - 120))
		self.screen.blit(title_surf, title_rect)

		# Описание игры
		font_desc = pygame.font.Font(None, 36)
		desc_text = "Таинственные пещеры Владыки Тени полны смертоносных существ и древних тайн."
		desc_surf = font_desc.render(desc_text, True, config.COLOR_WHITE)
		desc_rect = desc_surf.get_rect(center=(center_x, center_y - 20))
		self.screen.blit(desc_surf, desc_rect)

		# Атмосферный текст
		font_flavor = pygame.font.Font(None, 28)
		flavor_text = "Управляйте светом, собирайте коллекцию заклинаний и выживайте во тьме!"
		flavor_surf = font_flavor.render(flavor_text, True, (200, 200, 200))
		flavor_rect = flavor_surf.get_rect(center=(center_x, center_y + 30))
		self.screen.blit(flavor_surf, flavor_rect)

		# Подсказка по управлению
		font_instr = pygame.font.Font(None, 24)
		instr_text = "A/D - Ходьба | W - Прыжок | Z - Красный свет (атака) | X - Зеленый свет (защита) | E - Удар"
		instr_surf = font_instr.render(instr_text, True, (160, 160, 160))
		instr_rect = instr_surf.get_rect(center=(center_x, center_y + 80))
		self.screen.blit(instr_surf, instr_rect)

		font_hint = pygame.font.Font(None, 36)
		hint_text = "Нажмите ENTER для начала приключения"
		hint_color = (155, 100, 0)
		hint_surf = font_hint.render(hint_text, True, hint_color)
		hint_rect = hint_surf.get_rect(center=(center_x, center_y + 180))
		self.screen.blit(hint_surf, hint_rect)

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

		if engine.player and hasattr(engine.player, 'boss_notification_timer') and engine.player.boss_notification_timer > 0:
			boss_font = pygame.font.Font(None, 36)
			boss_text = boss_font.render("ВЛАДЫКА ПОГЛОТИЛ ВАШ СВЕТ!", True, (255, 100, 100))
			boss_rect = boss_text.get_rect(center=(config.SCREEN_WIDTH // 2, 100))
			bg_rect = boss_rect.inflate(20, 10)
			bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
			bg_surf.fill((0, 0, 0, 180))
			self.screen.blit(bg_surf, bg_rect.topleft)
			self.screen.blit(boss_text, boss_rect)

	def _render_dead(self):
		dark_overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
		dark_overlay.fill((0, 0, 0, 210))
		self.screen.blit(dark_overlay, (0, 0))

		font = pygame.font.Font(None, 64)
		title = font.render("Я тебя предупреждал, глупый странник...", True, config.COLOR_RED)
		title_rect = title.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 60))
		self.screen.blit(title, title_rect)

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
		pygame.draw.rect(self.screen, (20, 20, 35), (80, 50, config.SCREEN_WIDTH - 160, config.SCREEN_HEIGHT - 100), border_radius=15)
		pygame.draw.rect(self.screen, config.COLOR_GREEN, (80, 50, config.SCREEN_WIDTH - 160, config.SCREEN_HEIGHT - 100), 2, border_radius=15)

		font_title = pygame.font.Font(None, 44)
		title_text = font_title.render("КНИГА ЗАКЛИНАНИЙ (Tab - Выход)", True, (120, 255, 180))
		self.screen.blit(title_text, (110, 80))

		pygame.draw.line(self.screen, (0, 180, 80, 100), (110, 130), (config.SCREEN_WIDTH - 110, 130), 1)

		if engine.player and engine.player.inventory:
			y = 160
			font_item = pygame.font.Font(None, 28)
			for i, item in enumerate(engine.player.inventory):
				bullet_text = f"Свиток {i + 1}:"
				bullet_surf = font_item.render(bullet_text, True, config.COLOR_AMBER)
				self.screen.blit(bullet_surf, (120, y))
				
				item_surf = font_item.render(item, True, config.COLOR_WHITE)
				self.screen.blit(item_surf, (240, y))
				
				y += 40
		
		font_hint = pygame.font.Font(None, 26)
		hint_surf = font_hint.render("Используйте Z и X во время игры для активации собранной магии", True, (120, 255, 180))
		hint_rect = hint_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 85))
		self.screen.blit(hint_surf, hint_rect)


	def _render_win_1(self):
		glow_surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
		center_x = config.SCREEN_WIDTH // 2
		center_y = config.SCREEN_HEIGHT // 2

		for r in range(400, 0, -8):
			alpha = int((1 - r / 400.0) ** 2 * 90)
			pygame.draw.circle(glow_surf, (*config.COLOR_GREEN, alpha), (center_x, center_y), r)
		self.screen.blit(glow_surf, (0, 0))

		pygame.draw.rect(self.screen, config.COLOR_GREEN, (50, 50, config.SCREEN_WIDTH - 100, config.SCREEN_HEIGHT - 100), 3, border_radius=15)

		font_title = pygame.font.Font(None, 64)
		title_text = "КОНЦОВКА: МУДРЕЦ ИЛИ ТРУС?"
		for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3)]:
			shadow_surf = font_title.render(title_text, True, (0, 45, 0))
			shadow_rect = shadow_surf.get_rect(center=(center_x + dx, center_y - 120 + dy))
			self.screen.blit(shadow_surf, shadow_rect)
			
		title_surf = font_title.render(title_text, True, (120, 255, 120))
		title_rect = title_surf.get_rect(center=(center_x, center_y - 120))
		self.screen.blit(title_surf, title_rect)

		font_desc = pygame.font.Font(None, 36)
		desc_text = "Не могу определиться ты трус или мудрец. Ну ладно это твой выбор"
		desc_surf = font_desc.render(desc_text, True, config.COLOR_WHITE)
		desc_rect = desc_surf.get_rect(center=(center_x, center_y - 20))
		self.screen.blit(desc_surf, desc_rect)

		font_flavor = pygame.font.Font(None, 28)
		flavor_text = "Вы продолжили свой путь, но мысль о пещерах и упущеном шансе вас не покидала..."
		flavor_surf = font_flavor.render(flavor_text, True, (200, 200, 200))
		flavor_rect = flavor_surf.get_rect(center=(center_x, center_y + 30))
		self.screen.blit(flavor_surf, flavor_rect)

		font_hint = pygame.font.Font(None, 32)
		hint_text = "Нажмите Escape для выхода в главное меню"
		hint_color = (50, 120, 0)
		hint_surf = font_hint.render(hint_text, True, hint_color)
		hint_rect = hint_surf.get_rect(center=(center_x, center_y + 180))
		self.screen.blit(hint_surf, hint_rect)

	def _render_win_2(self):
		glow_surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
		
		
		center_x = config.SCREEN_WIDTH // 2
		center_y = config.SCREEN_HEIGHT // 2
		for r in range(400, 0, -8):
			alpha = int((1 - r / 400.0) ** 2 * 110)
			pygame.draw.circle(glow_surf, (*config.COLOR_GOLD_GLOW, alpha), (center_x, center_y), r)
		
		self.screen.blit(glow_surf, (0, 0))

		pygame.draw.rect(self.screen, config.COLOR_GOLD, (50, 50, config.SCREEN_WIDTH - 100, config.SCREEN_HEIGHT - 100), 3, border_radius=15)
		
		font_title = pygame.font.Font(None, 64)
		title_text = "ФИНАЛ: ПОБЕДА НАД ТЬМОЙ"
		
		for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3)]:
			shadow_surf = font_title.render(title_text, True, (100, 65, 0))
			shadow_rect = shadow_surf.get_rect(center=(center_x + dx, center_y - 120 + dy))
			self.screen.blit(shadow_surf, shadow_rect)
			
		title_surf = font_title.render(title_text, True, (255, 230, 100))
		title_rect = title_surf.get_rect(center=(center_x, center_y - 120))
		self.screen.blit(title_surf, title_rect)

		font_desc = pygame.font.Font(None, 36)
		desc_text = "Признаюсь, я не ожидал от тебя такого. Молодец, но ради чего?"
		desc_surf = font_desc.render(desc_text, True, config.COLOR_WHITE)
		desc_rect = desc_surf.get_rect(center=(center_x, center_y - 20))
		self.screen.blit(desc_surf, desc_rect)

		font_flavor = pygame.font.Font(None, 28)
		flavor_text = "Вы получили самые бесполезные заклинания в вашей жизни."
		flavor_surf = font_flavor.render(flavor_text, True, (200, 200, 200))
		flavor_rect = flavor_surf.get_rect(center=(center_x, center_y + 30))
		self.screen.blit(flavor_surf, flavor_rect)

		font_hint = pygame.font.Font(None, 32)
		hint_text = "Нажмите Escape для выхода в главное меню"
		hint_color = (255, 255, 0)
		hint_surf = font_hint.render(hint_text, True, hint_color)
		hint_rect = hint_surf.get_rect(center=(center_x, center_y + 180))
		self.screen.blit(hint_surf, hint_rect)