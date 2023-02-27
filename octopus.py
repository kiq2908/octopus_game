import pygame
import random
import time
import os
import sys
pygame.mixer.pre_init(44100, -16, 2, 4096)
# Initialize Pygame
pygame.init()
#initialize text redering capability
#font = pygame.font.SysFont('Arial', 24)

#Get screen dimensions
infoObject = pygame.display.Info()

# Define the constants for the game
BACKGROUND = "background.jpg"
INTRO1 = "hungry.png"
INTRO2 = "saynomore.png"
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

#SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
GROUND = SCREEN_HEIGHT - 50 
GRAVITY = 0.5
JUMP_SPEED = 10
MOVE_SPEED = 5
TRASH_MOVE_SPEED = 0.001
FPS = 60
WINNING_SCORE = 20
GAME_IN_PROGRESS = True
COUNT_DOWN = 3
TOTAL_TIME = 0
# Create the Pygame screen and set its caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("octopus_icon.jpg")
pygame.display.set_icon(icon)
pygame.display.set_caption("Octopus")
music = pygame.mixer.Sound("music.ogg")

# Load the background image and scale it to the screen size
background = pygame.image.load(BACKGROUND).convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

intro1 = pygame.image.load(INTRO1).convert()
intro1 = pygame.transform.scale(intro1, (SCREEN_HEIGHT, SCREEN_HEIGHT))
intro1_rect = intro1.get_rect()
intro1_sound = pygame.mixer.Sound("intro1.mp3")
intro1_sound.set_volume(0.1)
# Set the x and y coordinates of intro1 at the center of the screen
intro1_x = (SCREEN_WIDTH - intro1_rect.width) // 2
intro1_y = 0

intro2 = pygame.image.load(INTRO2).convert()
intro2 = pygame.transform.scale(intro2, (SCREEN_HEIGHT, SCREEN_HEIGHT))
intro2_rect = intro2.get_rect()
intro2_sound = pygame.mixer.Sound("intro2.mp3")
intro2_sound.set_volume(0.1)

# Set the x and y coordinates of intro1 at the center of the screen
intro2_x = (SCREEN_WIDTH - intro2_rect.width) // 2
intro2_y = 0


# Set up the font object with font size of 36 pixels
font = pygame.font.Font(None, 50)
announcement_font = pygame.font.Font(None, 100)
# Define the Octopus class
class Octopus:
    def __init__(self, x, y, image_path):
        # Load the octopus images
        self.octopus_right = pygame.image.load("octopus_right.png").convert_alpha()
        self.octopus_left = pygame.image.load("octopus_left.png").convert_alpha()

        octopus_ratio_width = 5
        octopus_ratio_height = 5
        self.octopus_right = pygame.transform.scale(self.octopus_right, (int(self.octopus_right.get_width() / octopus_ratio_width), int(self.octopus_right.get_height() / octopus_ratio_height)))
        self.octopus_left = pygame.transform.scale(self.octopus_left, (int(self.octopus_left.get_width() / octopus_ratio_width), int(self.octopus_left.get_height() / octopus_ratio_height)))
        #set the octopus score
        self.score = 0

        # Set the octopus's initial position and velocity
        self.image = self.octopus_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = [0, 0]
        self.facing_left = False

    def update(self, keys):
        # Apply gravity to the octopus's velocity
        self.velocity[1] += GRAVITY

        # Move the octopus left or right based on arrow keys
        if keys[pygame.K_LEFT]:
            self.velocity[0] = -MOVE_SPEED
            self.facing_left = True
        elif keys[pygame.K_RIGHT]:
            self.velocity[0] = MOVE_SPEED
            self.facing_left = False
        else:
            self.velocity[0] = 0

        # Make the octopus jump if the up arrow key is pressed
        if keys[pygame.K_UP] and self.rect.bottom >= GROUND:
            self.velocity[1] = -JUMP_SPEED

        # Update the octopus's position based on its velocity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Constrain the octopus's position to the screen boundaries and above the ground
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > GROUND:
            self.rect.bottom = GROUND

        # Update the octopus's image based on its facing direction
        if self.facing_left:
            self.image = self.octopus_left
        else:
            self.image = self.octopus_right
    def collect_trash(self):
        self.score += 1
    def draw(self, screen):
        # Draw the octopus on the screen
        score_text = font.render(f'Score: {self.score}/{WINNING_SCORE} ', True, (0,0,0))
        screen.blit(self.image, self.rect)
        screen.blit(score_text, (10, 10))


