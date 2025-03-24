document.addEventListener("DOMContentLoaded", function () {
    let count = 5;
    const countdownElement = document.getElementById("countdown");

    const interval = setInterval(() => {
        if (count > 1) {
            count--;
            countdownElement.innerText = count;
        } else {
            clearInterval(interval);
            window.location.href = window.loginRedirectURL;
        }
    }, 1000);
});
