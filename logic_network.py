from threshold import ThresholdDevice


class LogicNetwork:
    COUNTER_MODE = "counter"
    MEMORY_MODE = "memory"

    def __init__(self):
        self.mode = self.COUNTER_MODE

        # Counter Mode ayarları
        self.counter_threshold = 3
        self.pulse_count = 0

        # Memory Mode ayarları
        self.memory_length = 3
        self.learned_sequence = []
        self.current_sequence = []
        self.learning_complete = False

        # Genel istatistikler
        self.total_pulses = 0
        self.output_count = 0
        self.output_active = False
        self.last_detected_source = "-"

        # Vehicle 5 threshold devices
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
        if mode not in (
            self.COUNTER_MODE,
            self.MEMORY_MODE,
        ):
            return

        if self.mode != mode:
            self.mode = mode
            self.reset_working_memory()

    def set_counter_threshold(self, threshold):
        threshold = int(round(threshold))
        threshold = max(2, min(10, threshold))

        if threshold != self.counter_threshold:
            self.counter_threshold = threshold
            self.counter_device.threshold = threshold

            # Threshold değiştiğinde yarım kalmış sayım temizlenir.
            if self.mode == self.COUNTER_MODE:
                self.pulse_count = 0
                self.output_active = False

    def receive_pulse(self, source_id):
        """
        Bir ışık kaynağı ilk kez algılandığında çağrılır.

        source_id:
            Işık kaynağının etiketi.
            Örnek: "1", "2", "3"
        """
        source_id = str(source_id)

        self.total_pulses += 1
        self.last_detected_source = source_id
        self.output_active = False

        self._activate_input_device()

        if self.mode == self.COUNTER_MODE:
            return self._process_counter_mode()

        return self._process_memory_mode(source_id)

    def _activate_input_device(self):
        self.input_device.reset_input()
        self.input_device.add_excitation(1)
        self.input_device.evaluate()

    def _process_counter_mode(self):
        self.pulse_count += 1

        self.counter_device.reset_input()
        self.counter_device.add_excitation(
            self.pulse_count
        )

        counter_active = (
            self.counter_device.evaluate()
        )

        if counter_active:
            self._activate_output()

            # Yeni sayma döngüsü
            self.pulse_count = 0
            self.counter_device.reset_input()

            return True

        return False

    def _process_memory_mode(self, source_id):
        """
        İlk üç kaynak sırasını öğrenir.

        Örnek:
            Öğrenilen sıra: 2 -> 5 -> 1

        Bundan sonra yalnızca tekrar:
            2 -> 5 -> 1

        algılanırsa output üretir.
        """

        # Öğrenme aşaması
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

        # Tanıma aşaması
        self.current_sequence.append(source_id)
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

        self.output_active = False
        return False

    def _activate_output(self):
        self.output_device.reset_input()
        self.output_device.add_excitation(1)

        self.output_active = (
            self.output_device.evaluate()
        )

        if self.output_active:
            self.output_count += 1

    def reset_working_memory(self):
        """
        Mod değiştirilince aktif sayma ve öğrenme
        işlemlerini temizler. Genel istatistikleri korur.
        """
        self.pulse_count = 0
        self.output_active = False

        self.learned_sequence.clear()
        self.current_sequence.clear()
        self.learning_complete = False

        self.input_device.reset_input()
        self.counter_device.reset_input()
        self.output_device.reset_input()

    def reset(self):
        """
        Bütün logic network'ü başlangıç durumuna getirir.
        """
        self.pulse_count = 0
        self.total_pulses = 0
        self.output_count = 0
        self.output_active = False
        self.last_detected_source = "-"

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