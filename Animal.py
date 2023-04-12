from Parasite import Parasite

from math import sin, cos, pi, dist
from random import uniform, choice


class Animal:
    def __init__(self, world, x, y, energy, genes, parasite_genes):
        self.world = world
        self.energy = energy
        self.x = x
        self.y = y
        self.parasites = []
        self.parasites.append(Parasite(self, parasite_genes))
        self.genes = max(genes + uniform(-0.2, 0.2), 0)

    def get_power(self):
        energy_of_parasites = 0
        for parasite in self.parasites:
            energy_of_parasites += parasite.genes
        return energy_of_parasites

    def get_position(self):
        return (self.x, self.y)

    def dead(self):
        return self.energy <= 0

    def move(self):
        angle = uniform(0, 2*pi)
        self.x += self.genes * cos(angle)
        self.y += self.genes * sin(angle)

        self.x = min(self.world.max_x, self.x)
        self.y = min(self.world.max_y, self.y)
        self.x = max(-self.world.max_x, self.x)
        self.y = max(-self.world.max_y, self.y)

        for parasite in self.parasites:
            parasite.x = self.x
            parasite.y = self.y

    def eat(self):
        plants = self.world.plants
        new_plants = []
        for plant in plants:
            if dist(self.get_position(), plant) < 5:
                self.energy += self.world.energy_per_plant
            else:
                new_plants.append(plant)
        self.world.plants = new_plants

    def change_energy(self):
        for parasite in self.parasites:
            self.energy -= parasite.genes
        self.energy -= 1 + self.genes

    def pick_up(self):
        free_parasites = self.world.free_parasites
        new_free_parasites = []
        for parasite in free_parasites:
            if dist(self.get_position(), parasite.get_position()) < 1:
                if len(self.parasites) < 5:
                    self.parasites.append(parasite)
                    parasite.live = self.world.parasite_lives
                else:
                    break
            else:
                new_free_parasites.append(parasite)
        self.world.free_parasites = new_free_parasites

    def multiply(self):
        if self.energy < 1.5 * self.world.energy_per_animal:
            if len(self.parasites) > 1:
                parasite_to_remove = choice(self.parasites)
                self.parasites.remove(parasite_to_remove)
        if self.energy > 3 * self.world.energy_per_animal:
            if len(self.parasites) < 5:
                self.parasites.append(Parasite(self, choice(self.parasites).genes))
        if self.energy > 5 * self.world.energy_per_animal:
            self.world.animals.append(Animal(self.world, self.x, self.y, self.energy/2, self.genes, choice(self.parasites).genes))
            self.energy /= 2

    def __str__(self):
        return f"position: {self.get_position()}, power: {self.get_power()}, energy: {self.energy}, parasites: {len(self.parasites)}"
