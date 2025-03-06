import pygame
import sys
from enum import Enum

pygame.init()

background = pygame.image.load('Assets/background.jpg')
trash_positions = [(640, 440), (27, 365), (60, 650), (293, 385)]
pygame.mouse.set_cursor(pygame.cursors.broken_x)

class TrashCan(pygame.sprite.Sprite):
    def __init__(self, x, y, multiplier):
        super().__init__()
        self.image = pygame.image.load('Assets/trash.png')
        self.image = pygame.transform.scale(self.image, (118 * 1.3 * multiplier, 84 * 1.3 * multiplier))  # Scale the image to 50x50
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

        # self.image = pygame.Surface((50 * multiplier, 50 * multiplier))  # Create a surface
        # self.image.fill((255, 0, 0))  # Fill the surface with red color
        # self.rect = self.image.get_rect()
        # self.rect.midbottom = (x, y)

class GradientLine:
    def __init__(self, start_pos, end_pos, start_color, end_color):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.start_color = start_color
        self.end_color = end_color
        self.total_length = ((self.end_pos[0] - self.start_pos[0]) ** 2 + (self.end_pos[1] - self.start_pos[1]) ** 2) ** 0.5

    def draw(self, surface):
        pygame.draw.line(surface, self.start_color, self.start_pos, self.end_pos, 2)


def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Crazy Shooter")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()

    #line starts at upper left corner and ends at lower right corner
    gradient_line = GradientLine((-50, 220), (400, 600), (0, 0, 0), (0, 0, 255))
    y_max=gradient_line.start_pos[1]
    y_min=gradient_line.end_pos[1]
    x_max=gradient_line.end_pos[0]
    x_min=gradient_line.start_pos[0]

    # print(f"y_max: {y_max}, y_min: {y_min}, x_max: {x_max}, x_min: {x_min}")
    length=gradient_line.total_length

    for pos in trash_positions:
        #based on the position of the trash can, calculate the multiplier
        small_heigh = y_max - pos[1]
        big_base = x_max - x_min
        big_height = y_max - y_min
        small_base = big_base *  small_heigh / big_height
        hypothenuze = (small_base ** 2 + small_heigh ** 2) ** 0.5
        multiplier = hypothenuze / length * 2

        all_sprites.add(TrashCan(pos[0], pos[1], multiplier))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            

        screen.fill((0, 0, 0))  # Fill the screen with black
        screen.blit(pygame.transform.scale(background, (800, 600)), (0, 0))
        all_sprites.draw(screen)  # Draw all sprites

        gradient_line.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS

if __name__ == "__main__":
    main()