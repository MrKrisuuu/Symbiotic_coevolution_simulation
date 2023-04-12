from World import World


if __name__ == "__main__":
    #world
    max_x = 25
    max_y = 25
    start_plants = 100
    plants_per_step = 5
    energy_per_plant = 100
    #animals
    animals = 50
    energy_per_animal = 25
    #parasites
    parasite_lives = 20
    #simulation
    world = World(max_x, max_y, start_plants, plants_per_step, energy_per_plant, animals, energy_per_animal, parasite_lives, False)
    world.simulate(0, 10000)

# prosta wizualizacja
