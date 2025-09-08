// modal.js

function openModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "block";
    } else {
        console.error("[modal.js] No modal found with ID: " + modalId);
    }
}
function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "none";
    } else {
        console.error("[modal.js] No modal found with ID: " + modalId);
    }
}

// Support detecting the modal to close from button
function closeParentModal(button) {
    var modal = button.parentElement.parentElement.id; // escape two levels to get modal id
    console.log("[modal.js] Parent of button " + button + " is " + button.parentElement.parentElement + " with id " + modal);
    closeModal(modal);
}