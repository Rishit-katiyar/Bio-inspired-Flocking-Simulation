import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Advanced Flocking Simulation with Controls")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Boid class
class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = random.uniform(2, 4)
        self.max_force = 0.1
        self.perception = random.uniform(50, 100)
        self.energy = 100

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

    def flock(self, boids, obstacles, predators):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        avoidance = self.avoid_obstacles(obstacles)
        pred_avoidance = self.avoid_predators(predators)

        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(separation)
        self.apply_force(avoidance)
        self.apply_force(pred_avoidance)

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

    def avoid_obstacles(self, obstacles):
        steering = pygame.Vector2(0, 0)
        for obstacle in obstacles:
            distance = self.position.distance_to(obstacle)
            if distance < self.perception:
                diff = self.position - obstacle
                diff /= distance
                steering += diff
        return steering

    def avoid_predators(self, predators):
        steering = pygame.Vector2(0, 0)
        for predator in predators:
            distance = self.position.distance_to(predator.position)
            if distance < self.perception * 2:
                diff = self.position - predator.position
                diff /= distance
                steering += diff * 5  # Stronger avoidance force
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
        self.energy -= 0.1  # Decrease energy over time

    def show(self):
        color = blue if self.energy > 50 else white
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), 3)

# Predator class
class Predator:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 5
        self.max_force = 0.3
        self.hunger = 100

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

    def chase(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        avg_vector = pygame.Vector2(0, 0)
        for boid in boids:
            avg_vector += boid.position
            total += 1
        if total > 0:
            avg_vector /= total
            vector_to_boids = avg_vector - self.position
            vector_to_boids = vector_to_boids.normalize() * self.max_speed
            steering = vector_to_boids - self.velocity
            steering = self.limit(steering, self.max_force)
        self.apply_force(steering)

    def limit(self, vector, max_value):
        if vector.length() > max_value:
            vector.scale_to_length(max_value)
        return vector

    def update(self):
        self.velocity += self.acceleration
        self.velocity = self.limit(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0
        self.hunger -= 0.1  # Decrease hunger over time

    def eat(self, boids):
        for boid in boids:
            if self.position.distance_to(boid.position) < 10:
                boids.remove(boid)
                self.hunger = min(100, self.hunger + 20)  # Restore hunger

    def show(self):
        color = red if self.hunger > 50 else (255, 165, 0)  # Change color if hungry
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), 8)

# Main function
def main():
    clock = pygame.time.Clock()
    boids = [Boid(random.randint(0, width), random.randint(0, height)) for _ in range(100)]
    obstacles = []
    predators = []

    selected_element = None
    running = True
    while running:
        clock.tick(30)
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(event.pos)
                for boid in boids:
                    if boid.position.distance_to(mouse_pos) < 5:
                        selected_element = boid
                        break
                if not selected_element:
                    for obstacle in obstacles:
                        if obstacle.distance_to(mouse_pos) < 10:
                            selected_element = obstacle
                            break
                if not selected_element:
                    for predator in predators:
                        if predator.position.distance_to(mouse_pos) < 10:
                            selected_element = predator
                            break
            if event.type == pygame.MOUSEBUTTONUP:
                selected_element = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Spacebar to add boids
                    boids.append(Boid(random.randint(0, width), random.randint(0, height)))
                elif event.key == pygame.K_o:  # 'O' to add obstacles
                    obstacles.append(pygame.Vector2(random.randint(0, width), random.randint(0, height)))
                elif event.key == pygame.K_p:  # 'P' to add predators
                    predators.append(Predator(random.randint(0, width), random.randint(0, height)))

        if pygame.mouse.get_pressed()[0] and selected_element:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            if isinstance(selected_element, Boid) or isinstance(selected_element, Predator):
                selected_element.position = mouse_pos
            elif isinstance(selected_element, pygame.Vector2):
                selected_element.update(mouse_pos)

        for predator in predators:
            predator.edges()
            predator.chase(boids)
            predator.eat(boids)
            predator.update()
            predator.show()

        for boid in boids:
            boid.edges()
            boid.flock(boids, obstacles, predators)
            boid.update()
            boid.show()

        for obstacle in obstacles:
            pygame.draw.circle(screen, green, (int(obstacle.x), int(obstacle.y)), 10)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
