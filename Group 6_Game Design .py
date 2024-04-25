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
LOCK_RANGE = 100 # Lock Range for player to lock professors
num_bluebooks = 10
player_stamina_flag = 0
bluebooks_collected = 0

# Initialize a variable for the skill animation radius and cast_flag for player animation
draw_skill_animation_flag = 0
skill_animation_radius = 0
cast_flag = 0

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

# Define the new size for the character images
new_size = (32, 32)  # Change this size as needed

# Load and scale the images
Character_Tileset_Idle1 = pygame.transform.scale(pygame.image.load('Assets/Player/Idle1.png'), new_size)
Character_Tileset_Idle2 = pygame.transform.scale(pygame.image.load('Assets/Player/Idle2.png'), new_size)
Character_Tileset_Idle3 = pygame.transform.scale(pygame.image.load('Assets/Player/Idle3.png'), new_size)
Character_Tileset_Idle4 = pygame.transform.scale(pygame.image.load('Assets/Player/Idle4.png'), new_size)

Character_Tileset_Left1 = pygame.transform.scale(pygame.image.load('Assets/Player/Left1.png'), new_size)
Character_Tileset_Left2 = pygame.transform.scale(pygame.image.load('Assets/Player/Left2.png'), new_size)
Character_Tileset_Left3 = pygame.transform.scale(pygame.image.load('Assets/Player/Left3.png'), new_size)
Character_Tileset_Left4 = pygame.transform.scale(pygame.image.load('Assets/Player/Left4.png'), new_size)

Character_Tileset_Right1 = pygame.transform.scale(pygame.image.load('Assets/Player/Right1.png'), new_size)
Character_Tileset_Right2 = pygame.transform.scale(pygame.image.load('Assets/Player/Right2.png'), new_size)
Character_Tileset_Right3 = pygame.transform.scale(pygame.image.load('Assets/Player/Right3.png'), new_size)
Character_Tileset_Right4 = pygame.transform.scale(pygame.image.load('Assets/Player/Right4.png'), new_size)

Character_Tileset_Up1 = pygame.transform.scale(pygame.image.load('Assets/Player/Up1.png'), new_size)
Character_Tileset_Up2 = pygame.transform.scale(pygame.image.load('Assets/Player/Up2.png'), new_size)
Character_Tileset_Up3 = pygame.transform.scale(pygame.image.load('Assets/Player/Up3.png'), new_size)
Character_Tileset_Up4 = pygame.transform.scale(pygame.image.load('Assets/Player/Up4.png'), new_size)

