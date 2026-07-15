import pygame


class Slider:
    def __init__(
        self,
        x,
        y,
        width,
        minimum,
        maximum,
        value,
        label,
    ):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            8,
        )

        self.minimum = float(minimum)
        self.maximum = float(maximum)
        self.value = float(value)
        self.label = label

        self.dragging = False

    def value_to_x(self):
        ratio = (
            self.value - self.minimum
        ) / (
            self.maximum - self.minimum
        )

        return (
            self.rect.x
            + ratio * self.rect.width
        )

    def set_value_from_mouse(
        self,
        mouse_x,
    ):
        ratio = (
            mouse_x - self.rect.x
        ) / self.rect.width

        ratio = max(
            0.0,
            min(1.0, ratio),
        )

        self.value = (
            self.minimum
            + ratio
            * (
                self.maximum
                - self.minimum
            )
        )

    def handle_event(self, event):
        knob_x = self.value_to_x()

        knob_rect = pygame.Rect(
            int(knob_x - 12),
            int(self.rect.centery - 12),
            24,
            24,
        )

        if (
            event.type
            == pygame.MOUSEBUTTONDOWN
        ):
            if event.button == 1:
                if (
                    knob_rect.collidepoint(
                        event.pos
                    )
                    or self.rect.inflate(
                        0,
                        20,
                    ).collidepoint(
                        event.pos
                    )
                ):
                    self.dragging = True
                    self.set_value_from_mouse(
                        event.pos[0]
                    )

        elif (
            event.type
            == pygame.MOUSEBUTTONUP
        ):
            if event.button == 1:
                self.dragging = False

        elif (
            event.type
            == pygame.MOUSEMOTION
        ):
            if self.dragging:
                self.set_value_from_mouse(
                    event.pos[0]
                )

    def draw(
        self,
        surface,
        font,
        value_text,
    ):
        label_surface = font.render(
            f"{self.label}: {value_text}",
            True,
            (225, 230, 240),
        )

        surface.blit(
            label_surface,
            (
                self.rect.x,
                self.rect.y - 30,
            ),
        )

        pygame.draw.rect(
            surface,
            (62, 72, 92),
            self.rect,
            border_radius=4,
        )

        active_width = int(
            self.value_to_x()
            - self.rect.x
        )

        active_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            active_width,
            self.rect.height,
        )

        pygame.draw.rect(
            surface,
            (0, 220, 180),
            active_rect,
            border_radius=4,
        )

        pygame.draw.circle(
            surface,
            (235, 240, 250),
            (
                int(self.value_to_x()),
                self.rect.centery,
            ),
            11,
        )

        pygame.draw.circle(
            surface,
            (15, 20, 30),
            (
                int(self.value_to_x()),
                self.rect.centery,
            ),
            11,
            2,
        )


