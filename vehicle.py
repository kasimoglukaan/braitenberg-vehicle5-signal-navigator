import math
import pygame


class Vehicle:
    def __init__(self, x, y, radius=20, heading=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.heading = heading

        # Arayüzden değiştirilebilir değerler
        self.sensor_angle_degrees = 30.0
        self.speed_multiplier = 1.0

        self.sensor_offset_angle = math.radians(
            self.sensor_angle_degrees
        )
        self.sensor_dist = radius

        self.intensity_left = 0.0
        self.intensity_right = 0.0

        self.left_motor_speed = 0.0
        self.right_motor_speed = 0.0

        self.forward_speed = 0.0
        self.turning_rate = 0.0

        self.trigger_timer = 0
        self.triggered = False

        self.trail = []
        self.max_trail_length = 400

    def set_sensor_angle(self, degrees):
        """
        Her bir sensörün aracın orta çizgisine göre açısıdır.

        Örneğin 30 derece seçilirse:
        sol sensör +30 derece,
        sağ sensör -30 derece olur.

        Dolayısıyla iki sensör arasındaki toplam açı 60 derecedir.
        """
        self.sensor_angle_degrees = float(degrees)
        self.sensor_offset_angle = math.radians(
            self.sensor_angle_degrees
        )

    def set_speed_multiplier(self, multiplier):
        self.speed_multiplier = max(
            0.1,
            float(multiplier),
        )

    def sensor_positions(self):
        angle = self.sensor_offset_angle
        distance = self.sensor_dist

        left_local_x = math.cos(angle) * distance
        left_local_y = math.sin(angle) * distance

        right_local_x = math.cos(-angle) * distance
        right_local_y = math.sin(-angle) * distance

        cos_heading = math.cos(self.heading)
        sin_heading = math.sin(self.heading)

        left_world_x = (
            self.x
            + cos_heading * left_local_x
            - sin_heading * left_local_y
        )

        left_world_y = (
            self.y
            + sin_heading * left_local_x
            + cos_heading * left_local_y
        )

        right_world_x = (
            self.x
            + cos_heading * right_local_x
            - sin_heading * right_local_y
        )

        right_world_y = (
            self.y
            + sin_heading * right_local_x
            + cos_heading * right_local_y
        )

        return (
            (left_world_x, left_world_y),
            (right_world_x, right_world_y),
        )

    def intensity_at(
        self,
        point_x,
        point_y,
        light_x,
        light_y,
    ):
        dx = light_x - point_x
        dy = light_y - point_y

        distance_squared = dx * dx + dy * dy

        # Yakındaki kaynak güçlü, uzaktaki kaynak zayıf algılanır.
        intensity = 12000 / (
            distance_squared + 12000
        )

        return max(
            0.0,
            min(1.0, intensity),
        )

    def combined_intensity(
        self,
        sensor_position,
        lights,
    ):
        total_intensity = 0.0

        for light in lights:
            total_intensity += self.intensity_at(
                sensor_position[0],
                sensor_position[1],
                light.x,
                light.y,
            )

        return min(
            1.0,
            total_intensity,
        )

    def trigger_logic_output(self):
        """
        Her üçüncü pulse geldiğinde çağrılır.

        Araç:
        - 180 derece döner.
        - Kısa süre kırmızı görünür.
        """
        self.triggered = True
        self.trigger_timer = 45
        self.heading += math.pi

    def update(
        self,
        lights,
        width,
        height,
    ):
        left_sensor, right_sensor = (
            self.sensor_positions()
        )

        self.intensity_left = (
            self.combined_intensity(
                left_sensor,
                lights,
            )
        )

        self.intensity_right = (
            self.combined_intensity(
                right_sensor,
                lights,
            )
        )

        base_speed = (
            0.8 * self.speed_multiplier
        )

        gain = (
            3.2 * self.speed_multiplier
        )

        # Contralateral excitatory bağlantı:
        #
        # Sol sensör -> sağ motor
        # Sağ sensör -> sol motor
        #
        # Böylece araç ışık kaynaklarına yönelir.
        self.left_motor_speed = (
            base_speed
            + gain * self.intensity_right
        )

        self.right_motor_speed = (
            base_speed
            + gain * self.intensity_left
        )

        self.forward_speed = (
            self.left_motor_speed
            + self.right_motor_speed
        ) / 2

        self.turning_rate = (
            self.right_motor_speed
            - self.left_motor_speed
        ) / (2 * self.radius)

        self.heading += self.turning_rate

        self.x += (
            self.forward_speed
            * math.cos(self.heading)
        )

        self.y += (
            self.forward_speed
            * math.sin(self.heading)
        )

        # Ekranın bir tarafından çıkınca diğerinden girer.
        self.x %= width
        self.y %= height

        self.trail.append(
            (int(self.x), int(self.y))
        )

        if (
            len(self.trail)
            > self.max_trail_length
        ):
            self.trail.pop(0)

        if self.trigger_timer > 0:
            self.trigger_timer -= 1
        else:
            self.triggered = False

    def draw_trail(self, surface):
        if len(self.trail) < 2:
            return

        for index in range(
            1,
            len(self.trail),
        ):
            previous_point = (
                self.trail[index - 1]
            )

            current_point = (
                self.trail[index]
            )

            pygame.draw.line(
                surface,
                (105, 125, 165),
                previous_point,
                current_point,
                2,
            )

    def draw(self, surface):
        if self.triggered:
            body_color = (
                255,
                80,
                95,
            )
        else:
            body_color = (
                65,
                125,
                255,
            )

        pygame.draw.circle(
            surface,
            body_color,
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

        # Aracın baktığı yönü gösteren çizgi
        front_x = (
            self.x
            + math.cos(self.heading)
            * self.radius
        )

        front_y = (
            self.y
            + math.sin(self.heading)
            * self.radius
        )

        pygame.draw.line(
            surface,
            (20, 25, 35),
            (self.x, self.y),
            (front_x, front_y),
            3,
        )

        left_sensor, right_sensor = (
            self.sensor_positions()
        )

        # Araç merkezi ile sensörler arasındaki kollar
        pygame.draw.line(
            surface,
            (70, 85, 115),
            (self.x, self.y),
            left_sensor,
            2,
        )

        pygame.draw.line(
            surface,
            (70, 85, 115),
            (self.x, self.y),
            right_sensor,
            2,
        )

        pygame.draw.circle(
            surface,
            (0, 230, 180),
            (
                int(left_sensor[0]),
                int(left_sensor[1]),
            ),
            6,
        )

        pygame.draw.circle(
            surface,
            (0, 230, 180),
            (
                int(right_sensor[0]),
                int(right_sensor[1]),
            ),
            6,
        )