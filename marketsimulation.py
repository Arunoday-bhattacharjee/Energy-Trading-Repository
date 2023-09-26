import random
import csv


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

    
    return total_profit, transactions




buyer_prices = [random.randint(10, 20) for i in range(5)]
buyer_demands = [random.randint(10, 20) for i in range(5)]
seller_prices = [random.randint(5, 15) for i in range(5)]
seller_supplies = [random.randint(10, 20) for i in range(5)]

print("buyer prices: ",buyer_prices)
print("buyer demands: ",buyer_demands)
print("seller prices: ",seller_prices)
print("seller supplies: ",seller_supplies)

total_profit, transactions = energy_market_simulation(buyer_prices, buyer_demands, seller_prices, seller_supplies)

print("Total profit:", total_profit)
print("Transactions:", transactions)

buyer_prices = ','.join(map(str, buyer_prices))
buyer_demands = ','.join(map(str, buyer_demands))
seller_prices = ','.join(map(str, seller_prices))
seller_supplies = ','.join(map(str, seller_supplies))
new_row = [buyer_prices,buyer_demands,seller_prices,seller_supplies,total_profit]










