import pygame
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Crazy Shooter")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Fill the screen with black

        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS

if __name__ == "__main__":
    main()