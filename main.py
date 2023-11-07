import pygame
import math

pygame.init()

# Width and height of the window
WIDTH, HEIGHT = 800, 600
# window where we draw all the objects on pygame
# also called a surface
win = pygame.display.set_mode((WIDTH, HEIGHT))
# Window title
pygame.display.set_caption("Gavitational Slingshot effect")

# Mass for our objects
planet_mass = 100
space_rock = 5
# Set a gravitational constant
# Increase this amount for more G-force
G = 5
# Frames per second
# To speed this up just increase the amount
FPS = 60
# Planet radius
planet_size = 50
obj_size = 5
# Velocity scale
vel_scale = 100


# Load images
# transform.scale helps the image sizes/resolution 
bg = pygame.transform.scale(pygame.image.load("space_background.jpg"), (WIDTH, HEIGHT))
# image needs to be double the size of the radius because thats the diameterin x and y axis
planet = pygame.transform.scale(pygame.image.load("jupiter.png"), (planet_size * 2, planet_size * 2))

# Colours
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)


# Planet and G-force
class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        # Draw planet image at this position - should be in the middle
        win.blit(planet, (self.x - planet_size, self.y - planet_size))

# This will represent our metier/rock
# All the G-force logic and movment will be in thisclass
class Spacecraft:
    def __init__(self, x, y, x_vel, y_vel, mass):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass

    # Move method
    def move(self, planet=None):
        # Calculating the Gravitational Force
        # Calculate the distance between ourselves and the planet
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        # Force
        force = (G *self.mass * planet.mass) / distance ** 2
        # Acceleration
        acceleration = force / self.mass
        # Angle thata
        # In this order because this will give us the correct direction 
        angle = math.atan2(planet.y - self.y, planet.x - self.x)
        # Acceleration in both directions
        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        # Velocity for x direction and y direction
        self.x_vel += acceleration_x
        self.y_vel += acceleration_y
        # We take whatever our new velocity is and we are applying that to our x and to our y
        self.x += self.x_vel
        self.y += self.y_vel

    
    def draw(self):
        # Display in window, colour red, in position x and y, and object size
        # int just eliminates any floats that might occur
        pygame.draw.circle(win, red, (int(self.x), int(self.y)), obj_size)

def create_rock(location, mouse):
    temp_x, temp_y = location
    m_x, m_y = mouse
    # To calculate velocity from point to the select mouse click
    # Deivide by vel_scale to slow down the object
    # Makes it 100 times slower because its divided by 100(vel_scale)
    x_vel = (m_x - temp_x) / vel_scale
    y_vel = (m_y - temp_y) / vel_scale
    # objects starts at position temp_x and temp_y, moves x_veland y_vel and has the mass of the space_rock variable
    obj = Spacecraft(temp_x, temp_y, x_vel, y_vel, space_rock)
    return obj

# Function to display pygame window
def main():
    running = True

    # Implement a clock to regulate the below loop and make sure it doesnt run too fast based on my PC's CPU speed.
    # Regulates speed to be the same no matter the hardware we are running on
    clock = pygame.time.Clock()

    # Planet
    planet = Planet(WIDTH // 2, HEIGHT // 2, planet_mass)

    # Launching objects
    objects = []
    # Objects not yet launched
    temp_obj_pos = None

    while running:
        # Max is 60 FPS
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        # Loops through all the events that are occuring from pygame and check the events to see if they equal a specific one (like pressing a key or mouse click etc.)
        for event in pygame.event.get():
            # Exit while loop if we quit window
            if event.type == pygame.QUIT:
                running = False
            # Checks to see if mouse was clicked and stores that x/y axis location in temp_obj_pos list
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_rock(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        # Draw an image using blit()
        # Background must get drawn first so that its not displayed overothr objects
        win.blit(bg, (0, 0))
        # Temp_object exists then display
        if temp_obj_pos:
            # Displaying the line before circle prevents the line comming from middle of dot
            # Slingshot line
            # window, colour, where w clicked, and where we will click next, line thickness (2px)
            pygame.draw.line(win, white, temp_obj_pos, mouse_pos, 2)
            # display in window, colour red, in the temp position, object radius size
            # so this display a red dot where ever I click my mouse on screen
            pygame.draw.circle(win, red, temp_obj_pos, obj_size)

        # [:] makes a copy of this list so when the list is ammened it amends the copy and does effect the iteration of the original list
        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            # to remove objects once off the screen
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT

            # Planet collision
            # The distance between two points formula
            # Square route of the x coordinates plus the y coordinates is less than or equal to planet size
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= planet_size

            if off_screen or collided:
                objects.remove(obj)

        planet.draw()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()