// Main JS file for the application

// Handle navbar button selection
document.addEventListener('DOMContentLoaded', function() {
    const navButtons = document.querySelectorAll('.base-nav-buttons > button');
    
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove 'selected' class from all buttons
            navButtons.forEach(btn => btn.classList.remove('selected'));
            
            // Add 'selected' class to the clicked button
            this.classList.add('selected');
        });
    });
});