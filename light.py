import pygame


class Light:
    SOURCE_TYPES = {
        "excitatory": {
            "color": (255, 215, 70),
            "short_name": "+1",
        },
        "inhibitory": {
            "color": (255, 90, 105),
            "short_name": "-1",
        },
        "strong_inhibitory": {
            "color": (80, 220, 150),
            "short_name": "-2",
        },
        "boost": {
            "color": (170, 110, 255),
            "short_name": "+2",
        },
    }

    def __init__(
        self,
        x,
        y,
        color=None,
        label="1",
        source_type="excitatory",
        radius=18,
    ):
        self.x = float(x)
        self.y = float(y)

        self.label = str(label)
        self.radius = radius
        self.detected = False

        if source_type not in self.SOURCE_TYPES:
            source_type = "excitatory"

        self.source_type = source_type

        if color is None:
            color = self.SOURCE_TYPES[
                self.source_type
            ]["color"]

        self.color = color

    def move(self, position):
        self.x = float(position[0])
        self.y = float(position[1])

    def contains(self, position):
        dx = position[0] - self.x
        dy = position[1] - self.y

        return (
            dx * dx + dy * dy
            <= (self.radius + 4) ** 2
        )

    def signal_value(self):
        if self.source_type == "excitatory":
            return 1

        if self.source_type == "inhibitory":
            return -1

        if self.source_type == "strong_inhibitory":
            return -2

        if self.source_type == "boost":
            return 2

        return 0

    def signal_text(self):
        return self.SOURCE_TYPES[
            self.source_type
        ]["short_name"]

    def draw(self, surface, font):
        center = (
            int(self.x),
            int(self.y),
        )

        pygame.draw.circle(
            surface,
            self.color,
            center,
            self.radius,
        )

        pygame.draw.circle(
            surface,
            (20, 25, 35),
            center,
            self.radius,
            2,
        )

        # Kaynak numarası
        label_surface = font.render(
            self.label,
            True,
            (20, 25, 35),
        )

        label_rect = label_surface.get_rect(
            center=center
        )

        surface.blit(
            label_surface,
            label_rect,
        )

        # Kaynak türü: +1, -1, -2 veya +2
        type_font = pygame.font.SysFont(
            "consolas",
            11,
            bold=True,
        )

        type_surface = type_font.render(
            self.signal_text(),
            True,
            (25, 30, 40),
        )

        type_rect = type_surface.get_rect(
            center=(
                int(self.x),
                int(
                    self.y
                    + self.radius
                    + 11
                ),
            )
        )

        surface.blit(
            type_surface,
            type_rect,
        )