import random
import string

# The target word we want to evolve to
TARGET = "The quick brown fox jumps over a lazy dog"

# GA parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.01  # probability of mutating each character
MAX_GENERATIONS = 10000

# Allowed characters (includes letters, punctuation, and space)
ALLOWED_CHARS = string.ascii_letters + " ,!?;:'\""


def random_candidate() -> str:
    """Generate a random candidate string of the same length as TARGET."""
    return "".join(random.choice(ALLOWED_CHARS) for _ in range(len(TARGET)))


def fitness(candidate: str) -> int:
    """
    Calculate the fitness of a candidate.
    Fitness is defined as the number of characters that match the target in the correct position.
    """
    return sum(1 for a, b in zip(candidate, TARGET) if a == b)


def mutate(candidate: str) -> str:
    """
    Mutate the candidate string by randomly changing each character with probability MUTATION_RATE.
    """
    candidate_list = list(candidate)
    for i in range(len(candidate_list)):
        if random.random() < MUTATION_RATE:
            candidate_list[i] = random.choice(ALLOWED_CHARS)
    return "".join(candidate_list)


def crossover(parent1: str, parent2: str) -> str:
    """
    Perform a one-point crossover between two parents.
    A random crossover point is chosen and the child inherits the first part from parent1 and the rest from parent2.
    """
    index = random.randint(0, len(parent1) - 1)
    child = parent1[:index] + parent2[index:]
    return child


def select_parent(population: list) -> str:
    """
    Select a parent from the population using tournament selection.
    A few candidates are picked at random, and the one with the highest fitness is chosen.
    """
    tournament_size = 5
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda candidate: fitness(candidate), reverse=True)
    return tournament[0]


def genetic_algorithm():
    # Initialize the population with random candidates
    population = [random_candidate() for _ in range(POPULATION_SIZE)]
    generation = 0

    while generation < MAX_GENERATIONS:
        # Sort population by fitness (highest fitness first)
        population.sort(key=lambda candidate: fitness(candidate), reverse=True)
        best_candidate = population[0]
        best_fit = fitness(best_candidate)
        print(
            f"Generation {generation}: Best = '{best_candidate}' Fitness = {best_fit}"
        )

        # Check if we've reached the target
        if best_candidate == TARGET:
            print("Target reached!")
            return best_candidate

        new_population = []
        # Optionally: Use elitism by carrying the best candidate to the next generation
        new_population.append(best_candidate)

        # Generate new candidates until we have a full population
        while len(new_population) < POPULATION_SIZE:
            # Select two parents via tournament selection
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            # Create a new candidate via crossover
            child = crossover(parent1, parent2)
            # Apply mutation to the child
            child = mutate(child)
            new_population.append(child)

        population = new_population
        generation += 1

    print("Maximum generations reached without finding the target.")
    return None


if __name__ == "__main__":
    genetic_algorithm()
