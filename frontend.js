const vendorCountForm = document.querySelector('#vendor-count-form');
const buyers = [];
const sellers = [];

vendorCountForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const buyerCount = parseInt(document.getElementById('buyer-count').value);
  const sellerCount = parseInt(document.getElementById('seller-count').value);
  //console.log(buyerCount);
  //console.log(sellerCount);
  if(buyerCount>0 || sellerCount>0){
      vendorCountForm.remove();
      const vendorDetailsForm = document.createElement('form');
      vendorDetailsForm.id = 'vendor-details-form';
      for(let i=1; i<=buyerCount; i++){
          const buyerLabel = document.createElement('label');
          buyerLabel.textContent = `Buyer ${i} (Price):`;
          const buyerInput = document.createElement('input');
          buyerInput.type = 'number';
          buyerInput.id = `buyer-input-${i}`;
          buyerInput.style.marginRight = '50px';
          buyerInput.style.marginBottom = '50px'; 
          const buyerUnitsLabel = document.createElement('label');
          buyerUnitsLabel.textContent = `Buyer ${i} (No of Units):`;
          const buyerUnitsInput = document.createElement('input');
          buyerUnitsInput.type = 'number';
          buyerUnitsInput.id = `buyer-units-${i}`;
          buyerUnitsInput.style.marginRight = '50px';
          buyerUnitsInput.style.marginBottom = '50px'; 
          vendorDetailsForm.appendChild(buyerLabel);
          vendorDetailsForm.appendChild(buyerInput);
          vendorDetailsForm.appendChild(buyerUnitsLabel);
          vendorDetailsForm.appendChild(buyerUnitsInput);


          
          
          vendorDetailsForm.appendChild(document.createElement('br'));
        }
        for(let i=1; i<=sellerCount; i++){
          const sellerLabel = document.createElement('label');
          sellerLabel.textContent = `Seller ${i} (Price):`;
          const sellerInput = document.createElement('input');
          sellerInput.type = 'number';
          sellerInput.id = `seller-input-${i}`;
          const sellerUnitsLabel = document.createElement('label');
          sellerInput.style.marginRight = '50px';
          sellerInput.style.marginBottom = '50px'; 
          sellerUnitsLabel.textContent = `Seller ${i} (No of Units):`;
          const sellerUnitsInput = document.createElement('input');
          sellerUnitsInput.type = 'number';
          sellerUnitsInput.id = `seller-units-${i}`;
          sellerUnitsInput.style.marginRight = '50px';
          sellerUnitsInput.style.marginBottom = '50px';
          vendorDetailsForm.appendChild(sellerLabel);
          vendorDetailsForm.appendChild(sellerInput);
          vendorDetailsForm.appendChild(sellerUnitsLabel);
          vendorDetailsForm.appendChild(sellerUnitsInput);
          vendorDetailsForm.appendChild(document.createElement('br'));
        }
        
        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.textContent = 'Save';
        submitButton.classList.add = "waves-effect waves-light btn btn-floating pulse";
        vendorDetailsForm.appendChild(submitButton);

        


        const formContainer = document.getElementById('form-container');
        formContainer.appendChild(vendorDetailsForm);

        vendorDetailsForm.addEventListener('submit', (event) => {
          event.preventDefault();

          
          for(let i=1; i<=sellerCount; i++){
            const seller ={
              ID: i,
              price: parseInt(document.getElementById(`seller-input-${i}`).value),
              units: parseInt(document.getElementById(`seller-units-${i}`).value)
            };
            sellers.push(seller);
          }
          
          for(let i=1; i<=buyerCount; i++){

            const buyer ={
              ID: i,
              price: parseInt(document.getElementById(`buyer-input-${i}`).value),
              units: parseInt(document.getElementById(`buyer-units-${i}`).value)
            };
            buyers.push(buyer);
          }
          console.log(buyers);
          console.log(sellers);
          if(buyers.length>0 || sellers.length>0){
            
            vendorDetailsForm.remove();
            const algorithmSelector = document.createElement('form');
            algorithmSelector.id = 'algorithm-selector';
            const algorithmLabel = document.createElement('label');
            algorithmLabel.textContent = 'Select Algorithm';

            const algorithm1 = document.createElement('input');
            algorithm1.setAttribute("id", "genetic-algorithm");
            algorithm1.setAttribute("type", "radio");
            algorithm1.setAttribute("value", "genetic-algorithm");
            algorithm1.setAttribute("name", "algorithm");
            const algorithm1Label = document.createElement('label');
            algorithm1Label.textContent = 'Genetic Algorithm';

            const algorithm2 = document.createElement('input');
            algorithm2.setAttribute("id", "greedy-algorithm");
            algorithm2.setAttribute("type", "radio");
            algorithm2.setAttribute("value", "greedy-algorithm");
            algorithm2.setAttribute("name", "algorithm");
            const algorithm2Label = document.createElement('label');
            algorithm2Label.textContent = 'Greedy Algorithm';
            const algorithm3 = document.createElement('INPUT');
            algorithm3.setAttribute("id", "simulation");
            algorithm3.setAttribute("type", "radio");
            algorithm3.setAttribute("value", "simulation");
            algorithm3.setAttribute("name", "algorithm");
            const algorithm3Label = document.createElement('label');
            algorithm3Label.textContent = 'Simulation';
            const submitButton = document.createElement('button');
            submitButton.type = 'submit';
            submitButton.textContent = 'Submit';

            algorithmSelector.appendChild(algorithmLabel);
            //add line break
            algorithmSelector.appendChild(document.createElement('br'));
            algorithmSelector.appendChild(algorithm1);
            algorithmSelector.appendChild(algorithm1Label);
            //add line break
            algorithmSelector.appendChild(document.createElement('br'));
            algorithmSelector.appendChild(algorithm2);
            algorithmSelector.appendChild(algorithm2Label);
            //add line break
            algorithmSelector.appendChild(document.createElement('br'));
            algorithmSelector.appendChild(algorithm3);
            algorithmSelector.appendChild(algorithm3Label);
            //add line break
            algorithmSelector.appendChild(document.createElement('br'));
            algorithmSelector.appendChild(submitButton);
            formContainer.appendChild(algorithmSelector);

            
            algorithmSelector.addEventListener('submit', (event) => {
              event.preventDefault();
              const algorithm = document.querySelector('input[name="algorithm"]:checked').value;
              
              if(algorithm === 'genetic-algorithm'){
                algorithmSelector.remove();
                geneticAlgorithm('genetic');
                
              }
              else if(algorithm === 'greedy-algorithm'){
                algorithmSelector.remove();
                greedyAlgorithm('greedy');
                

      

              }
              else if(algorithm === 'simulation'){
                algorithmSelector.remove();
                simulation('simulation');
              

              }
            }
            );
            
            function geneticAlgorithm(algo){
              const data = {
                sellers: sellers,
                buyers: buyers,
                algorithm: algo
              }
              console.log(data);
            fetch('http://127.0.0.1:5000/process_data', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                  'Content-Type': 'application/json'
                  }
              })
                .then(response => response.json())
                .then(data => {
                  if (data.status === "success") {
                    console.log(data);
                    const profitElem = document.createElement('p');
                    profitElem.textContent = `Profit (Rs.):${data.profit}`;
                    const linebreaker = document.createElement('br');
                    
                    const trades = data.trades; // extract trades data from response 
                    const tradesDiv = document.createElement('div');
                    for (let i = 0; i < trades.length; i++) {
                      const tradeElem = document.createElement('p');
                      const trade = trades[i];
                      tradeElem.textContent = `Buyer: ${trade[0]}, Seller: ${trade[1]}, Amount (in units of Energy): ${trade[2]}`;
                      tradesDiv.appendChild(tradeElem);
                      tradesDiv.appendChild(linebreaker);
                    }

                    const tradeLabel = document.createElement('p');
                    tradeLabel.innerHTML="Trades"
                    tradeLabel.style.fontSize = "40px";
                    formContainer.appendChild(profitElem);
                    formContainer.appendChild(linebreaker);
                    formContainer.appendChild(tradeLabel);
                    formContainer.appendChild(linebreaker);
                    formContainer.appendChild(tradesDiv);

                                  
                    
                  }
                })

              
              
            }
            
            function greedyAlgorithm(algo){
              const data = {
                sellers: sellers,
                buyers: buyers,
                algorithm: algo
              }
              console.log(data);
            fetch('http://127.0.0.1:5000/process_data', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                  'Content-Type': 'application/json'
                  }
              })
                .then(response => response.json())
                .then(data => {
                  if (data.status === "success") {
                    console.log(data);
                    const profitElem = document.createElement('p');
                    profitElem.textContent = `Profit (Rs.):${data.profit}`;
                    const linebreaker = document.createElement('br');
                    
                    const trades = data.trades; // extract trades data from response 
                    const tradesDiv = document.createElement('div');
                    for (let i = 0; i < trades.length; i++) {
                      const tradeElem = document.createElement('p');
                      const trade = trades[i];
                      tradeElem.textContent = `Buyer: ${trade[0]}, Seller: ${trade[1]}, Amount (in units of energy traded): ${trade[2]}`;
                      tradesDiv.appendChild(tradeElem);
                      tradesDiv.appendChild(linebreaker);
                    }

                    const tradeLabel = document.createElement('p');
                    tradeLabel.innerHTML="Trades"
                    tradeLabel.style.fontSize = "40px";
                    formContainer.appendChild(profitElem);
                    formContainer.appendChild(linebreaker);
                    formContainer.appendChild(tradeLabel);
                    formContainer.appendChild(linebreaker);
                    formContainer.appendChild(tradesDiv);

                                  
                    
                  }
                })
                  
            }
            function simulation(algo){
              const data = {
                sellers: sellers,
                buyers: buyers,
                algorithm: algo
              }
              console.log(data);
            fetch('http://127.0.0.1:5000/process_data', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                  'Content-Type': 'application/json'
                  }
              })
                .then(response => response.json())
                .then(data => {
                  if (data.status === "success") {
                    console.log(data);

                    const profitElem = document.createElement('p');
                    profitElem.textContent = `Profit:${data.profit}`;
                    const linebreaker = document.createElement('br');
                    
                    const trades = data.trades; // extract trades data from response 
                    const tradesDiv = document.createElement('div');
                    for (let i = 0; i < trades.length; i++) {
                      const tradeElem = document.createElement('p');
                      const trade = trades[i];
                      tradeElem.textContent = `Buyer: ${trade[0]}, Seller: ${trade[1]}, Amount: ${trade[2]}`;
                      tradesDiv.appendChild(tradeElem);
                      tradesDiv.appendChild(linebreaker);
                    }

                    const tradeLabel = document.createElement('p');
                    tradeLabel.innerHTML="Trades:"
                    tradeLabel.style.fontSize = "40px";
                    formContainer.appendChild(profitElem);
                    formContainer.appendChild(linebreaker);
                    formContainer.appendChild(tradeLabel);
                    
                    formContainer.appendChild(tradesDiv);

                                  
                    
                  }
                })
              
            }
            
          }
        });
  }
});





