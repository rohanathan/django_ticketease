document.addEventListener("DOMContentLoaded", function () {
    if (window.enableSuccessRedirect && window.redirectUrl) {
        let countdown = 5;
        const countdownElement = document.getElementById("countdown");

        const interval = setInterval(() => {
            countdown--;
            if (countdownElement) countdownElement.textContent = countdown;

            if (countdown <= 0) {
                clearInterval(interval);
                window.location.href = window.redirectUrl;
            }
        }, 1000);
    }
});
