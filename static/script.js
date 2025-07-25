// Utility to get an element by ID with null check
const getById = (id) => document.getElementById(id);

// Validate the form before submission
function validateForm() {
    const symptom = getById("symptom")?.value;
    if (!symptom) {
        alert("Please select a symptom to continue.");
        return false;
    }
    return true;
}

// Show a loading message (e.g., spinner or message)
function showLoadingMessage() {
    const loadingDiv = getById("loading");
    if (loadingDiv) {
        loadingDiv.style.display = "block";
        loadingDiv.innerText = "Processing your input, please wait...";
    }
}

// Suggest medicine based on selected symptom
function updateMedicineSuggestion() {
    const symptom = getById("symptom")?.value;
    const medicineBox = getById("medicineBox");

    if (!medicineBox) {
        console.warn("Medicine box element not found.");
        return;
    }

    const suggestions = {
        "Fever": "Paracetamol, Ibuprofen",
        "Cold": "Cetirizine, Steam Inhalation",
        "Cough": "Cough Syrup, Warm Honey with Lemon",
        "Headache": "Aspirin, Proper Sleep, Hydration",
        "Stomach Pain": "Antacids, ORS, Light Meals",
        "Vomiting": "Ondansetron, Hydration Therapy",
        "Motions": "ORS, Probiotics, Banana"
    };

    if (suggestions[symptom]) {
        medicineBox.innerHTML = `<strong>Suggested Medicines:</strong> ${suggestions[symptom]}`;
        medicineBox.style.display = "block";
    } else {
        medicineBox.innerHTML = "";
        medicineBox.style.display = "none";
    }
}

// Event listeners setup
document.addEventListener("DOMContentLoaded", () => {
    const form = getById("symptomForm");
    const symptomDropdown = getById("symptom");

    if (form) {
        form.addEventListener("submit", (event) => {
            if (!validateForm()) {
                event.preventDefault();
            } else {
                showLoadingMessage();
            }
        });
    }

    if (symptomDropdown) {
        symptomDropdown.addEventListener("change", updateMedicineSuggestion);
    }
});
