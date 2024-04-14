document.addEventListener("DOMContentLoaded", function() {
    // JavaScript code to interact with HTML forms
    const loginForm = document.querySelector("form");
    loginForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(loginForm);
        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.success) {
                window.location.href = '/dashboard';
            } else {
                alert("Login failed!");
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
