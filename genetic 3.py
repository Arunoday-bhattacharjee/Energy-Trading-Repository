import random

# Define the participants and their characteristics
buyers = {
    1: {"price": 34, "demand": 27},
    2: {"price": 35, "demand": 8},
    3: {"price": 24, "demand": 4},
    4: {"price": 11, "demand": 10},
    5: {"price": 13, "demand": 11},
}

sellers = {
    1: {"price": 8, "supply": 20},
    2: {"price": 9, "supply": 3},
    3: {"price": 11, "supply": 5},
    4: {"price": 12, "supply": 10},
    5: {"price": 14, "supply": 20},
}

total_supply = sum([seller["supply"] for seller in sellers.values()])
total_demand = sum([buyer["demand"] for buyer in buyers.values()])

# Define the genetic algorithm parameters
max_iterations = 250
population_size = 1000
crossover_rate = 0.9
mutation_rate = 0.2

# Define the fitness function
def calculate_fitness(solution):
    trades = []
    total_profit = 0
    
    for buyer, seller, units in solution:
        price = min(buyers[buyer]["price"], sellers[seller]["price"])
        if price == buyers[buyer]["price"] and units <= buyers[buyer]["demand"]:
            buyers[buyer]["demand"] -= units
            sellers[seller]["supply"] -= units
            trades.append((buyer, seller, units))
            total_profit += price * units
    
    return total_profit, trades

# Define the selection function
def selection(population):
    parent1 = random.choice(population)
    parent2 = random.choice(population)
    return parent1, parent2

# Define the crossover function
def crossover(parent1, parent2):
    if random.random() > crossover_rate:
        return parent1, parent2
    
    index = random.randint(0, len(parent1) - 1)
    child1 = parent1[:index] + parent2[index:]
    child2 = parent2[:index] + parent1[index:]
    
    return child1, child2

# Define the mutation function
def mutation(solution):
    if random.random() > mutation_rate:
        return solution
    
    index = random.randint(0, len(solution) - 1)
    buyer, seller, units = solution[index]
    new_buyer = random.choice(list(buyers.keys()))
    new_seller = random.choice(list(sellers.keys()))
    new_units = random.randint(1, max(1, min(buyers[new_buyer]["demand"], sellers[new_seller]["supply"])))
    solution[index] = (new_buyer, new_seller, new_units)
    
    return solution

# Define the initial population
population = [[(buyer, seller, random.randint(1, min(buyers[buyer]["demand"], sellers[seller]["supply"]))) 
               for seller in sellers for buyer in buyers] 
              for i in range(population_size)]

# Run the genetic algorithm
best_solution = None
best_fitness = float("-inf")

for i in range(max_iterations):
    new_population = []
    
    # Select two parents and create two children using crossover and mutation
    for j in range(population_size):
        parent1, parent2 = selection(population)
        child1, child2 = crossover(parent1, parent2)
        child1 = mutation(child1)
        child2 = mutation(child2)
        new_population.extend([child1, child2])
    
    population = new_population
    
    # Evaluate the fitness of each solution in the population and keep track of the best solution
    for solution in population:
        fitness = calculate_fitness(solution)
        if fitness[0] > best_fitness:
            best_fitness = fitness[0]
            best_solution = solution
    
    # Print the best solution and its fitness
    print(f"Iteration {i+1}: Best solution = {best_solution}, Best fitness = {best_fitness}")
    
    # Stop the algorithm if the optimal solution is found
    if best_fitness == total_supply * min([buyer["price"] for buyer in buyers.values()]):
        break

# Print the trades and the total profit
print("Trades:")
for buyer, seller, units in calculate_fitness(best_solution)[1]:
    print(f"Buyer {buyer} bought {units} units from Seller {seller}")
print(f"Total profit: {best_fitness}")
        
