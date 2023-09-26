const test = document.querySelector("#test");

test.addEventListener("click", munresk());

function munresk() {
    
    let numBuyers = 2;
  let numSellers = 2;
  let demands = [10, 15];
  let supplies = [20, 10];
  let prices = [30, 35, 50, 40]; // Seller 1, Seller 2, Buyer 1, Buyer 2
  
  let result = findOptimalTrades(numBuyers, numSellers, demands, supplies, prices);
  console.log("Total profit: " + result.totalProfit);
  console.log("Trades:");
  for (let i = 0; i < result.trades.length; i++) {
    let trade = result.trades[i];
    console.log("Buyer " + trade.buyer + " purchased " + trade.quantity +
                " units of energy from Seller " + trade.seller);
  } 
} 