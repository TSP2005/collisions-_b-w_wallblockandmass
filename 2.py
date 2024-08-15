import sys
import pygame

screen_dim = [800, 600]


class block:
    def __init__(self, mass, loc, size, v):
        self.size = size
        self.mass = mass
        self.loc = loc
        self.v = v
        self.rect = pygame.Rect(self.loc[0], self.loc[1], self.size, self.size)

    def update_rect(self):
        self.rect = pygame.Rect(self.loc[0], self.loc[1], self.size, self.size)

    def collision_box(self, box):
        u1 = self.v
        u2 = box.v
        m1 = self.mass
        m2 = box.mass

        self.v = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)

    def collision_wall(self):
        self.v *= -1


class CollisionSim:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_dim)
        pygame.display.set_caption("collision simulator")
        self.clock = pygame.time.Clock()
        self.FPS = 2
        self.boxes = []
        self.wall = pygame.Rect(screen_dim[0] / 2 - 210, screen_dim[1] / 2 - 20, 10, 100)
        self.collision_count = 0
        # Initialize the font
        self.font = pygame.font.Font(None, 36)

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def render(self):
        for box in self.boxes:
            pygame.draw.rect(self.screen, (0, 0, 255), box.rect)
        pygame.draw.line(self.screen, (255, 255, 255), (0, screen_dim[1] / 2 + 81), (800, screen_dim[1] / 2 + 81))
        pygame.draw.rect(self.screen, (255, 255, 255), self.wall)

        # Render the collision count
        collision_text = self.font.render(f"Collisions: {self.collision_count}", True, (255, 255, 255))
        self.screen.blit(collision_text, (10, 10))

    def update(self):
        for box in self.boxes:
            self.check_collision(box)
            box.loc[0] += box.v
            box.update_rect()

    def check_collision(self, box):
        if box.rect.colliderect(self.wall):
            box.collision_wall()
            self.collision_count += 1
        for another_box in self.boxes:
            if another_box != box and box.rect.colliderect(another_box):
                box.collision_box(another_box)
                self.collision_count += 1


if __name__ == "__main__":
    box1 = block(100, [screen_dim[0] / 2, screen_dim[1] / 2], 80, -10)
    box2 = block(1, [screen_dim[0] / 2 - 100, screen_dim[1] / 2 + 50], 30, 0)
    sim = CollisionSim()
    sim.boxes = [box1, box2]
    sim.run()
