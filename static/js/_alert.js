document.addEventListener('DOMContentLoaded', function() {
    // Function to hide alerts, validation messages and red borders after 2 seconds
    function hideMessages() {
        setTimeout(() => {
            document.querySelectorAll('#alert-message').forEach(alert => {
                alert.classList.remove('d-flex', 'align-items-center');
                alert.classList.add('d-none');
            });

            document.querySelectorAll('.is-invalid').forEach(input => {
                input.classList.remove('is-invalid');
            });

            document.querySelectorAll('.invalid-feedback').forEach(feedback => {
                feedback.style.display = 'none';
            });
        }, 5000);
    }

    // Hide messages when the page is loaded
    hideMessages();
});