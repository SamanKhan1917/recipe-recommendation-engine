document.getElementById("recommendButton").addEventListener("click", function() {
    const ingredients = document.getElementById("ingredients").value;
    fetch("http://localhost:8000/recommendations", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ ingredients: ingredients })
    })
    .then(response => response.json())
    .then(data => {
        const recipeList = document.getElementById("recipeList");
        recipeList.innerHTML = ""; // Clear previous results

        if (data.recipes.length > 0) {
            data.recipes.forEach(recipe => {
                const li = document.createElement("li");
                li.textContent = recipe; // Assume recipe is a string
                recipeList.appendChild(li);
            });
        } else {
            recipeList.innerHTML = "<li>No recipes found!</li>";
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
