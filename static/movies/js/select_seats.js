document.addEventListener("DOMContentLoaded", function () {
    const movieId = document.getElementById("seatContainer").dataset.movieId;
    const showtimeId = document.getElementById("seatContainer").dataset.showtimeId;
    const seatContainer = document.getElementById("seatContainer");
    const confirmButton = document.getElementById("confirmSeatsBtn");
    const seatCounter = document.getElementById("seatCounter");
    const quantitySelect = document.getElementById("seatQuantity");
    const totalPriceElement = document.getElementById("totalPrice");

    let selectedSeats = new Set();
    let maxSeats = 1; // Default quantity
    let totalPrice = 0;

    confirmButton.disabled = true; // Ensure confirm button is disabled initially

    // Fetch seat data from backend
    fetch(`/movies/${movieId}/showtime/${showtimeId}/get-seats/`)
        .then(response => response.json())
        .then(data => {
            seatContainer.innerHTML = ''; // Clear previous content

            let rowContainers = {};

            data.seats.forEach(seat => {
                let seatBtn = document.createElement("button");
                seatBtn.innerText = seat.row + seat.number;
                seatBtn.classList.add("seat-btn");

                // Add seat category class
                if (seat.seat_class === "Gold") {
                    seatBtn.classList.add("gold");
                    seatBtn.dataset.price = 15; // Gold Price
                } else {
                    seatBtn.classList.add("diamond");
                    seatBtn.dataset.price = 20; // Diamond Price
                }

                if (seat.is_booked) {
                    seatBtn.disabled = true;
                    seatBtn.classList.add("booked");
                } else {
                    seatBtn.onclick = function () {
                        const seatPrice = parseInt(seatBtn.dataset.price);

                        if (selectedSeats.has(seat.row + seat.number)) {
                            selectedSeats.delete(seat.row + seat.number);
                            this.classList.remove("selected");
                            totalPrice -= seatPrice;
                        } else {
                            if (selectedSeats.size < maxSeats) {
                                selectedSeats.add(seat.row + seat.number);
                                this.classList.add("selected");
                                totalPrice += seatPrice;
                            } else {
                                alert(`You can only select up to ${maxSeats} seats.`);
                            }
                        }
                        updateConfirmButton();
                    };
                }

                // Group seats by row
                if (!rowContainers[seat.row]) {
                    rowContainers[seat.row] = document.createElement("div");
                    rowContainers[seat.row].classList.add("seat-row");
                }
                rowContainers[seat.row].appendChild(seatBtn);
            });

            // Append rows in the correct order (screen at bottom)
            Object.keys(rowContainers).sort().forEach(row => {
                seatContainer.appendChild(rowContainers[row]);
            });
        })
        .catch(error => console.error("Error fetching seats:", error));

    // Update maxSeats when quantity is changed
    quantitySelect.addEventListener("change", function () {
        maxSeats = parseInt(this.value);
        selectedSeats.clear();
        document.querySelectorAll(".seat-btn.selected").forEach(btn => btn.classList.remove("selected"));
        totalPrice = 0;
        updateConfirmButton();
    });

    function updateConfirmButton() {
        seatCounter.innerText = `Selected Seats: ${selectedSeats.size}`;
        totalPriceElement.innerText = totalPrice.toFixed(2);
        confirmButton.disabled = selectedSeats.size === 0;
    }
});

function confirmSeats() {
    let selectedSeats = [...document.querySelectorAll(".seat-btn.selected")].map(btn => btn.innerText);
    if (selectedSeats.length === 0) return alert("Please select at least one seat!");

    window.location.href = `/bookings/${movieId}/showtime/${showtimeId}/confirm-booking/?seats=${selectedSeats.join(",")}&total=${totalPrice}`;
}
