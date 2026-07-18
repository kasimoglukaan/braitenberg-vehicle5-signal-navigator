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
        integer=False,
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
        self.integer = integer
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

        new_value = (
            self.minimum
            + ratio
            * (
                self.maximum
                - self.minimum
            )
        )

        if self.integer:
            new_value = round(new_value)

        self.value = new_value

    def handle_event(self, event):
        knob_x = self.value_to_x()

        knob_rect = pygame.Rect(
            int(knob_x - 12),
            int(self.rect.centery - 12),
            24,
            24,
        )

        clickable_area = self.rect.inflate(
            0,
            24,
        )

        if (
            event.type
            == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if (
                knob_rect.collidepoint(event.pos)
                or clickable_area.collidepoint(
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
                self.rect.y - 29,
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

        knob_position = (
            int(self.value_to_x()),
            self.rect.centery,
        )

        pygame.draw.circle(
            surface,
            (235, 240, 250),
            knob_position,
            11,
        )

        pygame.draw.circle(
            surface,
            (15, 20, 30),
            knob_position,
            11,
            2,
        )


class ModeButton:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        mode,
    ):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height,
        )

        self.text = text
        self.mode = mode

    def clicked(self, event):
        return (
            event.type
            == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(
                event.pos
            )
        )

    def draw(
        self,
        surface,
        font,
        selected=False,
        danger=False,
    ):
        if danger:
            background = (110, 45, 58)
            text_color = (255, 225, 230)
            border_color = (210, 85, 105)

        elif selected:
            background = (0, 220, 180)
            text_color = (15, 20, 30)
            border_color = (0, 245, 200)

        else:
            background = (42, 50, 68)
            text_color = (220, 225, 235)
            border_color = (78, 90, 115)

        pygame.draw.rect(
            surface,
            background,
            self.rect,
            border_radius=8,
        )

        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            2,
            border_radius=8,
        )

        rendered_text = font.render(
            self.text,
            True,
            text_color,
        )

        text_rect = rendered_text.get_rect(
            center=self.rect.center
        )

        surface.blit(
            rendered_text,
            text_rect,
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

        self.title_font = pygame.font.SysFont(
            "consolas",
            22,
            bold=True,
        )

        self.normal_font = pygame.font.SysFont(
            "consolas",
            16,
            bold=True,
        )

        self.small_font = pygame.font.SysFont(
            "consolas",
            14,
        )

        self.tiny_font = pygame.font.SysFont(
            "consolas",
            12,
        )

        content_x = self.rect.x + 20
        content_width = self.rect.width - 40

        button_gap = 7

        button_width = (
            content_width
            - button_gap * 2
        ) // 3

        self.counter_button = ModeButton(
            content_x,
            425,
            button_width,
            42,
            "COUNTER",
            "counter",
        )

        self.memory_button = ModeButton(
            content_x
            + button_width
            + button_gap,
            425,
            button_width,
            42,
            "MEMORY",
            "memory",
        )

        self.signal_button = ModeButton(
            content_x
            + (
                button_width
                + button_gap
            ) * 2,
            425,
            button_width,
            42,
            "SIGNAL",
            "signal",
        )

        # Counter ve Signal Mode slider'ı
        self.threshold_slider = Slider(
            content_x,
            660,
            content_width,
            2,
            10,
            3,
            "Output threshold",
            integer=True,
        )

        # Memory Mode butonu
        self.reset_memory_button = ModeButton(
            content_x,
            650,
            content_width,
            38,
            "RESET LEARNED SEQUENCE",
            "reset_memory",
        )

        self.sensor_slider = Slider(
            content_x,
            755,
            content_width,
            5,
            85,
            30,
            "Sensor offset",
        )

        self.speed_slider = Slider(
            content_x,
            845,
            content_width,
            0.25,
            3.0,
            1.0,
            "Vehicle speed",
        )

    def handle_event(
        self,
        event,
        logic_network,
    ):
        if self.counter_button.clicked(event):
            logic_network.set_mode(
                logic_network.COUNTER_MODE
            )

        if self.memory_button.clicked(event):
            logic_network.set_mode(
                logic_network.MEMORY_MODE
            )

        if self.signal_button.clicked(event):
            logic_network.set_mode(
                logic_network.SIGNAL_MODE
            )

        if (
            logic_network.mode
            == logic_network.MEMORY_MODE
            and self.reset_memory_button.clicked(
                event
            )
        ):
            logic_network.reset_memory()

        if logic_network.mode in (
            logic_network.COUNTER_MODE,
            logic_network.SIGNAL_MODE,
        ):
            self.threshold_slider.handle_event(
                event
            )
        else:
            self.threshold_slider.dragging = False

        self.sensor_slider.handle_event(event)
        self.speed_slider.handle_event(event)

    def apply_settings(
        self,
        vehicle,
        logic_network,
    ):
        vehicle.set_sensor_angle(
            self.sensor_slider.value
        )

        vehicle.set_speed_multiplier(
            self.speed_slider.value
        )

        logic_network.set_counter_threshold(
            self.threshold_slider.value
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

    def draw_section_title(
        self,
        surface,
        text,
        x,
        y,
    ):
        self.draw_text(
            surface,
            text,
            (x, y),
            self.normal_font,
            (0, 220, 180),
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

        elif (
            logic_network.mode
            == logic_network.MEMORY_MODE
            and not logic_network.learning_complete
        ):
            state = "LEARNING"

        else:
            state = "RUNNING"

        general_lines = [
            f"State: {state}",
            (
                "Mode: "
                f"{logic_network.mode.upper()}"
            ),
            f"Sources: {len(lights)}",
            (
                "Last source: "
                f"{logic_network.last_detected_source}"
            ),
            (
                "Last action: "
                f"{logic_network.last_signal_action}"
            ),
            (
                "Logic outputs: "
                f"{logic_network.output_count}"
            ),
        ]

        for line in general_lines:
            self.draw_text(
                surface,
                line,
                (x, y),
                self.small_font,
                (220, 225, 235),
            )

            y += 22

        y += 12

        self.draw_section_title(
            surface,
            "SENSOR / MOTOR DATA",
            x,
            y,
        )

        y += 28

        sensor_lines = [
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

        for line in sensor_lines:
            self.draw_text(
                surface,
                line,
                (x, y),
                self.small_font,
                (205, 212, 225),
            )

            y += 21

        self.draw_section_title(
            surface,
            "LOGIC MODE",
            x,
            392,
        )

        self.counter_button.draw(
            surface,
            self.tiny_font,
            selected=(
                logic_network.mode
                == logic_network.COUNTER_MODE
            ),
        )

        self.memory_button.draw(
            surface,
            self.tiny_font,
            selected=(
                logic_network.mode
                == logic_network.MEMORY_MODE
            ),
        )

        self.signal_button.draw(
            surface,
            self.tiny_font,
            selected=(
                logic_network.mode
                == logic_network.SIGNAL_MODE
            ),
        )

        if (
            logic_network.mode
            == logic_network.MEMORY_MODE
        ):
            self.draw_memory_information(
                surface,
                logic_network,
                x,
            )

        elif (
            logic_network.mode
            == logic_network.SIGNAL_MODE
        ):
            self.draw_signal_information(
                surface,
                logic_network,
                x,
            )

        else:
            self.draw_counter_information(
                surface,
                vehicle,
                logic_network,
                x,
            )

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

    def draw_status_boxes(
        self,
        surface,
        statuses,
        x,
        y,
    ):
        status_x = x
        status_y = y

        for status in statuses:
            is_on = status == "ON"

            status_box = pygame.Rect(
                status_x,
                status_y,
                48,
                29,
            )

            if is_on:
                background = (25, 75, 67)
                border = (0, 220, 180)
                text_color = (0, 235, 185)

            else:
                background = (39, 46, 62)
                border = (73, 84, 106)
                text_color = (180, 188, 202)

            pygame.draw.rect(
                surface,
                background,
                status_box,
                border_radius=6,
            )

            pygame.draw.rect(
                surface,
                border,
                status_box,
                1,
                border_radius=6,
            )

            status_surface = (
                self.small_font.render(
                    status,
                    True,
                    text_color,
                )
            )

            surface.blit(
                status_surface,
                status_surface.get_rect(
                    center=status_box.center
                ),
            )

            status_x += 55

            if (
                status_x
                > self.rect.right - 60
            ):
                status_x = x
                status_y += 36

    def draw_counter_information(
        self,
        surface,
        vehicle,
        logic_network,
        x,
    ):
        self.draw_text(
            surface,
            "Threshold devices",
            (x, 495),
            self.small_font,
            (205, 212, 225),
        )

        statuses = (
            logic_network
            .counter_device_statuses(
                output_is_visible=(
                    vehicle.triggered
                )
            )
        )

        self.draw_status_boxes(
            surface,
            statuses,
            x,
            523,
        )

        self.threshold_slider.draw(
            surface,
            self.small_font,
            str(
                int(
                    self.threshold_slider.value
                )
            ),
        )

    def draw_memory_information(
        self,
        surface,
        logic_network,
        x,
    ):
        memory_state = (
            "RECOGNIZING"
            if logic_network.learning_complete
            else "LEARNING"
        )

        self.draw_text(
            surface,
            f"Memory state: {memory_state}",
            (x, 490),
            self.small_font,
            (205, 212, 225),
        )

        self.draw_text(
            surface,
            "Learned sequence",
            (x, 522),
            self.tiny_font,
            (150, 165, 190),
        )

        learned_box = pygame.Rect(
            x,
            542,
            self.rect.width - 40,
            38,
        )

        pygame.draw.rect(
            surface,
            (35, 43, 59),
            learned_box,
            border_radius=7,
        )

        self.draw_text(
            surface,
            logic_network
            .learned_sequence_text(),
            (x + 10, 552),
            self.small_font,
            (0, 220, 180),
        )

        self.draw_text(
            surface,
            "Current sequence",
            (x, 590),
            self.tiny_font,
            (150, 165, 190),
        )

        current_box = pygame.Rect(
            x,
            610,
            self.rect.width - 40,
            38,
        )

        pygame.draw.rect(
            surface,
            (35, 43, 59),
            current_box,
            border_radius=7,
        )

        self.draw_text(
            surface,
            logic_network
            .current_sequence_text(),
            (x + 10, 620),
            self.small_font,
            (255, 205, 90),
        )

        self.reset_memory_button.draw(
            surface,
            self.small_font,
            danger=True,
        )

    def draw_signal_information(
        self,
        surface,
        logic_network,
        x,
    ):
        self.draw_text(
            surface,
            (
                "Activation: "
                f"{logic_network.pulse_count}"
                f"/{logic_network.counter_threshold}"
            ),
            (x, 490),
            self.small_font,
            (235, 240, 250),
        )

        legend = [
            (
                "Yellow   +1 excitation",
                (255, 215, 70),
            ),
            (
                "Red      -1 inhibition",
                (255, 90, 105),
            ),
            (
                "Green    -2 inhibition",
                (80, 220, 150),
            ),
            (
                "Purple   +2 excitation",
                (170, 110, 255),
            ),
        ]

        legend_y = 525

        for text, color in legend:
            pygame.draw.circle(
                surface,
                color,
                (
                    x + 6,
                    legend_y + 7,
                ),
                6,
            )

            self.draw_text(
                surface,
                text,
                (
                    x + 20,
                    legend_y,
                ),
                self.tiny_font,
                (205, 212, 225),
            )

            legend_y += 23

        self.threshold_slider.draw(
            surface,
            self.small_font,
            str(
                int(
                    self.threshold_slider.value
                )
            ),
        )