import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20  # Size of each grid cell
PLAYER_SPEED = 5
PROFESSOR_SPEED = 3
PROFESSOR_ALERT_DISTANCE = 8 * GRID_SIZE  # Distance at which professor speeds up
EXIT_RANGE_ALLOWANCE = 10  # Adjust this value as needed
DAMAGE = 1
num_bluebooks = 10
player_stamina_flag = 0

# Constants for Stamina
MAX_STAMINA = MAX_HEALTH = 100
STAMINA_RECHARGE_RATE = 1  # Stamina points recharged per frame when not boosting
STAMINA_DEPLETION_RATE = 2  # Stamina points depleted per frame when boosting
STAMINA_BOOST_SPEED = 3 # Additional Player speed when sprint is activated

# Global variables for Stamina
player_stamina = MAX_STAMINA

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 235)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
NEON_GREEN = (57, 255, 20)
DARK_RED = (139, 0, 0)
LIGHT_PURPLE = (200, 162, 200)
TRANSPARENT_BLACK = (0, 0, 0, 128)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bluebook Collector")

# Constants for UI elements
UI_AREA_WIDTH = 200
UI_AREA_HEIGHT = 100
UI_AREA_MARGIN = 10

# Global variables for obstacles
obstacles = []
bluebooks = []
professors = []
exit_box = None
won = False  # Define won globally and initialize to False

class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
    def draw(self, screen):
        pass

class Obstacle(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, BLACK)
        self.width = width
        self.height = height
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

class Bluebook(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, BLUE)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

class Professor(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, DARK_RED)
    
    def move_towards_player(self, player_x, player_y):
        pass
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN)
        self.health = 100
        self.bluebooks_collected = 0
        self.player_stamina = MAX_STAMINA  # Initialize player's stamina
    
    def draw(self, screen):
        global num_bluebooks
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)
        
        # Draw health, bluebook collection, and stamina
        font = pygame.font.Font(None, 28)
        health_text = font.render(f"Health: {self.health}", True, RED)
        bluebook_text = font.render(f"Bluebooks: {self.bluebooks_collected}/{num_bluebooks}", True, BLUE)
        stamina_text = font.render(f"Stamina: {self.player_stamina}/{MAX_STAMINA}", True, LIGHT_BLUE)
        
        screen.blit(health_text, (10, 10))

        # Draw health bar
        pygame.draw.rect(screen, RED, pygame.Rect(10, 30, self.health, 10))
        pygame.draw.rect(screen, BLACK, pygame.Rect(10, 30, MAX_HEALTH, 10), 2)  # Outline for stamina bar

        screen.blit(bluebook_text, (10, 50))
        screen.blit(stamina_text, (10, 70))
        
        # Draw stamina bar
        pygame.draw.rect(screen, LIGHT_BLUE, pygame.Rect(10, 90, self.player_stamina, 10))
        pygame.draw.rect(screen, BLACK, pygame.Rect(10, 90, MAX_STAMINA, 10), 2)  # Outline for stamina bar

