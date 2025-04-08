import pygame
import random

class Asteroid:
    def __init__(self, x, y, use_verlet=False):
        self.position = pygame.Vector2(x, y)
        self.previous_position = pygame.Vector2(x, y)  # Needed for Verlet
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.use_verlet = use_verlet
        self.radius = 10

    def apply_force(self, force):
        self.acceleration += force

    def update(self, dt):
        if self.use_verlet:
            # Verlet Integration
            temp = self.position.copy()
            self.position += (self.position - self.previous_position) + self.acceleration * dt * dt
            self.previous_position = temp
        else:
            # Euler Integration
            self.velocity += self.acceleration * dt
            self.position += self.velocity * dt

        self.acceleration = pygame.Vector2(0, 0)  # Reset acceleration after update

    def draw(self, screen):
        pygame.draw.circle(screen, (200, 200, 200), self.position, self.radius)
        
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create some asteroids
asteroids = [Asteroid(random.randint(100, 700), random.randint(100, 500), use_verlet=False) for _ in range(5)]

running = True
while running:
    dt = clock.tick(60) / 100  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Optional: simulate gravitational pull to center
    center = pygame.Vector2(400, 300)
    for asteroid in asteroids:
        direction = (center - asteroid.position).normalize()
        asteroid.apply_force(direction * 5)  # tweak this force

        asteroid.update(dt)

    screen.fill((20, 20, 30))
    for asteroid in asteroids:
        asteroid.draw(screen)

    pygame.display.flip()

pygame.quit()
