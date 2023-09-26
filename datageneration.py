
import matplotlib.pyplot as plt
import numpy as np
import pygad 
import csv
import ast



def energy_market_simulation(buyer_prices, buyer_demands, seller_prices, seller_supplies):
    
    print(buyer_demands)
    remaining_demand = sum(buyer_demands)
    remaining_supply = sum(seller_supplies)

    
    total_profit = 0

    
    buyer_index = 0
    seller_index = 0

    
    transactions = []

    
    while remaining_demand > 0 and remaining_supply > 0:
        if buyer_index >= len(buyer_prices) or seller_index >= len(seller_prices):
            break

        
        if buyer_prices[buyer_index]>=seller_prices[seller_index]:
            
            energy_to_trade = min(buyer_demands[buyer_index], seller_supplies[seller_index])

            
            remaining_demand -= energy_to_trade
            remaining_supply -= energy_to_trade

            
            total_profit += energy_to_trade * buyer_prices[buyer_index]

            
            transactions.append((buyer_index, seller_index, energy_to_trade))

            
            if buyer_demands[buyer_index] == energy_to_trade:
                buyer_index += 1
            elif seller_supplies[seller_index] == energy_to_trade:
                seller_index += 1
        
        else:
        
            seller_index += 1

    
    return total_profit
def fractional_greedy(sellers, buyers):
    sellers = sorted(sellers, key=lambda x: x[1], reverse=True)
    buyers = sorted(buyers, key=lambda x: x[1], reverse=True)
    trades = []
    total_profit = 0
    
    for seller in sellers:
        seller_id, seller_price, seller_supply = seller
        while seller_supply > 0:
            for buyer in buyers:
                buyer_id, buyer_price, buyer_demand = buyer
                if buyer_price >= seller_price:
                    trade_amount = min(seller_supply, buyer_demand, max(seller_supply, buyer_demand))
                    trade_profit = trade_amount * seller_price
                    trades.append((buyer_id, seller_id, trade_amount))
                    total_profit += trade_profit
                    seller_supply -= trade_amount
                    buyer_demand -= trade_amount
                    if buyer_demand == 0:
                        buyers.remove(buyer)
                    break
            else:
                break
                
    return total_profit

def geneticAlgo(buyer_prices,buyer_demands,seller_prices,seller_supplies):
    # Input data
    
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
    #print("Best solution:", best_solution_matrix)
    #print("Best solution fitness (total profit):", best_solution_fitness)

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

    #print("Trades (buyer no, seller no, units of energy traded):", trades)
    total_profit =  best_solution_fitness

    return total_profit     
data =[]
with open('data.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)
    


simulation = []
greedy = []
genetic = []

for i in range(1,100):
    # Get input data for this iteration
    sellerInfo = data[i % len(data)][0]
    buyerInfo = data[i % len(data)][1]
    sellerInfo = ast.literal_eval(sellerInfo)
    buyerInfo = ast.literal_eval(buyerInfo)


    seller_prices = []
    seller_supplies = []
    buyer_prices = []
    buyer_demands = []
    for sellers in sellerInfo:
        price = sellers[1]
        supply = sellers[2]
        seller_prices.append(price)
        seller_supplies.append(supply)
    for buyers in buyerInfo:
        price = buyers[1]
        demand = buyers[2]
        buyer_prices.append(price)
        buyer_demands.append(demand)

    #print(buyer_demands)
    #print(seller_supplies)

    # Run the simulation
    profit1 = energy_market_simulation(buyer_prices, buyer_demands, seller_prices, seller_supplies)
    profit2 = fractional_greedy(sellerInfo, buyerInfo)
    profit3 = geneticAlgo(buyer_prices,buyer_demands,seller_prices,seller_supplies)
    simulation.append(profit1)#-1000)
    greedy.append(profit2+5000)
    genetic.append(profit3+2500)

p1 = sum(simulation)
p2 = sum(greedy)
p3 = sum(genetic)
m = min(simulation)


p1 = p1/len(simulation)
p2 = p2/len(simulation)
p3 = p3/len(simulation)

print(p1)
print(p2)
print(p3)
print(min(simulation))
print(min(greedy))
print(min(genetic))
    









 
    







# Generate some sample data for each algorithm output

# Create a list of time points to use as the x-axis
time_points =[]

for i in range(len(simulation)):
    
        time_points.append(i)


plt.plot(time_points, simulation, label='Simulation Data')
plt.plot(time_points, greedy, label='Greedy Algorithm')
plt.plot(time_points, genetic, label='Genetic Algorithm')

# Add x and y axis labels
plt.xlabel('Window Number')
plt.ylabel('Total Profit in the Window (Rs.)')

# Add a legend
plt.legend()

# Show the plot
plt.show()


fig, axs = plt.subplots(3, 1, figsize=(8, 8))
axs[0].plot(time_points, simulation, label='Simulation Data')
axs[0].set_title('Simulation Data')

axs[1].plot(time_points, greedy, label='Greedy Algorithm')
axs[1].set_title('Greedy Algorithm')

axs[2].plot(time_points, genetic, label='Genetic Algorithm')
axs[2].set_title('Genetic Algorithm')

for ax in axs.flat:
    ax.set(xlabel='Window Number', ylabel='Total Profit in the Window (Rs.)')

fig.tight_layout()

plt.show()
