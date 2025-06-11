import pygame
import pygame.mixer
import sys
import random
import time

# Reinitialize the mixer with higher-quality settings
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load('Assets/background_music.mp3')
pygame.mixer.music.set_volume(0.4)  # Set the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music in a loop

# Set the mouse cursor to the default system cursor
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

# Load the sound effect
mouse_click_sound = pygame.mixer.Sound('Assets/AWP.mp3')
gameover_sound = pygame.mixer.Sound('Assets/gameover.mp3')
# Set the volume for the mouse click sound (0.5 is 50% volume)
mouse_click_sound.set_volume(0.1)

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_IMAGE = 'Assets/background.jpg'
TRASH_IMAGE = 'Assets/trash.png'
RACOON_IMAGE = 'Assets/racoon.png'
ENDGAME_IMAGE = 'Assets/evilRacoon.jpg'
MONSTER_IMAGE = 'Assets/monster.png'
MENU_IMAGE = 'Assets/Meniu3.png'
PLAY_BUTTON_IMAGE = 'Assets/PlayButton.png'
ICON = 'Assets/cat-icon.png'
TRASH_POSITIONS = [(640, 440), (27, 365), (60, 650), (293, 385)]
RACOON_DISPLAY_TIME = 1200
RACOON_SPAWN_COOLDOWN = 900
AWP_SOUND_COOLDOWN = 15

class TrashCan(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor,health):
        super().__init__()
        self.health = health
        self.racoon_displayed = False
        self.image = pygame.image.load(TRASH_IMAGE)
        self.image = pygame.transform.scale(self.image, (int(118 * 1.3 * scale_factor), int(84 * 1.3 * scale_factor)))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.scale_factor = scale_factor
        self.spawn_time = pygame.time.get_ticks()
        self.racoon = Racoon(self)

    def handle_racoon(self, current_time, racoon_count,health):
        if self.racoon_displayed and current_time - self.spawn_time > RACOON_DISPLAY_TIME:
            self.racoon_displayed = False
            racoon_count -= 1
            health-=1
        return racoon_count,health

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

def render_text_with_outline(font, text, text_color, outline_color):
                    outline_surface = font.render(text, True, outline_color)
                    text_surface = font.render(text, True, text_color)
                    width, height = text_surface.get_size()
                    outline = pygame.Surface((width + 2, height + 2), pygame.SRCALPHA)
                    for dx, dy in [(-2, -2), (-2, 0), (-2, 1), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]:
                        outline.blit(outline_surface, (1 + dx, 1 + dy))
                    outline.blit(text_surface, (1, 1))
                    return outline

def main():
    racoon_count=0
    score=0
    health =3
    awp_coodown = 30
    # Set up the game screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Crazy Shooter")
    # Set the game icon
    icon = pygame.image.load(ICON)
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    
    button_not_pressed = True

    # intro screen
    while button_not_pressed == True:
        event_handler()
        screen.fill((255, 255, 255))  # Clear the screen
        background = pygame.transform.scale(pygame.image.load(MENU_IMAGE), (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))

        # Check for mouse clicks
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        play_button_image = pygame.image.load(PLAY_BUTTON_IMAGE)
        play_button_image = pygame.transform.scale(play_button_image, (play_button_image.get_width() / 5, play_button_image.get_height() / 5))  # Resize the button
        # Move the play button further down by increasing the y-coordinate
        button_rect = play_button_image.get_rect(midleft=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 235))
        screen.blit(play_button_image, button_rect)
        if mouse_click[0]:
            # Check if the click is within the button area

            if button_rect.collidepoint(mouse_x, mouse_y):
                button_not_pressed = False
                break

        pygame.display.flip()
        clock = pygame.time.Clock()
        clock.tick(60)

    background = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE), (SCREEN_WIDTH, SCREEN_HEIGHT))


    # Define the gradient start and end points
    gradient_start, gradient_end = (-50, 220), (400, 600)
    
    # Create a group for trash cans
    trash_group = pygame.sprite.Group()
    for pos in TRASH_POSITIONS:
        scale_factor = calculate_scale_factor(pos[1], gradient_start, gradient_end)
        trash_group.add(TrashCan(pos[0], pos[1], scale_factor,health))
    
    last_racoon_time = pygame.time.get_ticks()
    prev_click = False

    while True:
        event_handler()  # Handle events
        screen.fill((255, 255, 255)) # Clear the screen
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
            racoon_count,health = trash_can.handle_racoon(current_time, racoon_count,health)
            trash_can.draw(screen)
            trash_can.draw_racoon(screen)

        # Check for mouse clicks
        mouse_x, mouse_y = pygame.mouse.get_pos()   
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0]:
            if prev_click == False:
                prev_click = True
                if awp_coodown == 0:
                    mouse_click_sound.play()
                    awp_coodown = AWP_SOUND_COOLDOWN
                for trash_can in trash_group:
                    if trash_can.racoon_displayed and trash_can.racoon.rect.collidepoint(mouse_x, mouse_y):
                        racoon_count -= 1
                        trash_can.racoon_displayed = False
                        score += 1
                        break
        else:
            prev_click = False

        
        #reset cooldown
        if awp_coodown > 0:
            awp_coodown -= 3

        # display the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0)) 
        screen.blit(score_text, (SCREEN_WIDTH-score_text.get_width()-15, 10))
        monster_img=pygame.image.load(MONSTER_IMAGE)
        monster_img = pygame.transform.scale(monster_img, (monster_img.get_width() / 9, monster_img.get_height() / 9))
        # Display monster image based on health
        if health == 3:
            screen.blit(monster_img, (SCREEN_WIDTH-monster_img.get_width()-15,10+score_text.get_height()+10))
            screen.blit(monster_img, (SCREEN_WIDTH-monster_img.get_width() * 2 - 15 * 2,10 + score_text.get_height() + 10))
            screen.blit(monster_img, (SCREEN_WIDTH-monster_img.get_width() * 3 - 15 * 3,10 + score_text.get_height() + 10))
        elif health == 2:
            screen.blit(monster_img, (SCREEN_WIDTH-monster_img.get_width()-15,10+score_text.get_height()+10))
            screen.blit(monster_img, (SCREEN_WIDTH-monster_img.get_width() * 2 - 15 * 2,10 + score_text.get_height() + 10))
        elif health == 1:
            screen.blit(monster_img, (SCREEN_WIDTH-monster_img.get_width()-15,10+score_text.get_height()+10))
        elif health<=0:
            end_time = pygame.time.get_ticks() + 5000
            gameover_sound.play()
            while pygame.time.get_ticks() < end_time:
                event_handler()
                screen.fill((255, 255, 255))
                font = pygame.font.Font(None, 72)
                

                game_over_text = render_text_with_outline(font, "You ran out of energy :(", (255, 0, 0), (0, 0, 0))
                screen.blit(pygame.transform.scale(pygame.image.load(ENDGAME_IMAGE), (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
                pygame.display.flip()
            pygame.quit()
            sys.exit()

        pygame.display.flip()  # Update the display
        clock.tick(60)   # Cap the frame rate

if __name__ == "__main__":
    main()