let data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
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
    
  } else {
    console.error(data.message);
  }
})
.catch(error => {
  console.error(error);
});

  