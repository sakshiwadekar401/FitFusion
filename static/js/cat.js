document.getElementById("recommendBtn").addEventListener("click", function () {
    // Get values from the form inputs
    const goal = document.getElementById("goal").value;
    const activity = document.getElementById("activity").value;
    const diet = document.getElementById("diet").value;

    // Variable to hold the recommendation
    let recommendation = "";

    // Basic recommendation logic based on selected goal, activity, and diet
    switch (goal) {
        case "weightLoss":
            recommendation += "For weight loss, focus on a calorie deficit diet with high protein and fiber. ";
            break;
        case "maintainWeight":
            recommendation += "To maintain your weight, balance calorie intake with your energy expenditure. ";
            break;
        case "muscleGain":
            recommendation += "To gain muscle, prioritize protein intake and eat in a slight calorie surplus. ";
            break;
        case "fatBurn":
            recommendation += "For fat burning with lean muscle retention, aim for high protein, low-carb diets. ";
            break;
        case "enhancePerformance":
            recommendation += "Enhancing performance requires a balanced diet rich in complex carbs and proteins. ";
            break;
        case "improveImmunity":
            recommendation += "To improve immunity, increase your intake of vitamins C, D, and zinc-rich foods. ";
            break;
        case "boneHealth":
            recommendation += "For bone health, focus on calcium and vitamin D-rich foods like leafy greens and dairy. ";
            break;
        case "gutHealth":
            recommendation += "For gut health, focus on fiber, prebiotic, and probiotic-rich foods. ";
            break;
        case "mentalWellness":
            recommendation += "Boost mental wellness with foods rich in omega-3, B-vitamins, and antioxidants. ";
            break;
        case "energyBoost":
            recommendation += "For an energy boost, focus on balanced carbs and proteins with nutrient-dense snacks. ";
            break;
        case "recovery":
            recommendation += "Post-recovery diets should be rich in proteins, vitamins, and anti-inflammatory foods. ";
            break;
        default:
            recommendation += "Choose a goal to tailor your diet recommendation. ";
            break;
    }

    // Activity level adjustment
    switch (activity) {
        case "sedentary":
            recommendation += "Since you're sedentary, try to limit calorie intake and focus on nutrient-dense foods. ";
            break;
        case "lightlyActive":
            recommendation += "Light activity means you should maintain a balanced intake of carbs, proteins, and fats. ";
            break;
        case "moderate":
            recommendation += "For moderate activity, increase your carb intake slightly to fuel your workouts. ";
            break;
        case "veryActive":
            recommendation += "With high activity levels, make sure you're getting enough calories, especially carbs. ";
            break;
        case "athlete":
            recommendation += "As an athlete, focus on high-calorie, protein-rich, and carb-heavy meals. Hydrate well. ";
            break;
        case "recoveryMode":
            recommendation += "In recovery mode, focus on nutrient-dense, anti-inflammatory, and high-protein meals. ";
            break;
        case "officeBound":
            recommendation += "Since you're office-bound, watch out for snacking and try to stay active when possible. ";
            break;
        default:
            recommendation += "Choose your activity level to get better advice. ";
            break;
    }

    // Dietary preferences adjustment
    switch (diet) {
        case "vegetarian":
            recommendation += "As a vegetarian, prioritize plant-based proteins like legumes, tofu, and quinoa. ";
            break;
        case "vegan":
            recommendation += "For vegans, make sure you're getting enough B12, iron, and omega-3 from plant sources. ";
            break;
        case "nonVegetarian":
            recommendation += "As a non-vegetarian, you can focus on lean meats, fish, and eggs for protein. ";
            break;
        case "highProtein":
            recommendation += "For a high-protein diet, prioritize lean meats, fish, eggs, and legumes. ";
            break;
        case "glutenFree":
            recommendation += "Gluten-free diets should focus on naturally gluten-free grains like rice and quinoa. ";
            break;
        case "dairyFree":
            recommendation += "For dairy-free diets, ensure you get calcium from fortified plant milks and leafy greens. ";
            break;
        case "lowCarb":
            recommendation += "Low-carb diets should focus on high-fat, high-protein foods while avoiding sugar. ";
            break;
        case "pescatarian":
            recommendation += "For pescatarians, include fatty fish like salmon for omega-3s and proteins. ";
            break;
        case "lowSodium":
            recommendation += "On a low-sodium diet, avoid processed foods and focus on fresh ingredients. ";
            break;
        case "highFiber":
            recommendation += "For high fiber, focus on whole grains, fruits, and vegetables. ";
            break;
        case "highCalcium":
            recommendation += "On a high-calcium diet, prioritize dairy products or fortified plant-based alternatives. ";
            break;
        case "antiInflammatory":
            recommendation += "Anti-inflammatory diets should include foods like berries, fatty fish, and turmeric. ";
            break;
        case "lowGI":
            recommendation += "For low-glycemic diets, choose whole grains, legumes, and leafy greens to stabilize blood sugar. ";
            break;
        default:
            recommendation += "Choose a dietary preference to tailor your diet plan. ";
            break;
    }

    // Display the recommendation in the 'recommendation' div
    const recommendationDiv = document.getElementById("recommendation");
    recommendationDiv.innerHTML = `<p>${recommendation}</p>`;
    recommendationDiv.style.display = "block"; // Make sure the div is visible
});
