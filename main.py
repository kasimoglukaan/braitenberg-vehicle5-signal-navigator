import pygame

from light import Light
from logic_network import LogicNetwork
from ui import Dashboard
from vehicle import Vehicle


pygame.init()

SIMULATION_WIDTH = 780
DASHBOARD_WIDTH = 390

HEIGHT = 910
WIDTH = (
    SIMULATION_WIDTH
    + DASHBOARD_WIDTH
)

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
        # Sarı: +1
        Light(
            145,
            145,
            label="1",
            source_type="excitatory",
        ),

        # Kırmızı: -1
        Light(
            590,
            150,
            label="2",
            source_type="inhibitory",
        ),

        # Yeşil: -2
        Light(
            660,
            650,
            label="3",
            source_type=(
                "strong_inhibitory"
            ),
        ),

        # Mor: +2
        Light(
            190,
            700,
            label="4",
            source_type="boost",
        ),

        # Sarı: +1
        Light(
            410,
            410,
            label="5",
            source_type="excitatory",
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

# Sağ tıklamayla eklenen kaynakların sırası
source_type_order = [
    "excitatory",
    "inhibitory",
    "strong_inhibitory",
    "boost",
]

next_source_type_index = 0


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
                selected_mode = (
                    logic_network.mode
                )

                (
                    vehicle,
                    logic_network,
                    lights,
                ) = reset_simulation()

                logic_network.set_mode(
                    selected_mode
                )

                selected_light = None

        elif (
            event.type
            == pygame.MOUSEBUTTONDOWN
        ):
            if (
                event.pos[0]
                < SIMULATION_WIDTH
            ):
                # Sol tıklama:
                # Kaynağı seç ve sürükle.
                if event.button == 1:
                    selected_light = None

                    for light in reversed(
                        lights
                    ):
                        if light.contains(
                            event.pos
                        ):
                            selected_light = (
                                light
                            )
                            break

                # Sağ tıklama:
                # Yeni kaynak oluştur.
                elif event.button == 3:
                    source_type = (
                        source_type_order[
                            next_source_type_index
                        ]
                    )

                    next_source_type_index = (
                        next_source_type_index
                        + 1
                    ) % len(source_type_order)

                    new_light = Light(
                        event.pos[0],
                        event.pos[1],
                        label=str(
                            len(lights) + 1
                        ),
                        source_type=source_type,
                    )

                    lights.append(new_light)

        elif (
            event.type
            == pygame.MOUSEBUTTONUP
        ):
            if event.button == 1:
                selected_light = None

        elif (
            event.type
            == pygame.MOUSEMOTION
        ):
            if selected_light is not None:
                mouse_x = max(
                    20,
                    min(
                        SIMULATION_WIDTH
                        - 20,
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
                    (
                        mouse_x,
                        mouse_y,
                    )
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

            # Araç kaynağa ilk kez girdiğinde
            # bir pulse üret.
            if (
                distance
                <= detection_distance
                and not light.detected
            ):
                light.detected = True

                output_active = (
                    logic_network.receive_pulse(
                        source_id=light.label,
                        source_type=(
                            light.source_type
                        ),
                    )
                )

                if output_active:
                    vehicle.trigger_logic_output()

            # Araç kaynaktan yeterince uzaklaşınca
            # kaynak tekrar algılanabilir hâle gelir.
            elif (
                distance
                > detection_distance + 25
            ):
                light.detected = False

    # Simülasyon arka planı
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

    # Izgara
    grid_spacing = 40

    for grid_x in range(
        0,
        SIMULATION_WIDTH,
        grid_spacing,
    ):
        pygame.draw.line(
            screen,
            (215, 220, 230),
            (
                grid_x,
                0,
            ),
            (
                grid_x,
                HEIGHT,
            ),
        )

    for grid_y in range(
        0,
        HEIGHT,
        grid_spacing,
    ):
        pygame.draw.line(
            screen,
            (215, 220, 230),
            (
                0,
                grid_y,
            ),
            (
                SIMULATION_WIDTH,
                grid_y,
            ),
        )

    # Araç izi
    vehicle.draw_trail(screen)

    # Kaynaklar
    for light in lights:
        light.draw(
            screen,
            label_font,
        )

    # Araç
    vehicle.draw(screen)

    # Sağ panel
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