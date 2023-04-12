from Animal import Animal

from random import uniform
import matplotlib.pyplot as plt
from statistics import mean
import imageio


class World:
    def __init__(self, x, y, start_plants, plants_per_step, energy_per_plant, animals, energy_per_animal, parasite_lives, if_draw_simulation):
        self.max_x = x
        self.max_y = y
        self.plants_per_step = plants_per_step
        self.energy_per_plant = energy_per_plant
        self.animals = []
        self.free_parasites = []
        self.plants = []
        self.energy_per_animal = energy_per_animal
        self.parasite_lives = parasite_lives
        self.if_draw_simulation = if_draw_simulation
        for _ in range(animals):
            self.animals.append(Animal(self, uniform(-self.max_x, self.max_x), uniform(-self.max_y, self.max_y), energy_per_animal, 0, 0))
        for _ in range(start_plants):
            self.plants.append((uniform(-self.max_x, self.max_x), uniform(-self.max_y, self.max_y)))

    def simulate(self, start, epochs):
        for _ in range(start):
            self.step()
        epochs = list(range(1, epochs+1))
        num_animals = []
        num_animals_genes = []
        num_parasites = []
        num_parasites_genes = []
        files = []
        for epoch in epochs:
            epoch_animals, epoch_parasites, epoch_parasites_genes, epoch_animals_genes = self.get_statistics(epoch)
            num_animals.append(epoch_animals)
            num_animals_genes.append(epoch_animals_genes)
            num_parasites.append(epoch_parasites)
            num_parasites_genes.append(epoch_parasites_genes)
            if self.if_draw_simulation:
                pos_animals = [animal.get_position() for animal in self.animals]
                if pos_animals:
                    x, y = zip(*pos_animals)
                    plt.scatter(x, y, color="blue")
                if self.plants:
                    x, y = zip(*self.plants)
                    plt.scatter(x, y, color="green")
                pos_parasites = [parasites.get_position() for parasites in self.free_parasites]
                if pos_parasites:
                    x, y = zip(*pos_parasites)
                    plt.scatter(x, y, color="red")
                plt.xlim(-self.max_x, self.max_x)
                plt.ylim(-self.max_y, self.max_y)
                plt.title(f"Epoch: {epoch}")
                plt.savefig(f"./states/{epoch}.png")
                files.append(f"./states/{epoch}.png")
                plt.clf()
            self.step()
        plt.plot(epochs, num_animals, "blue", label="Animals")
        plt.plot(epochs, num_animals_genes, "grey", label="Animals Genes")
        plt.plot(epochs, num_parasites, "red", label="Parasites")
        plt.plot(epochs, num_parasites_genes,  "black", label="Parasites Genes")
        plt.legend()
        plt.savefig("result.png")
        if self.if_draw_simulation:
            with imageio.get_writer("mygif.gif", mode="I") as writer:
                for filename in files:
                    image = imageio.v2.imread(filename)
                    writer.append_data(image)

    def get_statistics(self, epoch):
        all_parasites_genes = []
        all_animals_genes = []
        for animal in self.animals:
            for parasite in animal.parasites:
                all_parasites_genes.append(parasite.genes)
        for parasite in self.free_parasites:
            all_parasites_genes.append(parasite.genes)
        parasites = 0
        for animal in self.animals:
            all_animals_genes.append(animal.genes)
            parasites += len(animal.parasites)
        print(f"{epoch}: parasites ({parasites + len(self.free_parasites)}): {mean(all_parasites_genes)}, animals ({len(self.animals)}): {mean(all_animals_genes)}, plants: {len(self.plants)}")
        return len(self.animals), parasites + len(self.free_parasites), mean(all_parasites_genes), mean(all_animals_genes)

    def step(self):
        self.animals.sort(key=lambda a: a.get_power(), reverse=True)

        for _ in range(self.plants_per_step):
            if len(self.plants)>=4*self.max_x*self.max_y:
                break
            self.plants.append((uniform(-self.max_x, self.max_x), uniform(-self.max_y, self.max_y)))

        for animal in self.animals:
            animal.move()

        for animal in self.animals:
            animal.eat()

        for animal in self.animals:
            animal.change_energy()

        alive_animals = []
        for animal in self.animals:
            if animal.dead():
                self.free_parasites += animal.parasites
            else:
                alive_animals.append(animal)
        self.animals = alive_animals

        alive_parasites = []
        for parasite in self.free_parasites:
            if parasite.dead():
                pass
            else:
                alive_parasites.append(parasite)
        self.free_parasites = alive_parasites

        for parasite in self.free_parasites:
            parasite.lives -= 1

        for parasite in self.free_parasites:
            parasite.move()

        for animal in self.animals:
            animal.pick_up()

        for animal in self.animals:
            animal.multiply()