import pygame
import config
from sprites.player import Player
from sprites.enviroment import Platform

class GameEngine:
    def __init__(self, screen):
        self.screen = screen
        self.player = None
        self.state = 'MENU'
        self.is_running = True

        self.platforms = pygame.sprite.Group()
        self._build_level()

    def _build_level(self):
        """Создаем тестовое окружение пещеры"""
        self.platforms.empty()
        
        # Пол под ногами странника
        floor = Platform(0, 550, config.SCREEN_WIDTH, 170, config.COLOR_GRAY)
        # Тестовая стена/препятствие справа
        wall = Platform(700, 350, 60, 200, config.COLOR_GRAY)
        
        self.platforms.add(floor, wall)
        

    def handle_events(self):
        '''Отвечает за обработку событий, таких как нажатия клавиш и закрытие окна'''
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    if self.state in ['GAME', 'WIN_1']:
                        self.state = 'MENU'
                    elif self.state == 'MENU':
                        self.is_running = False
                        return False

                elif event.key == pygame.K_m and self.state in ['GAME', 'MAP']:
                    if self.state == 'GAME':
                        self.state = 'MAP'
                    else:
                        self.state = 'GAME'

                elif event.key == pygame.K_TAB and self.state in ['GAME', 'INVENTORY']:
                    if self.state == 'GAME':
                        self.state = 'INVENTORY'
                    else:
                        self.state = 'GAME'

                elif event.key == pygame.K_RETURN and self.state == 'MENU':
                    self._build_level()
                    self.player = Player(150, 400)
                    self.state = 'GAME'

        if self.state == 'GAME':
            self.player.handle_imput()

            if self.player.rect.x < 0:
                self.state = 'WIN_1'

        return True
    

    def update(self, dt):
        if self.state == 'GAME' and self.player:
            self.player.update_logic(dt, self.platforms)
        elif self.state in ['MAP', 'INVENTORY']:
            pass  #  логика обновления карты


    def render(self):
        '''отрисовка текущего состояния игры на экране'''
        self.screen.fill(config.COLOR_BLACK)
        
        if self.state == "MENU":
            self._render_menu()
        elif self.state == "GAME":
            self._render_game()
        elif self.state == "MAP":
            self._render_map()
        elif self.state == "INVENTORY":
            self._render_inventory()
        elif self.state == "WIN_1":
            self._render_win_1()
            
        pygame.display.flip()
    

    def _render_menu(self):
        font = pygame.font.Font(None, 48)
        text = font.render("ТЕНЬ И СВЕТ: НАЖМИТЕ ENTER ДЛЯ СТАРТА", True, config.COLOR_AMBER)
        rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)

    def _render_game(self):
        self.platforms.draw(self.screen)
        
        if self.player:
            self.screen.blit(self.player.image, self.player.rect)
        
        font = pygame.font.Font(None, 24)
        text = font.render("ИГРА (Платформы и хитбоксы активны. Препятствие на X=700)", True, config.COLOR_WHITE)
        self.screen.blit(text, (20, 20))

    def _render_map(self):
        font = pygame.font.Font(None, 48)
        text = font.render("ЭКРАН КАРТЫ. НАЖМИТЕ M ДЛЯ ВЫХОДА", True, config.COLOR_BLUE)
        rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)

    def _render_inventory(self):
        font_title = pygame.font.Font(None, 48)
        font_item = pygame.font.Font(None, 36)
        title_text = font_title.render("СВИТКИ ЗАКЛИНАНИЙ (Tab - Выход):", True, config.COLOR_GREEN)
        self.screen.blit(title_text, (50, 50))

        if self.player:
            start_y = 150
            for i, item in enumerate(self.player.inventory):
                item_text = font_item.render(f"{i + 1}. {item}", True, config.COLOR_WHITE)
                self.screen.blit(item_text, (80, start_y + (i * 50)))

    def _render_win_1(self):
        font = pygame.font.Font(None, 48)
        text = font.render("КОНЦОВКА №1: СТРАННИК УШЕЛ ДОМОЙ", True, config.COLOR_GREEN)
        rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)