class Dashboard:
    def __init__(
        self,
        x,
        y,
        width,
        height,
    ):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height,
        )

        self.title_font = (
            pygame.font.SysFont(
                "consolas",
                22,
                bold=True,
            )
        )

        self.normal_font = (
            pygame.font.SysFont(
                "consolas",
                16,
            )
        )

        self.small_font = (
            pygame.font.SysFont(
                "consolas",
                14,
            )
        )

        slider_x = (
            self.rect.x + 25
        )

        slider_width = (
            self.rect.width - 50
        )

        self.sensor_slider = Slider(
            slider_x,
            520,
            slider_width,
            5,
            85,
            30,
            "Sensor offset",
        )

        self.speed_slider = Slider(
            slider_x,
            610,
            slider_width,
            0.25,
            3.0,
            1.0,
            "Vehicle speed",
        )

    def handle_event(self, event):
        self.sensor_slider.handle_event(
            event
        )

        self.speed_slider.handle_event(
            event
        )

    def apply_settings(self, vehicle):
        vehicle.set_sensor_angle(
            self.sensor_slider.value
        )

        vehicle.set_speed_multiplier(
            self.speed_slider.value
        )

    def draw_text(
        self,
        surface,
        text,
        position,
        font,
        color,
    ):
        rendered_text = font.render(
            text,
            True,
            color,
        )

        surface.blit(
            rendered_text,
            position,
        )

    def draw(
        self,
        surface,
        vehicle,
        logic_network,
        lights,
        paused,
    ):
        pygame.draw.rect(
            surface,
            (23, 28, 40),
            self.rect,
        )

        pygame.draw.line(
            surface,
            (65, 75, 95),
            (
                self.rect.left,
                self.rect.top,
            ),
            (
                self.rect.left,
                self.rect.bottom,
            ),
            2,
        )

        x = self.rect.x + 20
        y = self.rect.y + 20

        self.draw_text(
            surface,
            "VEHICLE 5",
            (x, y),
            self.title_font,
            (235, 240, 250),
        )

        y += 34

        self.draw_text(
            surface,
            "SIGNAL PATTERN NAVIGATOR",
            (x, y),
            self.normal_font,
            (0, 220, 180),
        )

        y += 42

        if paused:
            state = "PAUSED"
        elif vehicle.triggered:
            state = "LOGIC OUTPUT"
        else:
            state = "RUNNING"

        self.draw_text(
            surface,
            f"State: {state}",
            (x, y),
            self.normal_font,
            (235, 240, 250),
        )

        y += 28

        self.draw_text(
            surface,
            (
                "Pulse counter: "
                f"{logic_network.pulse_count}/3"
            ),
            (x, y),
            self.normal_font,
            (235, 240, 250),
        )

        y += 28

        self.draw_text(
            surface,
            f"Sources: {len(lights)}",
            (x, y),
            self.normal_font,
            (235, 240, 250),
        )

        y += 40

        self.draw_text(
            surface,
            "SENSOR AND MOTOR DATA",
            (x, y),
            self.normal_font,
            (0, 220, 180),
        )

        y += 29

        information_lines = [
            (
                "Left intensity:  "
                f"{vehicle.intensity_left:.2f}"
            ),
            (
                "Right intensity: "
                f"{vehicle.intensity_right:.2f}"
            ),
            (
                "Left motor:      "
                f"{vehicle.left_motor_speed:.2f}"
            ),
            (
                "Right motor:     "
                f"{vehicle.right_motor_speed:.2f}"
            ),
        ]

        for line in information_lines:
            self.draw_text(
                surface,
                line,
                (x, y),
                self.small_font,
                (210, 215, 225),
            )

            y += 23

        y += 22

        self.draw_text(
            surface,
            "THRESHOLD LOGIC",
            (x, y),
            self.normal_font,
            (0, 220, 180),
        )

        y += 29

        threshold_lines = [
            (
                "Input threshold:   "
                f"{logic_network.input_device.threshold}"
            ),
            (
                "Counter threshold: "
                f"{logic_network.counter_device.threshold}"
            ),
            (
                "Output threshold:  "
                f"{logic_network.output_device.threshold}"
            ),
        ]

        for line in threshold_lines:
            self.draw_text(
                surface,
                line,
                (x, y),
                self.small_font,
                (210, 215, 225),
            )

            y += 23

        # Sliderlar
        self.sensor_slider.draw(
            surface,
            self.small_font,
            (
                f"{self.sensor_slider.value:.0f}° "
                "each side"
            ),
        )

        self.speed_slider.draw(
            surface,
            self.small_font,
            (
                f"{self.speed_slider.value:.2f}x"
            ),
        )

        controls_y = 680

        self.draw_text(
            surface,
            "CONTROLS",
            (x, controls_y),
            self.normal_font,
            (0, 220, 180),
        )

        controls_y += 28

        control_lines = [
            "Left drag : move source",
            "Right click: add source",
            "Space: pause | R: reset",
        ]

        for line in control_lines:
            self.draw_text(
                surface,
                line,
                (x, controls_y),
                self.small_font,
                (175, 185, 202),
            )

            controls_y += 21