trash_image = pygame.image.load("trash.png").convert_alpha()
class Trash:
    def __init__(self):
        # Load the collectible Trash image
        self.image = trash_image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() / 3), int(self.image.get_height() / 3)))
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
    def reset(self):
        
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = 50
    def drop(self, time):
        if time < 5000:
            ready_for_next_Trash = False
            # Apply gravity to the Trash's velocity
            self.velocity[1] += GRAVITY / 50

            # Update the Trash's position based on its velocity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

            # Constrain the Trash's position to the screen boundaries
            # if self.rect.left < 0:
            #     self.rect.left = 0
            #     self.velocity[0] = Trash_MOVE_SPEED
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                self.velocity[0] = -TRASH_MOVE_SPEED
            if self.rect.bottom > GROUND:
                self.rect.bottom = GROUND
                self.velocity[1] = 0
        else:
            self.remove()
            trash.reset()
    def draw(self, screen):
        # Draw the Trash on the screen
        screen.blit(self.image, self.rect)
    def remove(self):
        self.rect.x = -100
# Create a Pygame surface to draw on
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Load the octopus image and create a Octopus object
octopus = Octopus(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 15, "octopus_right.png")
# Start the Pygame game loop
clock = pygame.time.Clock()
#pygame.display.toggle_fullscreen()
announcement = announcement_font.render(f'You won', True, (0, 0, 0))

run = True
keypress = True
#create a Trash
trash = Trash()
last_Trash_time = 0
Trash_time = 0
start_time = 0
count_time = False
game_start_moment = 0
duration1 = 0
duration2 = 0
end_intro1 = 0
end_intro2 = 0
end_intro1_state = False
end_intro2_state = False
playing_music = False

while run:
    # Checking every event happening in the game
    for event in pygame.event.get():
        #check if the closing button was pressed
        if event.type == pygame.QUIT:
            #if so, end the game
            pygame.quit()
            sys.exit()
    if end_intro1_state == False:
        screen.blit(intro1, (intro1_x, intro1_y))
        end_intro1 = pygame.time.get_ticks()
        duration1 = end_intro1 - start_time
        if duration1 >= (3000+1000*intro1_sound.get_length()):
            end_intro1_state = True
            intro1_sound.stop() # stop the sound when intro 1 is finished

        else:
            intro1_sound.play() # play the sound while intro 1 is displayed
    elif end_intro2_state == False:
        screen.blit(intro2, (intro2_x, intro2_y))
        end_intro2 = pygame.time.get_ticks()
        duration2 = end_intro2 - end_intro1
        if duration2 >= (1000*intro2_sound.get_length()):
            
            end_intro2_state = True
            intro2_sound.stop() # stop the sound when intro 1 is finished

        else:
            intro2_sound.play() # play the sound while intro 1 is displayed
    else:
        
    
        if not playing_music:
            music.play()
            playing_music = True
        #add background into the while loop so it always stay in the screen
        screen.blit(background, (0, 0))
        if not count_time and start_time == 0:
            start_time = pygame.time.get_ticks()
            count_time = True
        # Get the current state of the arrow keys
        if keypress:
            keys = pygame.key.get_pressed()
        
        # Update the octopus's position and velocity
        octopus.update(keys)
        # Draw the ocotpus on the screen
        octopus.draw(screen)
        #only drop Trash after 10 seconds
        new_trash_time = pygame.time.get_ticks()
        trash_time = new_trash_time - last_Trash_time
        #print("Trash time: " + str(Trash_time))
        #print("New Trash time: " + str(new_Trash_time))
        trash.drop(trash_time)
        
        last_Trash_time = new_trash_time
        if keypress:
            trash.draw(screen)
        #Check if the octopus catches the Trash
        if octopus.rect.colliderect(trash):
            octopus.collect_trash()
            trash.remove()
            trash.reset()
        if trash.rect.bottom == GROUND:
            trash.remove()
            trash.reset()
            
            
        if octopus.score == WINNING_SCORE:
            
            GAME_IN_PROGRESS = False
            
        if not GAME_IN_PROGRESS:
            count_time = False
            keypress = False
            end_time = pygame.time.get_ticks()
            if TOTAL_TIME == 0:
                TOTAL_TIME = (end_time - start_time - duration2 -duration1) / 1000
            screen.blit(announcement, (SCREEN_WIDTH / 2 - announcement.get_width() / 2, SCREEN_HEIGHT / 2 - announcement.get_height() / 2))
            time_display = announcement_font.render(f'Total time: {TOTAL_TIME} seconds', True, (0,0,0))
            time_display_rect = time_display.get_rect()

            # position the time display surface beneath the announcement in the middle of the screen
            time_display_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + announcement.get_height() / 2 + 20)

            # blit the time display surface to the screen
            screen.blit(time_display, time_display_rect)    # Update the display and limit the frame rate to 60 FPS
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()