import pygad
import numpy as np

def geneticAlgo():
    # Input data
    buyer_prices = [1,61,61,41,112]  # Replace with your buyer prices
    buyer_demands = [1,51,71,41,115]       # Replace with your buyer demands
    seller_prices = [13,6,5,6,12]   # Replace with your seller prices
    seller_supplies = [2,1,91,91,314]     # Replace with your seller supplies

    num_buyers = len(buyer_prices)
    num_sellers = len(seller_prices)

    # Fitness function
    def fitness_func(ga_instance, solution, solution_idx):
        trades = []
        total_profit = 0
        solution_matrix = np.reshape(solution, (num_sellers, num_buyers))

        for buyer_idx, buyer_demand in enumerate(buyer_demands):
            for seller_idx, seller_supply in enumerate(seller_supplies):
                trade_units = min(buyer_demand, seller_supply, solution_matrix[seller_idx][buyer_idx])
                trade_price = solution_matrix[seller_idx][buyer_idx]
                if trade_units > 0 and buyer_prices[buyer_idx] >= trade_price >= seller_prices[seller_idx]:
                    trades.append((buyer_idx, seller_idx, trade_units))
                    total_profit += trade_units * trade_price
                    buyer_demand -= trade_units
                    seller_supply -= trade_units

        return total_profit

    # Create the initial population outside of PyGAD
    num_solutions = 50
    initial_population = np.random.randint(low=min(seller_prices), high=max(buyer_prices)+1, size=(num_solutions, num_sellers, num_buyers))
    initial_population_flat = initial_population.reshape((num_solutions, num_sellers * num_buyers))

    # Genetic Algorithm parameters
    num_generations = 500

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=6,
        fitness_func=fitness_func,
        sol_per_pop=70,
        num_genes=num_sellers * num_buyers,
        init_range_low=min(seller_prices),
        init_range_high=max(buyer_prices)+1,
        mutation_percent_genes=7,
        parent_selection_type="rws",
        keep_parents=1,
        crossover_type="single_point",
        mutation_type="random",
        initial_population=initial_population_flat  # Pass the initial population directly
    )

    # Run the genetic algorithm
    ga_instance.run()

    # Get the best solution
    best_solution, best_solution_fitness, best_solution_idx = ga_instance.best_solution()
    best_solution_matrix = np.reshape(best_solution, (num_sellers, num_buyers))
    print("Best solution:", best_solution_matrix)
    print("Best solution fitness (total profit):", best_solution_fitness)

    # Extract trades from the best solution
    trades = []
    for buyer_idx, buyer_demand in enumerate(buyer_demands):
        for seller_idx, seller_supply in enumerate(seller_supplies):
            trade_units = min(buyer_demand, seller_supply, best_solution_matrix[seller_idx][buyer_idx])
            trade_price = best_solution_matrix[seller_idx][buyer_idx]
            if trade_units > 0 and buyer_prices[buyer_idx] >= trade_price >= seller_prices[seller_idx]:
                trades.append((buyer_idx, seller_idx, int(trade_units)))
                buyer_demand -= trade_units
                seller_supply -= trade_units

    print("Trades (buyer no, seller no, units of energy traded):", trades)
    
geneticAlgo() 



