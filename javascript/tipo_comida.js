let foodTypes = ['Al Paso', 'Alemana', 'Árabe', 'Argentina', 'Asiática', 'Australiana', 'Brasileña', 'Café y Snacks', 'Carnes', 'Casera', 'Chilena', 'China', 'Cocina de Autor', 'Comida Rápida', 'Completos', 'Coreana', 'Cubana', 'Española', 'Exótica', 'Francesa', 'Gringa', 'Hamburguesa', 'Helados', 'India', 'Internacional', 'Italiana', 'Latinoamericana', 'Mediterránea', 'Mexicana', 'Nikkei', 'Parrillada', 'Peruana', 'Pescados y mariscos', 'Picoteos', 'Pizzas', 'Pollos y Pavos', 'Saludable', 'Sándwiches', 'Suiza', 'Japonesa', 'Sushi', 'Tapas', 'Thai', 'Vegana', 'Vegetariana'];
let foodTypesHTML = document.getElementById("tipo-comida");
let foodTypesInit = false;

function loadFoodTypes() {
     if (!foodTypesInit) {
        for (let i = 0; i < foodTypes.length; i++) {
            let option = document.createElement("option");
            option.value = foodTypes[i];
            option.innerText = foodTypes[i];
            foodTypesHTML.appendChild(option);
        }
        foodTypesInit = true;
     }
} 