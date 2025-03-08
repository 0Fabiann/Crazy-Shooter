import pygame
import sys
import random
import time

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_IMAGE = 'Assets/background.jpg'
TRASH_IMAGE = 'Assets/trash.png'
RACOON_IMAGE = 'Assets/racoon.png'
TRASH_POSITIONS = [(640, 440), (27, 365), (60, 650), (293, 385)]
RACOON_DISPLAY_TIME = 2000
RACOON_SPAWN_COOLDOWN = 900

class TrashCan(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor):
        super().__init__()
        self.racoon_displayed = False
        self.image = pygame.image.load(TRASH_IMAGE)
        self.image = pygame.transform.scale(self.image, (int(118 * 1.3 * scale_factor), int(84 * 1.3 * scale_factor)))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.scale_factor = scale_factor
        self.spawn_time = pygame.time.get_ticks()
        self.racoon = Racoon(self)

    def handle_racoon(self, current_time, racoon_count):
        if self.racoon_displayed and current_time - self.spawn_time > RACOON_DISPLAY_TIME:
            self.racoon_displayed = False
            racoon_count -= 1
        return racoon_count

    def draw_racoon(self, screen):
        if self.racoon_displayed:
            self.racoon.draw(screen)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Racoon(pygame.sprite.Sprite):
    def __init__(self, trash_can: TrashCan):
        super().__init__()
        # Load and scale the racoon image
        self.image = pygame.image.load(RACOON_IMAGE)
        self.image = pygame.transform.scale(self.image, (int(50 * trash_can.scale_factor), int(50 * trash_can.scale_factor)))
        self.rect = self.image.get_rect(center=trash_can.rect.midtop)

    def draw(self, screen):
        # Draw the racoon on the screen
        screen.blit(self.image, self.rect)

def calculate_scale_factor(y_position, gradient_start, gradient_end):
    # Calculate the scale factor based on the y position and gradient
    total_length = ((gradient_end[0] - gradient_start[0]) ** 2 + (gradient_end[1] - gradient_start[1]) ** 2) ** 0.5
    relative_height = gradient_start[1] - y_position
    scale_factor = (relative_height / (gradient_start[1] - gradient_end[1])) * (2 * total_length)
    return scale_factor / total_length

def event_handler():
    # Handle events such as quitting the game or pressing the escape key
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

def main():
    # Set up the game screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Crazy Shooter")
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE), (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Define the gradient start and end points
    gradient_start, gradient_end = (-50, 220), (400, 600)
    
    # Create a group for trash cans
    trash_group = pygame.sprite.Group()
    for pos in TRASH_POSITIONS:
        scale_factor = calculate_scale_factor(pos[1], gradient_start, gradient_end)
        trash_group.add(TrashCan(pos[0], pos[1], scale_factor))
    
    last_racoon_time = pygame.time.get_ticks()

    racoon_count=0

    while True:
        event_handler()  # Handle events
        screen.blit(background, (0, 0))  # Draw the background

        current_time = pygame.time.get_ticks()
        if current_time - last_racoon_time > RACOON_SPAWN_COOLDOWN:
            untoggled_trash_cans = [trash_can for trash_can in trash_group if not trash_can.racoon_displayed]
            if untoggled_trash_cans and racoon_count < 3:
                current_trash_can = random.choice(untoggled_trash_cans)
                current_trash_can.racoon_displayed = True
                current_trash_can.spawn_time = current_time
                racoon_count += 1
                last_racoon_time = current_time

        for trash_can in trash_group:
            racoon_count = trash_can.handle_racoon(current_time, racoon_count)
            trash_can.draw(screen)
            trash_can.draw_racoon(screen)

        pygame.display.flip()  # Update the display
        clock.tick(60)   # Cap the frame rate

if __name__ == "__main__":
    main()