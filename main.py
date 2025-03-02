import pygame
import sys
from enum import Enum

pygame.init()

background = pygame.image.load('Assets/background.jpg')
trash_positions = [(640, 440), (27, 365), (60, 520), (293, 385)]
pygame.mouse.set_cursor(pygame.cursors.broken_x)

class TrashCan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Assets/trash.png')
        self.image = pygame.transform.scale(self.image, (118 * 1.3, 84 * 1.3))  # Scale the image to 50x50
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Crazy Shooter")
    clock = pygame.time.Clock()

    trash_can = TrashCan(375, 275)  # Create a TrashCan instance
    all_sprites = pygame.sprite.Group()
    for pos in trash_positions:
        all_sprites.add(TrashCan(pos[0], pos[1]))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            

        screen.fill((0, 0, 0))  # Fill the screen with black
        screen.blit(pygame.transform.scale(background, (800, 600)), (0, 0))
        all_sprites.draw(screen)  # Draw all sprites

        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS

if __name__ == "__main__":
    main()