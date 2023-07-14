import numpy as np

def objective_function(x):
    """The objective function to be minimized"""
    return np.sum(np.square(x))

def initialize_employed_bees(num_employed_bees=5, num_dimensions=2, bounds=[(0, 10), (-5, 5)]):
    """Initialize the employed bees with random positions"""
    employed_bees = np.zeros((num_employed_bees, num_dimensions))
    for i in range(num_employed_bees):
        for j in range(num_dimensions):
            employed_bees[i, j] = bounds[j][0] + (bounds[j][1] - bounds[j][0]) * np.random.rand()
    return employed_bees

def evaluate_population(population, fitness_function):
    """Evaluate the fitness of the population"""
    fitness = np.zeros(len(population))
    for i in range(len(population)):
        fitness[i] = fitness_function(population[i])
    return fitness

def select_best_food_source(employed_bees, fitness):
    """Select the best food source from the employed bees"""
    index = np.argmin(fitness)
    return employed_bees[index], fitness[index]

def select_partner_food_source(employed_bees, exclude_index):
    """Select a partner food source randomly, excluding the given index"""
    partner_index = np.random.randint(len(employed_bees))
    while partner_index == exclude_index:
        partner_index = np.random.randint(len(employed_bees))
    return employed_bees[partner_index]

def scout_bees(employed_bees, num_scout_bees, num_dimensions, bounds):
    """Replace the abandoned food sources with new random positions"""
    for i in range(num_scout_bees):
        for j in range(num_dimensions):
            employed_bees[i, j] = bounds[j][0] + (bounds[j][1] - bounds[j][0]) * np.random.rand()

def abc(num_employed_bees, num_onlooker_bees, num_iterations=100,bounds): 
    """Run the Artificial Bee Colony algorithm"""
    num_dimensions = len(bounds)
    employed_bees = initialize_employed_bees(num_employed_bees, num_dimensions, bounds)
    fitness = evaluate_population(employed_bees, objective_function)
    best_solution, best_fitness = select_best_food_source(employed_bees, fitness)
    for iteration in range(num_iterations):
        # Employed bee phase
        for i in range(num_employed_bees):
            partner = select_partner_food_source(employed_bees, i)
            index = np.random.randint(num_dimensions)
            new_solution = employed_bees[i].copy()
            new_solution[index] = partner[index]
            new_fitness = objective_function(new_solution)
            if new_fitness < fitness[i]:
                employed_bees[i] = new_solution
                fitness[i] = new_fitness
        # Onlooker bee phase
        probabilities = fitness / np.sum(fitness)
        for i in range(num_onlooker_bees):
            index = np.random.choice(num_employed_bees, p=probabilities)
            partner = select_partner_food_source(employed_bees, index)
            index = np.random.randint(num_dimensions)
            new_solution = employed_bees[index].copy()
            new_solution[index] = partner[index]
            new_fitness = objective_function(new_solution)
            if new_fitness < fitness[index]:
                employed_bees[index] = new_solution
                fitness[index] = new_fitness
        # Scout bee phase
        best_solution, best_fitness = select_best_food_source(employed_bees, fitness)
        scout_bees(employed_bees, np.sum(fitness == best_fitness), num_dimensions, bounds)
    return