document.addEventListener("DOMContentLoaded", function () {
    if (window.removeLoginAlerts) {
        setTimeout(() => {
            document.querySelectorAll('.alert').forEach(alert => alert.remove());
        }, 3000);
    }
});
