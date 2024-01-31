function submitForm(event) {
    event.preventDefault();

    // Get form input values
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Create request body
    const data = {
        username: username,
        password: password
    };

    // Send POST request
    fetch("http://127.0.0.1:8000/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(responseData => {
            // Save data to local storage
            localStorage.setItem("user_info", JSON.stringify(responseData.user_info));
            localStorage.setItem("token", JSON.stringify(responseData.token));

            window.location.href = "http://127.0.0.1:8000/chat/test/";
        })
        .catch(error => {
            console.log(error);
        });
}