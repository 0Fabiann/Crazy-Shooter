import pygame
import sys
pygame.init()
background=pygame.image.load('Assets/background.jpg')
pygame.mouse.set_cursor(pygame.cursors.broken_x)


def main():
    
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Crazy Shooter")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Fill the screen with black
        screen.blit(pygame.transform.scale(background, (800, 600)),(0,0))

        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS



if __name__ == "__main__":
    main()