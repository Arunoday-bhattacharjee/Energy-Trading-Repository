function fractional_greedy(sellers, buyers) {
  sellers = sellers.sort((a, b) => b[1] - a[1]);
  buyers = buyers.sort((a, b) => b[1] - a[1]);
  const trades = [];
  let total_profit = 0;

  for (const seller of sellers) {
    let [seller_id, seller_price, seller_supply] = seller;
    while (seller_supply > 0) {
      for (const buyer of buyers) {
        let [buyer_id, buyer_price, buyer_demand] = buyer;
        if (buyer_price >= seller_price) {
          const trade_amount = Math.min(seller_supply, buyer_demand, Math.max(seller_supply, buyer_demand));
          const trade_profit = trade_amount * seller_price;
          trades.push([buyer_id, seller_id, trade_amount]);
          total_profit += trade_profit;
          seller_supply -= trade_amount;
          buyer_demand -= trade_amount;
          if (buyer_demand === 0) {
            buyers.splice(buyers.indexOf(buyer), 1);
          }
          break;
        }
      }
    }
  }

  return [total_profit, trades];
}

const total_energy = Math.floor(Math.random() * 100) + 1;


const num_sellers = 5;
const seller_supplies = Array.from({ length: num_sellers }, () => Math.floor(Math.random() * total_energy) + 1);
const seller_prices = Array.from({ length: num_sellers }, () => Math.floor(Math.random() * 41) + 10);
const sellers = Array.from({ length: num_sellers }, (_, i) => [`Seller${i}`, seller_prices[i], seller_supplies[i]]);

const num_buyers = 5;
const buyer_demands = Array.from({ length: num_buyers }, () => Math.floor(Math.random() * total_energy) + 1);
const buyer_prices = Array.from({ length: num_buyers }, () => Math.floor(Math.random() * 41) + 10);
const buyers = Array.from({ length: num_buyers }, (_, i) => [`Buyer${i}`, buyer_prices[i], buyer_demands[i]]);

const total_supply = seller_supplies.reduce((a, b) => a + b, 0);
const total_demand = buyer_demands.reduce((a, b) => a + b, 0);
if (total_supply !== total_demand) {
  const diff = Math.abs(total_supply - total_demand);

  if (total_supply > total_demand) {
    const seller_index = Math.floor(Math.random() * num_sellers);
    sellers[seller_index][1] -= diff;
    total_supply -= diff;
  } else {
    const buyer_index = Math.floor(Math.random() * num_buyers);
    buyers[buyer_index][1] += diff;
    total_demand += diff;
  }
}

console.log("Sellers:", sellers);
console.log("Buyers:", buyers);
console.log("Total supply:", total_supply);
console.log("Total demand:", total_demand);

const [total_profit, trades] = fractional_greedy(sellers, buyers);

console.log("Total profit:", total_profit);
console.log("Trades:");
for (const trade of trades) {
  console.log(`Buyer: ${trade[0]}, Seller: ${trade[1]}, Amount: ${trade[2]}`);
}