Character_Tileset_Down1 = pygame.transform.scale(pygame.image.load('Assets/Player/Down1.png'), new_size)
Character_Tileset_Down2 = pygame.transform.scale(pygame.image.load('Assets/Player/Down2.png'), new_size)
Character_Tileset_Down3 = pygame.transform.scale(pygame.image.load('Assets/Player/Down3.png'), new_size)
Character_Tileset_Down4 = pygame.transform.scale(pygame.image.load('Assets/Player/Down4.png'), new_size)


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
        self.paused = False
        self.pause_cooldown = 0
    
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
        self.locked = False  # Initialize locked state as False

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
        self.player_state = 'Idle'  # Initialize player's state
        self.player_frame = 0  # Initialize player's frame
    
    def draw(self, screen):
        global num_bluebooks
        
        # Call the Player_Animation function to animate the player
        Player_Animation(screen, self.player_state, self.player_frame)

        # Draw health, bluebook collection, and stamina
        font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 28)
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
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, 50, 10))

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
        font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 36)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)

    def clicked(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height

def initialize_game(difficulty):
    global obstacles, bluebooks, professors, exit_box, num_bluebooks, DAMAGE

    # Initialize obstacles
    obstacles = [
        Obstacle(x, y, width, height) for x, y, width, height in [
        # Top right bookshelf to lower bookshelf obstacles
        (x, y, 20, 20) for x in range(570, 750, 20) for y in range(50, 450, 50)] +
        # Middle horizontal table
        [(x, 225, 20, 20) for x in range(200, 460, 20)] +
        # Entrance Counter
        [(600, y, 20, 20) for y in range(500, 550, 20)] +
        # Periodicals table near exit
        [(x, 480, 20, 20) for x in range(630, 750, 20)] +
        # Top middle shelf
        [(x, 50, 20, 20) for x in range(200, 500, 20)] +
        # Circular tables in bottom middle
        [(x, 350, 35, 35) for x in range(150, 500, 80)] +
        # Circular tables in the free area between the middle computer section and the middle top shelf
        [(x, 125, 35, 35) for x in range(150, 500, 80)] +
        # Tables at the most bottom
        [(x, 500, 50, 50) for x in range(175, 570, 135)] +
        # Library counter on the leftmost middle
        [(50, y, 20, 20) for y in range(150, 500, 20)]
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
        if not any(obstacle.x - 10 < x < obstacle.x + obstacle.width + 10 and obstacle.y - 10 < y < obstacle.y + obstacle.height + 10 for obstacle in obstacles) and \
        not any(math.hypot(bluebook.x - x, bluebook.y - y) < 30 for bluebook in bluebooks) and \
        50 < x < WIDTH - 50 and 50 < y < HEIGHT - 50:
            bluebooks.append(Bluebook(x, y))
            bluebook_count -= 1

    num_professors = 3  # Default number of professors

    if difficulty == "easy":
        num_professors = 3
        DAMAGE = 1
    elif difficulty == "medium":
        num_professors = 4
        DAMAGE = 2
    elif difficulty == "hard":
        num_professors = 5
        DAMAGE = 3

    professors = []
    for _ in range(num_professors):
        x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        while any(obstacle.x - 2 < x < obstacle.x + obstacle.width + 2 and obstacle.y - 2 < y < obstacle.y + obstacle.height + 2 for obstacle in obstacles) or not (50 < x < WIDTH - 50 and 50 < y < HEIGHT - 50):
            x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        professors.append(Professor(x, y))

    # Initialize exit box
    exit_box = Exit(100, HEIGHT - 25)  # Place exit in lower left corner
    countdown()  # Call the countdown function

buttons = []

# First, let's load a fancy font. You can replace 'FancyFont.ttf' with the path to your font file.
fancy_font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 48)

def draw_menu():
    screen.fill(WHITE)
    
    # Use the fancy font for the title
    title_text = fancy_font.render("Bluebook Collector", True, BLUE)
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

def draw_guide():
    screen.fill(WHITE)
    
    # Use the fancy font for the guide title
    guide_title = fancy_font.render("Guide", True, DARK_RED)
    screen.blit(guide_title, (WIDTH // 2 - guide_title.get_width() // 2, 40))
    
    # Use a smaller font for the guide text
    guide_font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 18)
    guide_text = (
        "You are an Isko/Iska in UP Cebu! As Hell Week approaches, you need to procure bluebooks,\n"
        "but the canteen has run out! You need to find bluebooks in the University Library. But be careful!\n"
        "There are 'Smiling Singko' Professors ready to fail you and prevent you from taking the exam.\n"
        "Dodge them, and get the bluebooks you need to pass the semester!\n\n"
        "Use the mouse pointer for movement, SPACE to pause, left-click to dash, and right-click to use\n'Wala ko'y ligo' "
        "Force Field\nto immobilize the professors around you. Use it wisely though, it will use up all your stamina.\n"
        "Hint: Professors speed up SIGNIFICANTLY when you have all the bluebooks and are heading for the exit.\n\n"
        "Padayon Isko/Iska!\n"
        "The game will start anytime soon..."
    )
    
    # Split the guide text into lines
    guide_lines = guide_text.split('\n')
    
    # Render and blit each line separately
    for i, line in enumerate(guide_lines):
        line_surface = guide_font.render(line, True, BLACK)
        screen.blit(line_surface, (WIDTH // 2 - line_surface.get_width() // 2, 100 + i * 30))

    # Display a false loading screen after the guide
    loading_font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 36)
    loading_text = loading_font.render("Loading...", True, BLUE)
    screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT - 90))

    # Display a loading bar
    loading_bar_width = 300
    loading_bar_height = 20
    pygame.draw.rect(screen, RED, pygame.Rect(WIDTH // 2 - loading_bar_width // 2, HEIGHT - 60, loading_bar_width, loading_bar_height), 2)

    pygame.display.flip()

    # Update the loading bar over 10 seconds
    for i in range(100):
        pygame.draw.rect(screen, RED, pygame.Rect(WIDTH // 2 - loading_bar_width // 2, HEIGHT - 60, i * (loading_bar_width // 100), loading_bar_height))
        pygame.display.flip()
        pygame.time.wait(10)  # Pauses


def Player_Animation(screen, player_state, player_frame):
    # Define the tilesets for each player state
    Character_Tilesets = {
        "Idle": [Character_Tileset_Idle1, Character_Tileset_Idle2, Character_Tileset_Idle3, Character_Tileset_Idle4],
        "Left": [Character_Tileset_Left1, Character_Tileset_Left2, Character_Tileset_Left3, Character_Tileset_Left4],
        "Right": [Character_Tileset_Right1, Character_Tileset_Right2, Character_Tileset_Right3, Character_Tileset_Right4],
        "Up": [Character_Tileset_Up1, Character_Tileset_Up2, Character_Tileset_Up3, Character_Tileset_Up4],
        "Down": [Character_Tileset_Down1, Character_Tileset_Down2, Character_Tileset_Down3, Character_Tileset_Down4]
    }

    # Get the current tileset for the player's state
    current_tileset = Character_Tilesets[player_state]

    # Calculate the position to center the image
    pos_x = player.x - current_tileset[player_frame].get_width() // 2
    pos_y = player.y - current_tileset[player_frame].get_height() // 2

    # Draw the current frame of the player's animation
    screen.blit(current_tileset[player_frame], (pos_x, pos_y))

def draw_game():
    global num_bluebooks, draw_skill_animation_flag, skill_animation_radius
    screen.fill(WHITE)
    for obstacle in obstacles:
        obstacle.draw(screen)
    for bluebook in bluebooks:
        bluebook.draw(screen)
    for professor in professors:
        if math.hypot(player.x - professor.x, player.y - professor.y) <= PROFESSOR_ALERT_DISTANCE:
            professor.color = RED
        else:
            professor.color = DARK_RED
        professor.draw(screen)
    
    player.draw(screen)

    if player.paused:
            # Draw an opaque overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(TRANSPARENT_BLACK)  # Semi-transparent black
            screen.blit(overlay, (0, 0))

            # Draw the word "PAUSE"
            font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 72)  # Use the Pixeboy font
            text = font.render('PAUSE', True, (255, 255, 255))  # White text
            screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))

    if draw_skill_animation_flag == 1 and skill_animation_radius < LOCK_RANGE - 15:    
        pygame.draw.circle(screen, GREEN, (int(player.x), int(player.y)), skill_animation_radius, 2)
    else:
        skill_animation_radius = 0
    
    if player.bluebooks_collected >= num_bluebooks:
        exit_box.color = GREEN
    else:
        exit_box.color = LIGHT_PURPLE
    exit_box.draw(screen)
    
    pygame.display.flip()

def update_player_movement():
    global PLAYER_SPEED
    global player_stamina_flag, keys
    global lock_index, cast_flag, cast_index, skill_animation_radius, draw_skill_animation_flag
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and player.pause_cooldown == 0:
        player.paused = not player.paused
        player.pause_cooldown = 10 # Set as needed
    # Update the cooldown timer
    if player.pause_cooldown > 0:
        player.pause_cooldown -= 1
    if player.paused == False:
        if pygame.mouse.get_pressed()[2] and player.player_stamina == MAX_STAMINA:
            cast_flag = 1
            cast_index = 12
            # Right mouse click
            player.player_stamina = 0  # Reset stamina
            player_stamina_flag = 1  # Prevent further stamina use for a brief period

            # Lock professors in the area
            for professor in professors:
                if math.hypot(player.x - professor.x, player.y - professor.y) <= LOCK_RANGE:
                    professor.locked = True
                    lock_index = 100    # Time to lock the professors
        
        if cast_flag == 1:
            draw_skill_animation_flag = 1
            skill_animation_radius += 15
            if skill_animation_radius > LOCK_RANGE - 15:
                skill_animation_radius = 0  # Reset the radius when it reaches the lock range
                draw_skill_animation_flag = 0
            cast_index -= 1
            if cast_index == 0:
                cast_flag = 0
        
        else:
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
            
            # Update player's state and frame based on the movement direction
            if new_x > player.x:
                player.player_state = 'Right'
            elif new_x < player.x:
                player.player_state = 'Left'
            elif new_y > player.y:
                player.player_state = 'Down'
            elif new_y < player.y:
                player.player_state = 'Up'
            else:
                player.player_state = 'Idle'
            
            # Update player's frame for animation
            player.player_frame = (player.player_frame + 1) % 4  # Assuming there are 4 frames in each animation
            
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
    global lock_index, PROFESSOR_SPEED, num_bluebooks, speed

    if player.bluebooks_collected == num_bluebooks:
        PROFESSOR_SPEED = 5
    
    for professor in professors:
        if professor.locked:
            if lock_index == 0:
                professor.locked = False
            else:
                professor.x += random.uniform(-1, 1) * speed
                professor.y += random.uniform(-1, 1) * speed
                lock_index -= 1
        else:
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
    countdown_font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 100)
    player = Player(590, HEIGHT - 20)
    game_frozen = False
    won = False

# Difficulty Initialization
difficulty = None

# Countdown variables
countdown_timer = 3
countdown_font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 100)

