import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flocking Simulation")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Boid class
class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 4
        self.max_force = 0.1
        self.perception = 50

    def edges(self):
        if self.position.x > width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = width
        if self.position.y > height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = height

    def apply_force(self, force):
        self.acceleration += force

    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)

        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(separation)

    def align(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        avg_vector = pygame.Vector2(0, 0)
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < self.perception:
                avg_vector += boid.velocity
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = avg_vector.normalize() * self.max_speed
            steering = avg_vector - self.velocity
            steering = self.limit(steering, self.max_force)
        return steering

    def cohere(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        center_of_mass = pygame.Vector2(0, 0)
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < self.perception:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            vector_to_com = center_of_mass - self.position
            vector_to_com = vector_to_com.normalize() * self.max_speed
            steering = vector_to_com - self.velocity
            steering = self.limit(steering, self.max_force)
        return steering

    def separate(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        avg_vector = pygame.Vector2(0, 0)
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < self.perception / 2:
                diff = self.position - boid.position
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = avg_vector.normalize() * self.max_speed
            steering = avg_vector - self.velocity
            steering = self.limit(steering, self.max_force)
        return steering

    def limit(self, vector, max_value):
        if vector.length() > max_value:
            vector.scale_to_length(max_value)
        return vector

    def update(self):
        self.velocity += self.acceleration
        self.velocity = self.limit(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

    def show(self):
        pygame.draw.circle(screen, white, (int(self.position.x), int(self.position.y)), 3)

# Main function
def main():
    clock = pygame.time.Clock()
    boids = [Boid(random.randint(0, width), random.randint(0, height)) for _ in range(100)]

    running = True
    while running:
        clock.tick(30)
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for boid in boids:
            boid.edges()
            boid.flock(boids)
            boid.update()
            boid.show()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
