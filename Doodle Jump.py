import pygame
import random
import time

pygame.init()

# Set up the screen
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Doodle Jump")

# Load images
background = pygame.image.load("background.png").convert()
doodle = pygame.image.load("doodle.png").convert_alpha()
platform_img = pygame.image.load("platform.png").convert_alpha()

# Set up game variables
score = 0
platform_width = platform_img.get_width()
platform_height = platform_img.get_height()
platform_list = []
for i in range(10):
    x = random.randrange(0, screen_width - platform_width)
    if i <= 3:
            y = random.randrange(screen_height - 100, screen_height - 10)
    else:
        y = random.randrange(300, screen_height - platform_height)
    platform_list.append(pygame.Rect(x, y, platform_width, platform_height))
    time.sleep(1)
doodle_rect = pygame.Rect(screen_width // 2, screen_height - doodle.get_height(), doodle.get_width(), doodle.get_height())
doodle_dy = 0
jumping = False


# Set up fonts
font = pygame.font.SysFont(None, 40)

# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                doodle_rect.x -= 20
            elif event.key == pygame.K_RIGHT:
                doodle_rect.x += 20

    # Gravity
    doodle_dy += 0.3
    doodle_rect.y += doodle_dy

    # Check if doodle falls off the screen
    if doodle_rect.top > screen_height:
        running = False

    # Check if doodle lands on a platform
    for platform in platform_list:
        if doodle_rect.colliderect(platform):
            if doodle_dy > 0:
                doodle_dy = -7
                jumping = True
                time.sleep(0.5)
            else:
                jumping = False
            doodle_rect.bottom = platform.top
            break

    # Check if doodle goes off the screen and reappears on the other side
    if doodle_rect.left > screen_width:
        doodle_rect.right = 0
    elif doodle_rect.right < 0:
        doodle_rect.left = screen_width

    # Scroll platforms down if the doodle is above the half of the screen
    if doodle_rect.top < screen_height / 2:
        for platform in platform_list:
            platform.y += abs(doodle_dy)
            if platform.top > screen_height:
                score += 10
                platform_list.remove(platform)
                x = random.randrange(0, screen_width - platform_width)
                y = random.randrange(0, screen_height - platform_height)
                platform_list.append(pygame.Rect(x, y, platform_width, platform_height))

    # Draw the screen
    screen.blit(background, (0, 0))
    for platform in platform_list:
        screen.blit(platform_img, platform)
    screen.blit(doodle, doodle_rect)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# Clean up
pygame.quit()
