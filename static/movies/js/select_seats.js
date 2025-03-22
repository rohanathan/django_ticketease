
document.addEventListener("DOMContentLoaded", function () {
    const confirmButton = document.getElementById("confirmSeatsBtn");
    const seatCounter = document.getElementById("seatCounter");
    const totalPriceElement = document.getElementById("totalPrice");
    const quantitySelect = document.getElementById("seatQuantity");

    const movieId = document.getElementById("seatContainer").dataset.movieId;
    const showtimeId = document.getElementById("seatContainer").dataset.showtimeId;

    let selectedSeats = new Set();
    let maxSeats = parseInt(quantitySelect.value);
    let totalPrice = 0;

    quantitySelect.addEventListener("change", () => {
        maxSeats = parseInt(quantitySelect.value);
        selectedSeats.clear();
        document.querySelectorAll(".seat-btn.selected").forEach(btn => btn.classList.remove("selected"));
        totalPrice = 0;
        updateUI();
    });

    document.querySelectorAll(".seat-btn").forEach(button => {
        if (button.disabled) return;

        button.addEventListener("click", function () {
            const seatId = this.dataset.seat;
            const seatPrice = parseFloat(this.dataset.price);

            if (selectedSeats.has(seatId)) {
                selectedSeats.delete(seatId);
                this.classList.remove("selected");
                totalPrice -= seatPrice;
            } else {
                if (selectedSeats.size < maxSeats) {
                    selectedSeats.add(seatId);
                    this.classList.add("selected");
                    totalPrice += seatPrice;
                } else {
                    alert(`You can only select up to ${maxSeats} seats.`);
                }
            }
            updateUI();
        });
    });

    function updateUI() {
        seatCounter.innerText = `Selected Seats: ${selectedSeats.size}`;
        totalPriceElement.innerText = totalPrice.toFixed(2);
        confirmButton.disabled = selectedSeats.size === 0;
    }

    window.confirmSeats = function () {
        if (selectedSeats.size === 0) {
            alert("Please select at least one seat.");
            return;
        }
        const seatList = Array.from(selectedSeats).join(",");
        window.location.href = `/bookings/${movieId}/showtime/${showtimeId}/confirm-booking/?seats=${seatList}&total=${totalPrice}`;
    };
});