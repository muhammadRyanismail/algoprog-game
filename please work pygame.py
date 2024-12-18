import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump King")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load assets
sprite_sheet = pygame.image.load("character_spritesheet.png").convert_alpha()
platform_texture = pygame.image.load("platform_texture.png").convert_alpha()
sky_background = pygame.image.load("sky_background.png").convert_alpha()
sky_background = pygame.transform.scale(sky_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Constants for platform dimensions
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 10
FLOOR_HEIGHT = 20
MAX_JUMP_POWER = -30  # The maximum upward force
JUMP_CHARGE_RATE = 0.5  # How fast the jump power increases when holding SPACE


# Floor Class
class Floor:
    def __init__(self):
        self.x = 0
        self.y = SCREEN_HEIGHT - FLOOR_HEIGHT
        self.width = SCREEN_WIDTH
        self.height = FLOOR_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, (139, 69, 19), (self.x, self.y, self.width, self.height))  # Brown floor color


# Player class
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - 20
        self.y = SCREEN_HEIGHT - 80  # Place player above the floor
        self.width = 40
        self.height = 40

        # Animation settings
        self.current_frame = 0
        self.animation_frames = []
        self.load_sprites()

        # Physics properties
        self.velocity_y = 1
        self.gravity = 0.3

        # Jumping mechanics
        self.is_charging_jump = False  # Whether the player is holding the jump button
        self.jump_power = 0  # Current jump power being charged

    def load_sprites(self):
        sprite_width = 32
        sprite_height = 32
        for i in range(3):
            frame = sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
            scaled_frame = pygame.transform.scale(frame, (self.width, self.height))
            self.animation_frames.append(scaled_frame)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 5
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += 5
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

    def handle_jump_input(self, keys):
        if keys[pygame.K_SPACE]:
            if not self.is_charging_jump:
                self.is_charging_jump = True  # Start charging the jump
                self.jump_power = 0  # Reset jump power

            if self.is_charging_jump:
                self.jump_power -= JUMP_CHARGE_RATE  # Increase jump power
                if self.jump_power < MAX_JUMP_POWER:  # Cap the jump power
                    self.jump_power = MAX_JUMP_POWER
        else:
            if self.is_charging_jump:
                self.jump()  # Perform the jump with the current jump power
                self.is_charging_jump = False  # Reset charging state

    def jump(self):
        self.velocity_y = self.jump_power  # Apply the charged jump power

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y

    def check_collision(self, platforms, floor):
        # Check collision with platforms
        for platform in platforms:
            if (
                self.x + self.width > platform.x
                and self.x < platform.x + platform.width
                and self.y + self.height <= platform.y
                and self.y + self.height + self.velocity_y >= platform.y
            ):
                self.y = platform.y - self.height  # Reset position on platform
                self.velocity_y = 0  # Stop downward movement
                return True

        # Check collision with floor
        if self.y + self.height >= floor.y:
            self.y = floor.y - self.height  # Reset position on the floor
            self.velocity_y = 0  # Stop downward movement
            return True

        return False

    def draw(self):
        current_sprite = self.animation_frames[self.current_frame]
        screen.blit(current_sprite, (self.x, self.y))


# Platform class
class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT

    def draw(self):
        platform_image = pygame.transform.scale(platform_texture, (self.width, self.height))
        screen.blit(platform_image, (self.x, self.y))

       
  
    


# Generate random platforms
def generate_platforms():
    platforms = []
    for i in range(6):
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        y = i * (SCREEN_HEIGHT // 6)
        platforms.append(Platform(x, y))
    return platforms


# Main game loop
def main():
    player = Player()
    platforms = generate_platforms()
    floor = Floor()

    score = 0
    running = True

    while running:
        screen.blit(sky_background, (0, 0))  # Draw background
        keys = pygame.key.get_pressed()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle jump input
        player.handle_jump_input(keys)

        # Movement and game logic
        player.move(keys)
        player.apply_gravity()
        if player.check_collision(platforms, floor):
            score += 1

        # Scroll platforms and player upwards
        if player.y < SCREEN_HEIGHT // 4:
            player.y += 5
            for platform in platforms:
                platform.y += 5
                if platform.y > SCREEN_HEIGHT:
                    platform.y = random.randint(-50, -10)  # Place above screen
                    platform.x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
                    score += 1

        # Check game over condition
        if player.y > SCREEN_HEIGHT:
            print(f"Game Over! Final Score: {score}")
            running = False

        # Draw game elements
        floor.draw()
        player.draw()
        for platform in platforms:
            platform.draw()

        # Display the score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

# Main game loop
def main():
    player = Player()
    platforms = generate_platforms()
    floor = Floor()

    score = 0
    running = True

    start_time = pygame.time.get_ticks()  # Record the time when the game starts
    floor_visible = True  # Track whether the floor is still visible

    while running:
        screen.blit(sky_background, (0, 0))  # Draw background
        keys = pygame.key.get_pressed()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check if 10 seconds have passed
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 10000:  # 10000 milliseconds = 10 seconds
            floor_visible = False  # Hide the floor after 10 seconds

        # Handle jump input
        player.handle_jump_input(keys)

        # Movement and game logic
        player.move(keys)
        player.apply_gravity()

        # Only check floor collision if the floor is visible
        if floor_visible and player.check_collision(platforms, floor):
            score += 1

        # Scroll platforms and player upwards
        if player.y < SCREEN_HEIGHT // 4:
            player.y += 5
            for platform in platforms:
                platform.y += 5
                if platform.y > SCREEN_HEIGHT:
                    platform.y = random.randint(-50, -10)  # Place above screen
                    platform.x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
                    score += 1

        # Check game over condition
        if player.y > SCREEN_HEIGHT:
            print(f"Game Over! Final Score: {score}")
            running = False

        # Draw game elements
        if floor_visible:  # Only draw the floor if it's still visible
            floor.draw()
        player.draw()
        for platform in platforms:
            platform.draw()

        # Display the score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

      
 