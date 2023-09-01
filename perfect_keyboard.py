import random

# Create a string of keyboard letters of 1st gen keyboard
def init_population(pop_size):
    keyboardCharacters = list('qazwsxedcrfvtgbyhnujmik,ol.p;/')
    population = []

    # Initialize the empty population list with random characters
    for i in range (pop_size):
        rand_genome = keyboardCharacters [:] # We have a variable that takes the characters from the list and
                                             # puts them in a string (variable: rand_genome).
        print (rand_genome)
        random. shuffle(rand_genome)
        population.append (rand_genome)
        return population
        
    
# Create the next gen layout 
def new_generation_layout(population, sorted_evals, p_size):
    new_generation = []

    # Sort population by distance 
    sorted_population = []
    for i in sorted_evals:
        sorted_population.append(population[i])

    # Copy the best 10% of the layouts to the next generation
    for i in range(int(p_size*0.1)):
        new_generation.append(sorted_population [1])

    # Combine two keyboards from the top 50% of the generation 
    # and add the new_keyboard to the generation
    for _ in range (int(p_size*0.9)):
        p1 = random.choice (sorted_population[:int(p_size*0.5)])
        p2 = random.choice (sorted_population[:int(p_size*0.5)])
        child = mate(p1, p2)
        new_generation.append(child)

    return new_generation


# Combine two keyboards together 
def mate(keyboard1, keyboard2):
    index = random.randint(0, 29)
    length = random.randint(0, 29)
    child = ['_' for i in range (30)]

    # Add left keys from keyboard1
    for i in range(length):
        if index>29:
            index = 0
        child[index]= keyboard1[index]
        index+=1

    # Add right keys from keyboard2
    child_index = index
    while '_' in child:
        if index > 29:
            index = 0
        if child_index > 29:
            child_index = 0
        char = keyboard2[index]
        if char in child:
            index += 1
            continue
        child[child_index] = keyboard2[index]
        child_index += 1
        index += 1

    # 10% chance of random mutation
    probability = random.random()
    if probability > 0.9:
        point1 = random.randint(0, 29)
        point2 = random.randint(0, 29)
        allele1 = child[point1]
        allele2 = child[point2]
        child[point1] = allele2
        child[point2] = allele1

    return child

def evaluate_fitness(population, target_frequencies):
    fitness_scores = []

    # Evaluate the fitness of each keyboard layout in the population
    for keyboard in population:
        score = 0
        for i in range(len(keyboard)):
            if keyboard[i] in target_frequencies[i]:
                score += 1
        fitness_scores.append(score)

    return fitness_scores


# Define the population size
population_size = 100

# Initialize the current population
current_population = init_population(population_size)

# Define the target frequencies for each key
target_frequencies = [
    ['q', 'a', 'z', 'w', 's', 'x', 'e', 'd', 'c', 'r', 'f', 'v', 't', 'g', 'b', 'y', 'h', 'n', 'u', 'j', 'm', 'i', 'k', ',', 'o', 'l', '.', 'p', ';', '/'],]

# Evaluate the fitness of each keyboard layout in the current population
fitness_scores = evaluate_fitness(current_population, target_frequencies)

# Sort the fitness scores in ascending order and get the corresponding indices
sorted_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k])

# Sort the evaluations in descending order
sorted_evaluations = list(reversed(sorted_indices))

# Generate a new population
new_population = new_generation_layout(current_population, sorted_evaluations, population_size)

# Print each keyboard layout in the new population
for keyboard in new_population:
    print(keyboard)


