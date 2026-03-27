fetch('http://127.0.0.1:8000/create-item/2', {
  method: "POST",
  body: JSON.stringify({
    name: "Egg",
    price: 30
  })
})
.then(response => console.log(response))