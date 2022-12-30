from config import Config

config = Config.get_instance()


class Route:
    def __init__(self, start_position: tuple[int, int]):
        self.start_position = start_position
        self.available = True
        self.quality = 100
        self.skiers = []

    def move_skiers(self) -> None:
        skiers_skiing = []
        for skier in self.skiers:
            skier.move()
            if skier.y < config.SKIER_MAX_Y:
                skiers_skiing.append(skier)
            elif self.quality > 0:
                self.quality -= config.QUALITY_STEP
        self.skiers = skiers_skiing.copy()

    def is_empty(self) -> bool:
        return len(self.skiers) == 0
