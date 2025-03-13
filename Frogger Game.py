import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game Vars
WIDTH = 1280
HEIGHT = 960
BLACK = (0, 0, 0)
frog_width = 64
frog_height = 64
car_width = 64
car_height = 64
road_img = pygame.image.load("road.jpg")
road_img = pygame.transform.scale(road_img, (1280,320))


# Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogger")

# Frog Class
class Frog:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("frog.jpg")
        self.img = pygame.transform.scale(self.img, (frog_width, frog_height))

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, frog_width, frog_height)

# Frog Instance
frog_x = (WIDTH - frog_width) // 2
frog_y = HEIGHT - frog_height
player = Frog(frog_x, frog_y)

# Car Class
class Car:
    def __init__(self, x, y, dx, img_path, width, height):
        self.x = x
        self.y = y
        self.dx = dx
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (width, height))
        self.width = width
        self.height = height

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.dx

    # Creates A Wrapping Around Effect
    def check_boundary(self):
        if self.dx > 0 and self.x > WIDTH:
            self.x = -self.width
        elif self.dx < 0 and self.x < -self.width:
            self.x = WIDTH

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Initialise Cars
def initialise_cars(y, dx, min_spacing, max_spacing, start_off_screen_left, img_path):
    cars = []
    x = -car_width if start_off_screen_left else WIDTH

    for i in range(0, 4):  # 4 cars
        cars.append(Car(x, y, dx, img_path, car_width, car_height))
        x += random.randint(min_spacing, max_spacing) * (-1 if start_off_screen_left else 1)

    return cars

right_cars = initialise_cars(832, 0.25, 250, 400, True, "Rcar.png")
left_cars = initialise_cars(704, -0.55, 250, 400, False, "Lcar.png")
right_cars2 = initialise_cars(576, 0.35, 250, 400, True, "Rcar2.png")

# Game Loop
running = True
start_time = time.time()
movement_enabled = False
while running:
    # Fill Screen
    screen.fill(BLACK)

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if time.time() - start_time >= 3:
                movement_enabled = True
            if movement_enabled:
                if event.key == pygame.K_RIGHT:  # Move Right
                    player.x += 64
                if event.key == pygame.K_LEFT:  # Move Left
                    player.x -= 64
                if event.key == pygame.K_UP:  # Move Up
                    player.y -= 64  # Decrease y To Move Up
                if event.key == pygame.K_DOWN:  # Move Down
                    player.y += 64  # Increase y To Move Down

    
    #Backgrounds
    screen.blit(road_img,(0,576))
    
    # Update & Draw Cars
    for car in right_cars:
        car.draw(screen)
        car.move()
        car.check_boundary()

        # Checking Collision
        if player.get_rect().colliderect(car.get_rect()):
            running = False

    for car in left_cars:
        car.draw(screen)
        car.move()
        car.check_boundary()

        # Checking Collision
        if player.get_rect().colliderect(car.get_rect()):
            running = False
    
    for car in right_cars2:
        car.draw(screen)
        car.move()
        car.check_boundary()

        # Checking Collision
        if player.get_rect().colliderect(car.get_rect()):
            running = False

    # Player Boundary Check & Draw
    player.x = max(0, min(player.x, WIDTH - frog_width))
    player.y = max(0, min(player.y, HEIGHT - frog_height))
    player.draw(screen)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
