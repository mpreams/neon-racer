import pygame
import random

# Game window
pygame.init()
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Racer")
clock = pygame.time.Clock()
FRAME_COUNT = 0
BG_COLOR = (20, 20, 30)
font = pygame.font.Font(None, 36)

# Init road properties
ROAD_COLOR_1, ROAD_COLOR_2 = (50, 50, 50), (77, 77, 77)
road_y1 = 0
road_y2 = -HEIGHT
ROAD_SPEED = 10
# Initialize player properties
player_x = WIDTH // 2
player_y = HEIGHT - 120
PLAYER_SPEED = 7
#Initialize obstacles
obstacles = []
OBSTACLE_COLOR = (255, 50, 50)
OBSTACLE_SPAWN_RATE = 30  # Frames between obstacle spawns
OBSTACLE_SPEED = 5
pickups = []
PICKUP_COLOR = (50, 255, 50)
PICKUP_SPAWN_RATE = 210  # Pickup spawn probability
PICKUP_SPEED = 4
score = 0

# Road movement
def update_road(y1, y2, speed):
    global score
    y1 += speed
    y2 += speed
    if y1 >= HEIGHT:  # Reset road position when it goes off screen
        y1 = -HEIGHT
        score += 1
    if y2 >= HEIGHT:
        y2 = -HEIGHT   
        score += 1 
    return y1, y2

# Player movement
def move_player(keys, x):
    if keys[pygame.K_LEFT] and x - 10 > WIDTH // 4:
        x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and x + 10 < WIDTH - (WIDTH // 4) - 30:  # 30 is the width of the player  
        x += PLAYER_SPEED
    return x

# Obstacles movement
def spawn_obstacle():
    x = random.randint((WIDTH // 4) + 10, WIDTH - (WIDTH // 4) - 40)  # Keep within road bounds
    y = -50  # Start above the screen
    speed = random.randint(OBSTACLE_SPEED, OBSTACLE_SPEED + 3)
    obstacles.append([x, y, speed])

def update_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle[1] += obstacle[2] + (obstacle[0] / 500) # Move down by speed
        # Remove off-screen obstacles
        if obstacle[1] > HEIGHT:
            obstacles.remove(obstacle)
    return obstacles

# Pickups movement
def spawn_pickup():
    x = random.randint(WIDTH // 4, WIDTH - (WIDTH // 4))  # Keep within road bounds
    y = -30  # Start above the screen
    pickups.append([x, y])
    return pickups

def update_pickups(pickups):
    for pickup in pickups:
        pickup[1] += (PICKUP_SPEED + random.randint(1, PICKUP_SPEED))  # Move down by speed
        # Remove off-screen pickups
        if pickup[1] > HEIGHT:
            pickups.remove(pickup)
    return pickups

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)
    clock.tick(60)    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False 

    keys = pygame.key.get_pressed()
    # Update player and road positions
    player_x = move_player(keys, player_x)
    road_y1, road_y2 = update_road(road_y1, road_y2, ROAD_SPEED)


    # Draw road and player
    pygame.draw.rect(screen, ROAD_COLOR_1, (WIDTH // 4, road_y1, WIDTH // 2, HEIGHT))
    pygame.draw.rect(screen, ROAD_COLOR_2, (WIDTH // 4, road_y2, WIDTH // 2, HEIGHT))
    player_rect = pygame.Rect(player_x, player_y, 30, 60)
    pygame.draw.rect(screen, (0, 255, 255), player_rect)

    # Spawn obstacles
    FRAME_COUNT += 1
    if FRAME_COUNT % OBSTACLE_SPAWN_RATE == 0:
        spawn_obstacle()
    if random.randint(1, PICKUP_SPAWN_RATE) == 1:
        spawn_pickup() 

    # Update and draw obstacles
    obstacles = update_obstacles(obstacles)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], 30, 45)
        if player_rect.colliderect(obstacle_rect):
            end_text = font.render(f"Game Over! Final Score: {score}", True, (255, 0, 0))
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
            running = False
            pygame.display.update()
            pygame.time.wait(2800)  # Wait for 2 seconds before quitting           
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle_rect)

    # Update and draw pickups
    pickups = update_pickups(pickups)
    for pickup in pickups:
        pickup_rect = pygame.Rect(pickup[0], pickup[1], 15, 15)
        if player_rect.colliderect(pickup_rect):
            pickups.remove(pickup)
            score += 7        
        pygame.draw.ellipse(screen, PICKUP_COLOR, (pickup[0], pickup[1], 15, 15)) 

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))      # Draw score at the top left corner   
    
pygame.quit()  # Quit the game        