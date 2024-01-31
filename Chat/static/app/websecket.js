const token = JSON.parse(localStorage.getItem("token"));
const userInfo = JSON.parse(localStorage.getItem("user_info"));
const socket = new WebSocket('ws://127.0.0.1:8000/ws/private_chat/{{username}}', "Token'" + token[0]);

const notification_socket = new WebSocket('ws://127.0.0.1:8000/ws/notification/', "Token'" + token[0]);

console.log(token[0])
// Send message when button is clicked
document.getElementById("send").addEventListener("click", () => {
    const message = document.getElementById("message").value;
    socket.send(JSON.stringify({
        message: message
    }));
});

// Receive messages from server
socket.addEventListener("message", event => {
    const msg = JSON.parse(event.data);
    if (msg.sender == userInfo.username) {
        document.getElementById("chat-messages").innerHTML +=
            `<p style="text-align:right;">${msg.message}</p>`;
    }
    else {
        document.getElementById("chat-messages").innerHTML +=
            `<p>${msg.message}</p>`;
    }
    console.log(msg)
    console.log(userInfo.username)

});
socket.onclose = function (e) {
    console.log("chat closed");

};
socket.addEventListener("open", (event) => {
    console.log("chat opened!")
});

notification_socket.addEventListener("open", (event) => {
    console.log("notification opened!")
});

notification_socket.onclose = function (e) {
    console.log("notifications closed");
    console.error(e)
};

notification_socket.addEventListener("message", event => {
    const msg = JSON.parse(event.data);
    console.log(`you have message from ${msg.username}`)
});
