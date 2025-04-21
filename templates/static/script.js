// Example: Basic client-side form validation
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (e) {
        const name = form.name.value.trim();
        const phone = form.phone.value.trim();
        const vehicle_number = form.vehicle_number.value.trim();
        const vehicle_model = form.vehicle_model.value.trim();

        if (!name || !phone || !vehicle_number || !vehicle_model) {
            alert("Please fill in all fields!");
            e.preventDefault(); // Prevent form submission
        }
    });
});
