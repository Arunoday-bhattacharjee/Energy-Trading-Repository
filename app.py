from flask import Flask, request, jsonify
from flask_cors import CORS
import pygad
import numpy as np

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])
@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    sellers = data['sellers']
    buyers = data['buyers']

    if data['algorithm']== 'greedy':
        
        seller_info =[]
        buyer_info = []


        for buyer in buyers:
            buyer_id = buyer['ID']
            buyer_price = buyer['price']
            buyer_demand = buyer['units']
            buyer_info.append((buyer_id, buyer_price, buyer_demand))
        
        for seller in sellers:
            
            seller_id = seller['ID']
            seller_price = seller['price']
            seller_supply = seller['units']
            seller_info.append((seller_id, seller_price, seller_supply))

        total_profit,trades = fractional_greedy(seller_info, buyer_info)
        

        
        # Process the data and get the result
        result = total_profit
        #print(trades)
        for trade in trades:
            print(f"Buyer: {trade[0]}, Seller: {trade[1]}, Amount: {trade[2]}")
        print(result)
        
        # Return the result as a JSON object
        return jsonify({'status': 'success', 'trades':trades, 'profit': total_profit})
    
    elif data['algorithm']== 'simulation':
        # Process the data and get the result
        buyer_price =[]
        buyer_demand = []
        seller_price = []
        seller_supply = []
        for buyer in buyers:
            buyer_price.append(buyer['price'])
            buyer_demand.append(buyer['units'])
        
        for seller in sellers:
            seller_price.append(seller['price'])
            seller_supply.append(seller['units'])
        
        #print (buyer_demand)
        total_profit,trades = energy_market_simulation(buyer_price, buyer_demand, seller_price, seller_supply)
        return jsonify({'status': 'success', 'trades': trades, 'profit': total_profit})
    
    elif data['algorithm'] == 'genetic':
        buyer_price =[]
        buyer_demand = []
        seller_price = []
        seller_supply = []
        for buyer in buyers:
            buyer_price.append(buyer['price'])
            buyer_demand.append(buyer['units'])
        
        for seller in sellers:
            seller_price.append(seller['price'])
            seller_supply.append(seller['units'])
        
        
        total_profit,trades = geneticAlgo(buyer_price, buyer_demand, seller_price, seller_supply)
        return jsonify({'status': 'success', 'trades': trades, 'profit': total_profit})

    

    

         
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
                
    return total_profit, trades

def energy_market_simulation(buyer_prices, buyer_demands, seller_prices, seller_supplies):
    
    
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

            
            transactions.append((buyer_index+1, seller_index+1, energy_to_trade))

            
            if buyer_demands[buyer_index] == energy_to_trade:
                buyer_index += 1
            elif seller_supplies[seller_index] == energy_to_trade:
                seller_index += 1
        
        else:
        
            seller_index += 1

    
    return total_profit, transactions

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

    return total_profit,trades

    
if __name__ == '__main__':
    app.run(debug=True)