def main_menu():
    global difficulty
    global player
    difficulty = None
    menu = True
    while menu:
        draw_menu()  # Draw the menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.clicked():
                        difficulty = button.action
                        draw_guide()  # Display the guide
                        menu = False

# Define a global variable to track whether the game is frozen
game_frozen = False
player = Player(590, HEIGHT - 20)

class EndGameScreen:
    def __init__(self, message):
        self.message = message
        self.return_button = Button("Return to Main Menu", 250, 350, 300, 50, LIGHT_PURPLE, PURPLE, "menu")
        self.exit_button = Button("Exit", 250, 425, 300, 50, LIGHT_PURPLE, PURPLE, "exit")

    def draw(self, screen):
        overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay_surface.fill(TRANSPARENT_BLACK)
        screen.blit(overlay_surface, (0, 0))

        font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 28)
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
                        main_game_loop()
                    elif self.exit_button.clicked():
                        pygame.quit()
                        sys.exit()

class VictoryScreen(EndGameScreen):
    def __init__(self):
        super().__init__("Congratulations! You made it past Hell Week! :D")

class GameOverScreen(EndGameScreen):
    def __init__(self):
        super().__init__("Game Over! You were caught by the professors.")

def countdown():
    countdown_timer = 3  # Set the countdown timer
    countdown_font = pygame.font.Font('Assets/Fonts/Pixeboy.ttf', 72)  # Set the countdown font

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

def main_game_loop():
    
    # Main game loop
    main_menu()

    # Difficulty Initialization
    initialize_game(difficulty)
    game_frozen = False
    
    while True:
        if not game_frozen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if player.paused:
                update_player_movement()
                draw_game()
            else:
                update_player_movement()
                check_bluebook_collision()
                check_professor_collision()
                check_exit_collision()
                update_professors_movement()
                draw_game()
                check_game_over()

            pygame.display.flip()  # Update the display after drawing the skill animation

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.time.Clock().tick(60)

# Call the main game loop function
main_game_loop()
