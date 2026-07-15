import pygame

from light import Light
from logic_network import LogicNetwork
from ui import Dashboard
from vehicle import Vehicle


pygame.init()

SIMULATION_WIDTH = 780
DASHBOARD_WIDTH = 370

HEIGHT = 910
WIDTH = SIMULATION_WIDTH + DASHBOARD_WIDTH

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Vehicle 5 - Signal Pattern Navigator"
)

clock = pygame.time.Clock()
fps = 60

label_font = pygame.font.SysFont(
    "consolas",
    15,
    bold=True,
)


def create_lights():
    return [
        Light(
            145,
            145,
            (255, 215, 70),
            "1",
        ),
        Light(
            590,
            150,
            (255, 150, 70),
            "2",
        ),
        Light(
            660,
            650,
            (255, 100, 130),
            "3",
        ),
        Light(
            190,
            700,
            (170, 110, 255),
            "4",
        ),
        Light(
            410,
            410,
            (80, 220, 180),
            "5",
        ),
    ]


def reset_simulation():
    new_vehicle = Vehicle(
        x=90,
        y=HEIGHT // 2,
        heading=0,
    )

    new_logic_network = LogicNetwork()
    new_lights = create_lights()

    return (
        new_vehicle,
        new_logic_network,
        new_lights,
    )


vehicle, logic_network, lights = (
    reset_simulation()
)

dashboard = Dashboard(
    SIMULATION_WIDTH,
    0,
    DASHBOARD_WIDTH,
    HEIGHT,
)

selected_light = None
paused = False
running = True


while running:
    for event in pygame.event.get():
        dashboard.handle_event(
            event,
            logic_network,
        )

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_r:
                selected_mode = logic_network.mode

                (
                    vehicle,
                    logic_network,
                    lights,
                ) = reset_simulation()

                logic_network.set_mode(
                    selected_mode
                )

                selected_light = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] < SIMULATION_WIDTH:
                if event.button == 1:
                    selected_light = None

                    for light in reversed(lights):
                        if light.contains(event.pos):
                            selected_light = light
                            break

                elif event.button == 3:
                    new_label = str(
                        len(lights) + 1
                    )

                    lights.append(
                        Light(
                            event.pos[0],
                            event.pos[1],
                            (255, 205, 70),
                            new_label,
                        )
                    )

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected_light = None

        elif event.type == pygame.MOUSEMOTION:
            if selected_light is not None:
                mouse_x = max(
                    20,
                    min(
                        SIMULATION_WIDTH - 20,
                        event.pos[0],
                    ),
                )

                mouse_y = max(
                    20,
                    min(
                        HEIGHT - 20,
                        event.pos[1],
                    ),
                )

                selected_light.move(
                    (mouse_x, mouse_y)
                )

    dashboard.apply_settings(
        vehicle,
        logic_network,
    )

    if not paused:
        vehicle.update(
            lights,
            SIMULATION_WIDTH,
            HEIGHT,
        )

        for light in lights:
            dx = vehicle.x - light.x
            dy = vehicle.y - light.y

            distance = (
                dx * dx + dy * dy
            ) ** 0.5

            detection_distance = (
                vehicle.radius
                + light.radius
                + 20
            )

            if (
                distance <= detection_distance
                and not light.detected
            ):
                light.detected = True

                output_active = (
                    logic_network.receive_pulse(
                        light.label
                    )
                )

                if output_active:
                    vehicle.trigger_logic_output()

            elif (
                distance
                > detection_distance + 25
            ):
                light.detected = False

    screen.fill(
        (235, 238, 245)
    )

    pygame.draw.rect(
        screen,
        (235, 238, 245),
        pygame.Rect(
            0,
            0,
            SIMULATION_WIDTH,
            HEIGHT,
        ),
    )

    grid_spacing = 40

    for x in range(
        0,
        SIMULATION_WIDTH,
        grid_spacing,
    ):
        pygame.draw.line(
            screen,
            (215, 220, 230),
            (x, 0),
            (x, HEIGHT),
        )

    for y in range(
        0,
        HEIGHT,
        grid_spacing,
    ):
        pygame.draw.line(
            screen,
            (215, 220, 230),
            (0, y),
            (
                SIMULATION_WIDTH,
                y,
            ),
        )

    vehicle.draw_trail(screen)

    for light in lights:
        light.draw(
            screen,
            label_font,
        )

    vehicle.draw(screen)

    dashboard.draw(
        screen,
        vehicle,
        logic_network,
        lights,
        paused,
    )

    pygame.display.flip()
    clock.tick(fps)


pygame.quit()