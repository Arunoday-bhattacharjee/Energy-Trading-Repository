import random

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


total_energy = random.randint(1, 100)


num_sellers = 5
seller_supplies = [random.randint(1, total_energy) for i in range(num_sellers)]
seller_prices = [random.randint(10, 50) for i in range(num_sellers)]
sellers = [('Seller'+str(i), seller_supplies[i], seller_prices[i]) for i in range(num_sellers)]


num_buyers = 5
buyer_demands = [random.randint(1, total_energy) for i in range(num_buyers)]
buyer_prices = [random.randint(10, 50) for i in range(num_buyers)]
buyers = [('Buyer'+str(i), buyer_demands[i], buyer_prices[i]) for i in range(num_buyers)]


total_supply = sum(seller_supplies)
total_demand = sum(buyer_demands)
if total_supply != total_demand:
    diff = abs(total_supply - total_demand)
    
    if total_supply > total_demand:
        seller_index = random.randint(0, num_sellers-1)
        sellers[seller_index] = (sellers[seller_index][0], sellers[seller_index][1]-diff, sellers[seller_index][2])
        total_supply -= diff
    
    else:
        buyer_index = random.randint(0, num_buyers-1)
        buyers[buyer_index] = (buyers[buyer_index][0], buyers[buyer_index][1]+diff, buyers[buyer_index][2])
        total_demand -= diff

print("Sellers:", sellers)
print("Buyers:", buyers)
print("Total supply:", total_supply)
print("Total demand:", total_demand)


total_profit, trades = fractional_greedy(sellers, buyers)


print("Total profit:", total_profit)
print("Trades:")
for trade in trades:
    print(f"Buyer: {trade[0]}, Seller: {trade[1]}, Amount: {trade[2]}")
