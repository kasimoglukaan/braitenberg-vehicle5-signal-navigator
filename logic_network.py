from threshold import ThresholdDevice


class LogicNetwork:
    def __init__(self):
        self.pulse_count = 0

        self.input_device = ThresholdDevice(1, "Input")
        self.counter_device = ThresholdDevice(3, "Counter")
        self.output_device = ThresholdDevice(1, "Output")

        self.output_active = False

    def receive_pulse(self):
        self.pulse_count += 1

        self.input_device.reset_input()
        self.input_device.add_excitation(1)
        self.input_device.evaluate()

        self.counter_device.reset_input()
        self.counter_device.add_excitation(self.pulse_count)

        if self.counter_device.evaluate():
            self.output_device.reset_input()
            self.output_device.add_excitation(1)
            self.output_active = self.output_device.evaluate()

            self.pulse_count = 0
        else:
            self.output_active = False

        return self.output_active

    def reset(self):
        self.pulse_count = 0
        self.output_active = False

        self.input_device.reset_input()
        self.counter_device.reset_input()
        self.output_device.reset_input()