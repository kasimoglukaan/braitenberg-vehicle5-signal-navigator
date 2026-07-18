from threshold import ThresholdDevice


class LogicNetwork:
    COUNTER_MODE = "counter"
    MEMORY_MODE = "memory"
    SIGNAL_MODE = "signal"

    def __init__(self):
        self.mode = self.COUNTER_MODE

        # Counter ve Signal Mode
        self.counter_threshold = 3
        self.pulse_count = 0

        # Memory Mode
        self.memory_length = 3
        self.learned_sequence = []
        self.current_sequence = []
        self.learning_complete = False

        # Genel durum bilgileri
        self.total_pulses = 0
        self.output_count = 0
        self.output_active = False

        self.last_detected_source = "-"
        self.last_signal_action = "-"

        # Temel threshold cihazları
        self.input_device = ThresholdDevice(
            threshold=1,
            name="Input",
        )

        self.counter_device = ThresholdDevice(
            threshold=self.counter_threshold,
            name="Counter",
        )

        self.output_device = ThresholdDevice(
            threshold=1,
            name="Output",
        )

    def set_mode(self, mode):
        valid_modes = (
            self.COUNTER_MODE,
            self.MEMORY_MODE,
            self.SIGNAL_MODE,
        )

        if mode not in valid_modes:
            return

        if self.mode != mode:
            self.mode = mode
            self.reset_working_memory()

    def set_counter_threshold(self, threshold):
        threshold = int(round(threshold))
        threshold = max(
            2,
            min(10, threshold),
        )

        if (
            threshold
            == self.counter_threshold
        ):
            return

        self.counter_threshold = threshold
        self.counter_device.threshold = threshold

        if self.mode in (
            self.COUNTER_MODE,
            self.SIGNAL_MODE,
        ):
            self.pulse_count = 0
            self.output_active = False

    def receive_pulse(
        self,
        source_id,
        source_type="excitatory",
    ):
        """
        Araç bir kaynağı algıladığında çağrılır.
        """

        source_id = str(source_id)

        self.total_pulses += 1
        self.last_detected_source = source_id
        self.output_active = False

        self._activate_input_device()

        if self.mode == self.COUNTER_MODE:
            self.last_signal_action = "+1 pulse"

            return self._process_counter_mode()

        if self.mode == self.MEMORY_MODE:
            self.last_signal_action = (
                f"Remember source {source_id}"
            )

            return self._process_memory_mode(
                source_id
            )

        return self._process_signal_mode(
            source_type
        )

    def _activate_input_device(self):
        self.input_device.reset_input()
        self.input_device.add_excitation(1)
        self.input_device.evaluate()

    # --------------------------------------------------
    # Counter Mode
    # --------------------------------------------------

    def _process_counter_mode(self):
        self.pulse_count += 1

        if (
            self.pulse_count
            >= self.counter_threshold
        ):
            self._activate_output()

            # Yeni sayım döngüsü
            self.pulse_count = 0

            return True

        return False

    # --------------------------------------------------
    # Memory Mode
    # --------------------------------------------------

    def _process_memory_mode(
        self,
        source_id,
    ):
        # İlk üç kaynak sırasını öğrenir.
        if not self.learning_complete:
            self.learned_sequence.append(
                source_id
            )

            self.pulse_count = len(
                self.learned_sequence
            )

            if (
                len(self.learned_sequence)
                >= self.memory_length
            ):
                self.learning_complete = True
                self.current_sequence.clear()
                self.pulse_count = 0

            return False

        # Öğrenilen sırayı yeniden arar.
        self.current_sequence.append(
            source_id
        )

        self.pulse_count = len(
            self.current_sequence
        )

        if (
            len(self.current_sequence)
            < self.memory_length
        ):
            return False

        sequence_matches = (
            self.current_sequence
            == self.learned_sequence
        )

        self.current_sequence.clear()
        self.pulse_count = 0

        if sequence_matches:
            self._activate_output()
            return True

        return False

    # --------------------------------------------------
    # Signal Mode
    # --------------------------------------------------

    def _process_signal_mode(
        self,
        source_type,
    ):
        """
        Sarı kaynak:
            +1 excitatory activation

        Kırmızı kaynak:
            -1 inhibitory activation

        Yeşil kaynak:
            -2 strong inhibitory activation

        Mor kaynak:
            +2 excitatory boost
        """

        if source_type == "excitatory":
            self.pulse_count += 1

            self.last_signal_action = (
                "Excitatory +1"
            )

        elif source_type == "inhibitory":
            self.pulse_count -= 1

            self.pulse_count = max(
                0,
                self.pulse_count,
            )

            self.last_signal_action = (
                "Inhibitory -1"
            )

        elif (
            source_type
            == "strong_inhibitory"
        ):
            self.pulse_count -= 2

            self.pulse_count = max(
                0,
                self.pulse_count,
            )

            self.last_signal_action = (
                "Strong inhibition -2"
            )

        elif source_type == "boost":
            self.pulse_count += 2

            self.last_signal_action = (
                "Excitatory boost +2"
            )

        else:
            self.last_signal_action = (
                "Unknown signal"
            )

        if (
            self.pulse_count
            >= self.counter_threshold
        ):
            self._activate_output()

            # Output sonrasında yeni döngü
            self.pulse_count = 0

            return True

        return False

    def _activate_output(self):
        self.output_device.reset_input()
        self.output_device.add_excitation(1)

        self.output_active = (
            self.output_device.evaluate()
        )

        if self.output_active:
            self.output_count += 1

    # --------------------------------------------------
    # ON / OFF gösterimi
    # --------------------------------------------------

    def counter_device_statuses(
        self,
        output_is_visible=False,
    ):
        """
        Threshold değeri 3 ise:

        OFF OFF OFF OFF
        ON  OFF OFF OFF
        ON  ON  OFF OFF

        Output oluştuğunda:
        ON ON ON ON
        """

        total_devices = (
            self.counter_threshold + 1
        )

        if output_is_visible:
            return ["ON"] * total_devices

        statuses = []

        active_count = min(
            self.pulse_count,
            self.counter_threshold,
        )

        for index in range(
            self.counter_threshold
        ):
            if index < active_count:
                statuses.append("ON")
            else:
                statuses.append("OFF")

        # Son kutu output cihazıdır.
        statuses.append("OFF")

        return statuses

    # --------------------------------------------------
    # Reset işlemleri
    # --------------------------------------------------

    def reset_memory(self):
        """
        Araç hareket ederken yalnızca Memory Mode
        öğrenmesini sıfırlar.
        """

        self.learned_sequence.clear()
        self.current_sequence.clear()

        self.learning_complete = False
        self.pulse_count = 0
        self.output_active = False

        self.last_detected_source = "-"
        self.last_signal_action = "-"

        self.input_device.reset_input()
        self.counter_device.reset_input()
        self.output_device.reset_input()

    def reset_working_memory(self):
        """
        Mod değiştirildiğinde geçici durumları temizler.
        """

        self.pulse_count = 0
        self.output_active = False
        self.last_signal_action = "-"

        self.learned_sequence.clear()
        self.current_sequence.clear()
        self.learning_complete = False

        self.input_device.reset_input()
        self.counter_device.reset_input()
        self.output_device.reset_input()

    def reset(self):
        """
        Tüm logic network'ü başlangıç durumuna getirir.
        """

        self.pulse_count = 0
        self.total_pulses = 0
        self.output_count = 0
        self.output_active = False

        self.last_detected_source = "-"
        self.last_signal_action = "-"

        self.learned_sequence.clear()
        self.current_sequence.clear()
        self.learning_complete = False

        self.input_device.reset_input()
        self.counter_device.reset_input()
        self.output_device.reset_input()

    def learned_sequence_text(self):
        if not self.learned_sequence:
            return "-"

        return " -> ".join(
            self.learned_sequence
        )

    def current_sequence_text(self):
        if not self.current_sequence:
            return "-"

        return " -> ".join(
            self.current_sequence
        )