class Exit(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, LIGHT_PURPLE)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, 50, 50))

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)

    def clicked(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height

def initialize_game(difficulty):
    global obstacles, bluebooks, professors, exit_box, num_bluebooks

    # Initialize obstacles
    obstacles = [
        Obstacle(x, y, width, height) for x, y, width, height in [
            (x, 100, 20, 20) for x in range(50, 250, 20)] +
            [(x, 100, 20, 20) for x in range(400, 620, 20)] +
            [(x, 300, 20, 20) for x in range(400, 620, 20)] +
            [(x, 400, 20, 20) for x in range(400, 620, 20)] +
            [(600, y, 20, 20) for y in range(50, 250, 20)] +
            [(x, 100, 20, 20) for x in range(650, 850, 20)] +
            [(300, y, 20, 20) for y in range(250, 330, 20)] +
            [(x, 700, 20, 20) for x in range(650, 750, 20)]
    ]

    # Initialize bluebooks
    if difficulty == "easy":
        num_bluebooks = 10
    elif difficulty == "medium":
        num_bluebooks = 15
    elif difficulty == "hard":
        num_bluebooks = 20
    
    bluebooks = []
    bluebook_count = num_bluebooks

    # Keep adding bluebooks until the desired count is reached
    while bluebook_count > 0:
        x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        if not any(obstacle.x - 2 < x < obstacle.x + obstacle.width + 2 and obstacle.y - 2 < y < obstacle.y + obstacle.height + 2 for obstacle in obstacles) and 50 < x < WIDTH - 50 and 50 < y < HEIGHT - 50:
            bluebooks.append(Bluebook(x, y))
            bluebook_count -= 1

    num_professors = 3  # Default number of professors

    if difficulty == "easy":
        num_professors = 3
    elif difficulty == "medium":
        num_professors = 4
    elif difficulty == "hard":
        num_professors = 5

    professors = []
    for _ in range(num_professors):
        x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        while any(obstacle.x - 2 < x < obstacle.x + obstacle.width + 2 and obstacle.y - 2 < y < obstacle.y + obstacle.height + 2 for obstacle in obstacles) or not (50 < x < WIDTH - 50 and 50 < y < HEIGHT - 50):
            x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        professors.append(Professor(x, y))

    # Initialize exit box
    exit_box = Exit(10, HEIGHT - 60)  # Place exit in lower left corner

buttons = []

def draw_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 48)
    title_text = font.render("Bluebook Collector", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    
    global buttons
    buttons = []
    button_texts = ["Easy", "Medium", "Hard"]
    for i, text in enumerate(button_texts):
        x = WIDTH // 2 - 100
        y = 250 + i * 100
        button = Button(text, x, y, 200, 50, LIGHT_PURPLE, PURPLE, text.lower())
        buttons.append(button)
    
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

def draw_game():
    global num_bluebooks
    screen.fill(WHITE)
    for obstacle in obstacles:
        obstacle.draw(screen)
    for bluebook in bluebooks:
        too_close = False
        for other_bluebook in bluebooks:
            if bluebook != other_bluebook:
                distance = math.hypot(bluebook.x - other_bluebook.x, bluebook.y - other_bluebook.y)
                if distance < 30:  # Adjust the threshold as needed
                    too_close = True
                    break
        if not too_close:
            bluebook.draw(screen)
    for professor in professors:
        if math.hypot(player.x - professor.x, player.y - professor.y) <= PROFESSOR_ALERT_DISTANCE:
            professor.color = RED
        else:
            professor.color = DARK_RED
        professor.draw(screen)
    player.draw(screen)
    if player.bluebooks_collected >= num_bluebooks:
        exit_box.color = GREEN
    else:
        exit_box.color = LIGHT_PURPLE
    exit_box.draw(screen)
    
    pygame.display.flip()

def update_player_movement():
    global PLAYER_SPEED
    global player_stamina_flag
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle = math.atan2(mouse_y - player.y, mouse_x - player.x)
    
    # Check if left mouse button is pressed and there is sufficient stamina
    if pygame.mouse.get_pressed()[0] and player.player_stamina > 0 and player_stamina_flag == 0:
        new_speed = PLAYER_SPEED + STAMINA_BOOST_SPEED
        if player.player_stamina >= STAMINA_DEPLETION_RATE:
            player.player_stamina -= STAMINA_DEPLETION_RATE
        else:
            player.player_stamina = 0
            player_stamina_flag = 1
    else:
        new_speed = PLAYER_SPEED
        if player.player_stamina < MAX_STAMINA:
            player.player_stamina += STAMINA_RECHARGE_RATE
        if player.player_stamina == 100:
            player_stamina_flag = 0

    new_x = player.x + new_speed * math.cos(angle)
    new_y = player.y + new_speed * math.sin(angle)
    
    # Check for collision with obstacles
    for obstacle in obstacles:
        if obstacle.x - 10 < new_x < obstacle.x + obstacle.width + 10 and obstacle.y - 10 < new_y < obstacle.y + obstacle.height + 10:
            return
    
    # Check if the new position is within the game window boundaries
    if 20 <= new_x <= WIDTH - 20 and 20 <= new_y <= HEIGHT - 20:
        player.x = new_x
        player.y = new_y

def check_bluebook_collision():
    global bluebooks_collected
    for bluebook in bluebooks[:]:
        if math.hypot(player.x - bluebook.x, player.y - bluebook.y) < 15:
            bluebooks.remove(bluebook)
            player.bluebooks_collected += 1

def check_professor_collision():
    global health
    for professor in professors:
        if math.hypot(player.x - professor.x, player.y - professor.y) < 15:
            player.health -= DAMAGE

def check_exit_collision():
    global won
    global num_bluebooks
    if exit_box.x < player.x < exit_box.x + 50 and exit_box.y < player.y < exit_box.y + 50 and player.bluebooks_collected >= num_bluebooks:
        won = True

def check_game_over():
    if player.health <= 0:
        game_over_screen = GameOverScreen()
        game_over_screen.draw(screen)
        game_over_screen.handle_events()
    elif won:
        victory_screen = VictoryScreen()
        victory_screen.draw(screen)
        victory_screen.handle_events()

def calculate_path(prof_x, prof_y, target_x, target_y):
    grid_size = GRID_SIZE
    num_cols = WIDTH // grid_size
    num_rows = HEIGHT // grid_size
    grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    for obstacle in obstacles:
        obstacle_col_start = int(obstacle.x // grid_size)
        obstacle_row_start = int(obstacle.y // grid_size)
        obstacle_col_end = int((obstacle.x + obstacle.width) // grid_size)
        obstacle_row_end = int((obstacle.y + obstacle.height) // grid_size)

        for row in range(obstacle_row_start, obstacle_row_end):
            for col in range(obstacle_col_start, obstacle_col_end):
                if 0 <= row < num_rows and 0 <= col < num_cols:
                    grid[row][col] = 1

    start_node = (int(prof_x // grid_size), int(prof_y // grid_size))
    target_node = (int(target_x // grid_size), int(target_y // grid_size))

    def heuristic(node):
        return math.sqrt((node[0] - target_node[0]) ** 2 + (node[1] - target_node[1]) ** 2)

    open_set = [start_node]
    came_from = {}
    g_score = {start_node: 0}
    f_score = {start_node: heuristic(start_node)}

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])

        if current == target_node:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return [(x * grid_size, y * grid_size) for x, y in path]

        open_set.remove(current)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < num_cols and
                    0 <= neighbor[1] < num_rows and
                    grid[neighbor[1]][neighbor[0]] == 0):

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor)

                    if neighbor not in open_set:
                        open_set.append(neighbor)

    return []

def update_professors_movement():
    for professor in professors:
        # Calculate path to player
        path = calculate_path(professor.x, professor.y, player.x, player.y)
        
        # Check for collision avoidance with other professors
        for other_professor in professors:
            if other_professor != professor:
                # Calculate distance between professors
                dist_between_professors = math.hypot(professor.x - other_professor.x, professor.y - other_professor.y)
                # If the distance is less than a threshold, move away from the other professor
                if dist_between_professors < 30:
                    dx = professor.x - other_professor.x
                    dy = professor.y - other_professor.y
                    dist = math.hypot(dx, dy)
                    # Move away from the other professor, avoiding division by zero
                    if dist != 0:
                        professor.x += dx / dist * PROFESSOR_SPEED
                        professor.y += dy / dist * PROFESSOR_SPEED
                    else:
                        # Handle division by zero error by forcibly splitting professors
                        # Move the current professor
                        professor.x += dx * PROFESSOR_SPEED
                        professor.y += dy * PROFESSOR_SPEED
                        # Move the other professor
                        other_professor.x -= dx * PROFESSOR_SPEED
                        other_professor.y -= dy * PROFESSOR_SPEED

        # Set initial speed
        speed = PROFESSOR_SPEED

        # Check if player is within alert range
        if math.hypot(player.x - professor.x, player.y - professor.y) <= PROFESSOR_ALERT_DISTANCE:
            speed += 1  # Increase speed by 1

        if path:
            next_x, next_y = path[0]
            dx = next_x - professor.x
            dy = next_y - professor.y
            dist = math.hypot(dx, dy)
            if dist <= speed:
                professor.x, professor.y = next_x, next_y
            else:
                # Avoid division by zero when dist is zero
                if dist != 0:
                    professor.x += dx / dist * speed
                    professor.y += dy / dist * speed
                else:
                    # Handle division by zero error (optional)
                    pass
        else:
            # No valid path found, do something else (e.g., random movement)
            professor.x += random.uniform(-1, 1) * speed
            professor.y += random.uniform(-1, 1) * speed

def reset_game_stats():
    global menu, countdown_timer, countdown_font, player, game_frozen, won
    global obstacles, bluebooks, professors
    global WIDTH, HEIGHT, GRID_SIZE, PLAYER_SPEED, PROFESSOR_SPEED, PROFESSOR_ALERT_DISTANCE, EXIT_RANGE_ALLOWANCE, DAMAGE, num_bluebooks

    WIDTH, HEIGHT = 800, 600
    GRID_SIZE = 20  # Size of each grid cell
    PLAYER_SPEED = 5
    PROFESSOR_SPEED = 3
    PROFESSOR_ALERT_DISTANCE = 8 * GRID_SIZE  # Distance at which professor speeds up
    EXIT_RANGE_ALLOWANCE = 10  # Adjust this value as needed
    DAMAGE = 1
    num_bluebooks = 10
    obstacles = []
    bluebooks = []
    professors = []
    menu = True
    countdown_timer = 3
    countdown_font = pygame.font.Font(None, 100)
    player = Player(750, HEIGHT - 60)
    game_frozen = False
    won = False

# Difficulty Initialization
difficulty = None

# Countdown variables
countdown_timer = 3
countdown_font = pygame.font.Font(None, 100)

def main_menu():
    global difficulty
    global player
    difficulty = None
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.clicked():
                        difficulty = button.action
                        menu = False
        
        draw_menu()

# Main game loop
main_menu()

initialize_game(difficulty)
player = Player(750, HEIGHT - 60)

# Define a global variable to track whether the game is frozen
game_frozen = False

class EndGameScreen:
    def __init__(self, message):
        self.message = message
        self.return_button = Button("Return to Main Menu", 250, 400, 300, 50, LIGHT_PURPLE, PURPLE, "menu")
        self.exit_button = Button("Exit", 250, 500, 300, 50, LIGHT_PURPLE, PURPLE, "exit")

    def draw(self, screen):
        overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay_surface.fill(TRANSPARENT_BLACK)
        screen.blit(overlay_surface, (0, 0))

        font = pygame.font.Font(None, 36)
        message_text = font.render(self.message, True, WHITE)
        text_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(message_text, text_rect)

        self.return_button.draw(screen)
        self.exit_button.draw(screen)

        pygame.display.flip()

    def handle_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.return_button.clicked():
                        # Handle return to main menu action
                        reset_game_stats()
                        main_menu()
                    elif self.exit_button.clicked():
                        pygame.quit()
                        sys.exit()

class VictoryScreen(EndGameScreen):
    def __init__(self):
        super().__init__("Congratulations! You made it past Hell Week! :D")

class GameOverScreen(EndGameScreen):
    def __init__(self):
        super().__init__("Game Over! You were caught by the professors.")

# Countdown loop
while countdown_timer > 0:
    # Draw the game display
    draw_game()

    # Create a surface for the countdown text
    countdown_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    countdown_surface.fill((0, 0, 0, 128))  # Semi-transparent black background
    countdown_text = countdown_font.render(str(countdown_timer), True, WHITE)
    countdown_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    countdown_surface.blit(countdown_text, countdown_rect)

    # Blit the countdown surface onto the screen
    screen.blit(countdown_surface, (0, 0))
    pygame.display.flip()
    
    pygame.time.wait(1000)  # Pause for 1 second
    countdown_timer -= 1

# In the main game loop
while True:
    if not game_frozen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        update_player_movement()
        check_bluebook_collision()
        check_professor_collision()
        check_exit_collision()
        update_professors_movement()
        draw_game()
        check_game_over()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle events for frozen state (e.g., return to main menu or exit)

    pygame.time.Clock().tick(60)

