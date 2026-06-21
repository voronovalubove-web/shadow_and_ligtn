# pyrefly: ignore [missing-import]
import pygame
import config
from controller import GameController


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Shadow and Light")
    clock = pygame.time.Clock()
    controller = GameController(screen)


    running = True
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        running = controller.handle_events()

        if not running:
            break

        controller.update(dt)
        controller.render()
    
    pygame.quit()

if __name__ == "__main__":
    main()