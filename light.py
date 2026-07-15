import pygame


class Light:
    def __init__(self, x, y, color, label, radius=18):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.radius = radius
        self.detected = False

    def position(self):
        return self.x, self.y

    def contains(self, mouse_position):
        mouse_x, mouse_y = mouse_position

        dx = mouse_x - self.x
        dy = mouse_y - self.y

        return dx * dx + dy * dy <= self.radius * self.radius

    def move(self, position):
        self.x, self.y = position

    def draw(self, surface, font):
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            self.radius,
        )

        pygame.draw.circle(
            surface,
            (20, 25, 35),
            (int(self.x), int(self.y)),
            self.radius,
            2,
        )

        label_surface = font.render(
            self.label,
            True,
            (20, 25, 35),
        )

        label_rect = label_surface.get_rect(
            center=(int(self.x), int(self.y))
        )

        surface.blit(label_surface, label_rect)