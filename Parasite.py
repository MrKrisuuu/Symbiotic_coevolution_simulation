from math import sin, cos, pi
from random import uniform


class Parasite:
    def __init__(self, animal, genes):
        self.carrier = animal
        self.x = animal.x
        self.y = animal.y
        self.lives = animal.world.parasite_lives
        self.genes = max(genes + uniform(-0.2, 0.2), 0)  # power and energy

    def get_position(self):
        return (self.x, self.y)

    def move(self):
        angle = uniform(0, 2 * pi)
        self.x += cos(angle)
        self.y += sin(angle)

        self.x = min(self.carrier.world.max_x, self.x)
        self.y = min(self.carrier.world.max_y, self.y)
        self.x = max(-self.carrier.world.max_x, self.x)
        self.y = max(-self.carrier.world.max_y, self.y)

    def dead(self):
        return self.lives <= 0