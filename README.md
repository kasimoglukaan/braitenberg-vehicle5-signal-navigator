# Vehicle 5 – Signal Pattern Navigator

An extended implementation of a **Braitenberg Vehicle 5** simulation developed in Python using **Pygame**.

This project explores how a simple autonomous vehicle can exhibit increasingly complex behavior by combining sensor inputs with different logic processing modes. In addition to the classic threshold-based approach, the project introduces multiple navigation logics and an interactive control interface.

---

## Features

### Three Logic Modes

### Counter Mode
- Counts detected activation pulses.
- Generates an output whenever the activation threshold is reached.
- Threshold can be adjusted during runtime.

### Memory Mode
- Learns the sequence of recently visited light sources.
- Displays the learned sequence in real time.
- Includes a **Reset Learned Sequence** button.

### Signal Mode (Custom Extension)
A new logic mode designed specifically for this project.

Each light source performs a different logical operation:

| Light | Effect |
|--------|--------|
| Yellow | +1 Excitatory signal |
| Red | -1 Inhibitory signal |
| Green | -2 Strong inhibitory signal |
| Purple | +2 Excitatory boost |

The accumulated activation value is continuously compared against an adjustable threshold.

---

## Adjustable Parameters

The graphical interface allows the user to modify simulation parameters while the vehicle is moving.

- Vehicle speed
- Sensor angle
- Logic threshold
- Logic mode selection
- Reset learned sequence
- Play/Pause simulation

---

## Simulation

The vehicle:

- Detects nearby light sources using two sensors.
- Calculates motor speeds from sensor intensities.
- Steers toward light sources.
- Leaves a movement trail.
- Updates logic outputs in real time.

---

## User Interface

The interface contains:

- Live simulation world
- Sensor and motor values
- Logic status panel
- Runtime controls
- Adjustable sliders
- Logic mode buttons

---

## Technologies

- Python 3
- Pygame

---

## Project Structure

```
vehicle.py              Vehicle behaviour
light.py                Light source definitions
logic.py                Counter / Memory / Signal logic
ui.py                   User interface
main.py                 Main simulation loop
vehicle_basecode.py     Original laboratory template
```

---

## Future Improvements

Possible future extensions include:

- Multiple vehicle support
- Dynamic moving light sources
- Heat-map visualization
- Obstacle avoidance
- CSV experiment logging
- Custom logic editor
- Additional signal processing algorithms

---

## Author

Kaan Kasımoğlu

Artificial Intelligence MSc Student

BTU Cottbus–Senftenberg

---

## License

This project was developed for educational purposes.