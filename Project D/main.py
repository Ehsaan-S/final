import pygame
import math
import random

screen_width = 600
screen_height = 600

class SpaceRocks:
    def __init__(self):
        self.init_pygame()
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        self.player_size = 20
        self.player_x = screen_width // 2
        self.player_y = screen_height // 2

        # Load and transform the player's original image
        self.player_img_original = pygame.image.load(r"C:\Users\Ehsaan\Documents\GitHub\Project-D\Project D\spaceship.gif")
        self.player_img_original = pygame.transform.scale(self.player_img_original, (50, 50))
        self.player_img = self.player_img_original
        self.player_angle = 0

        self.bullets = []
        self.bullet_size = 5
        self.bullet_speed = 5  # Increase for faster bullets

        self.background_img = pygame.image.load(r"C:\Users\Ehsaan\Documents\GitHub\Project-D\Project D\space backround.jpg")
        self.background_img = pygame.transform.scale(self.background_img, (screen_width, screen_height))

        self.asteroids = []
        self.asteroids_speed_x = 0.1
        self.asteroids_speed_y = 0.1

    def main_loop(self):
        while True:
            self.handle_input()
            self.process_game_logic()
            self.draw()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroids")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # If the left mouse button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                rad_angle = math.radians(self.player_angle)
                bullet_dx = math.cos(rad_angle) * self.bullet_speed
                bullet_dy = -math.sin(rad_angle) * self.bullet_speed

                # Append a new bullet with its starting coordinates and velocity
                self.bullets.append((self.player_x + 25, self.player_y + 25, bullet_dx, bullet_dy))

    def process_game_logic(self):
        # Update player angle to point towards the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.player_x + 25), mouse_y - (self.player_y + 25)
        self.player_angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        # Rotate the player's image based on the calculated angle
        self.player_img = pygame.transform.rotate(self.player_img_original, self.player_angle)

        # Update player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_x -= 0.2
        if keys[pygame.K_RIGHT]:
            self.player_x += 0.2
        if keys[pygame.K_DOWN]:
            self.player_y += 0.2
        if keys[pygame.K_UP]:
            self.player_y -= 0.2

        # Ensure the player stays within the screen bounds
        if self.player_x < 0:
            self.player_x = 0
        if self.player_x > screen_width - 50:
            self.player_x = screen_width - 50
        if self.player_y < 0:
            self.player_y = 0
        if self.player_y > screen_height - 50:
            self.player_y = screen_height - 50

        # Update the positions and speeds of asteroids
        if len(self.asteroids) < 10 and random.randint(0, 1000) < 1:
            asteroid_x = random.randint(0, screen_width)
            asteroid_y = random.randint(0, screen_height)
            self.asteroids.append((asteroid_x, asteroid_y, self.asteroids_speed_x, self.asteroids_speed_y))

        for i in range(len(self.asteroids)):
            x, y, speed_x, speed_y = self.asteroids[i]
            new_x = x + speed_x
            new_y = y + speed_y

            # Reverse horizontal speed if an edge is reached
            if new_x < 0 or new_x > screen_width:
                speed_x = -speed_x
            # Reverse vertical speed if an edge is reached
            if new_y < 0 or new_y > screen_height:
                speed_y = -speed_y

            self.asteroids[i] = (new_x, new_y, speed_x, speed_y)

        # Update the bullet positions based on their velocities
        self.bullets = [(x + dx, y + dy, dx, dy) for (x, y, dx, dy) in self.bullets if 0 < x < screen_width and 0 < y < screen_height]

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))
        # Adjust the player's image to its new rotated position
        rotated_rect = self.player_img.get_rect(center=(self.player_x + 25, self.player_y + 25))
        self.screen.blit(self.player_img, rotated_rect.topleft)

        # Draw each bullet
        for bullet in self.bullets:
            x, y = int(bullet[0]), int(bullet[1])
            pygame.draw.circle(self.screen, (255, 255, 0), (x, y), self.bullet_size)

        # Draw each asteroid
        for asteroid in self.asteroids:
            x, y = int(asteroid[0]), int(asteroid[1])
            pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 10)

        pygame.display.flip()

game = SpaceRocks()
game.main_loop()
