document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const userName = urlParams.get("user");
    const lineNumber = urlParams.get("number");

    if (userName && lineNumber) {
        const userSpan = document.getElementById("user");
        const numberSpan = document.getElementById("number");
        const actionSpan = document.getElementById("action");

        userSpan.textContent = userName;
        numberSpan.textContent = lineNumber;

        // You can determine the action based on your application's logic
        actionSpan.textContent = "collect"; // Replace with appropriate action

        // For example, you might want to change the action based on some criteria
        // if (lineNumber <= 10) {
        //     actionSpan.textContent = "consult";
        // } else {
        //     actionSpan.textContent = "collect";
        // }
    }
});
