class ThresholdDevice:
    def __init__(self, threshold: int, name: str):
        self.threshold = threshold
        self.name = name
        self.activation = 0
        self.active = False

    def reset_input(self):
        self.activation = 0

    def add_excitation(self, amount: int = 1):
        self.activation += amount

    def add_inhibition(self, amount: int = 1):
        self.activation -= amount

    def evaluate(self):
        self.active = self.activation >= self.threshold
        return self.active