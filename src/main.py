import pygame
import config
from engine import GameEngine


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Shadow and Light")
    clock = pygame.time.Clock()
    engine = GameEngine(screen)


    running = True
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        running = engine.handle_events()

        if not running:
            break

        engine.update(dt)
        engine.render()
    
    pygame.quit()

if __name__ == "__main__":
    main()