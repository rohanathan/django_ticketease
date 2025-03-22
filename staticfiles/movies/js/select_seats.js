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

            const seatsByRow = {};

            data.seats.forEach(seat => {
                const rowKey = seat.row;
                if (!seatsByRow[rowKey]) {
                    seatsByRow[rowKey] = [];
                }
                seatsByRow[rowKey].push(seat);
            });
            
            // Sort rows in reverse alphabetical order (E to A)
            const sortedRows = Object.keys(seatsByRow).sort().reverse();
            
            seatContainer.innerHTML = ''; // Clear container
            
            sortedRows.forEach(row => {
                const rowDiv = document.createElement("div");
                rowDiv.classList.add("seat-row");
            
                seatsByRow[row].forEach(seat => {
                    let seatBtn = document.createElement("button");
                    seatBtn.innerText = seat.row + seat.number;
                    seatBtn.classList.add("seat-btn");
            
                    if (seat.is_booked) {
                        seatBtn.disabled = true;
                        seatBtn.classList.add("unavailable");
                    } else {
                        seatBtn.onclick = function () {
                            const seatId = seat.row + seat.number;
                            if (selectedSeats.has(seatId)) {
                                selectedSeats.delete(seatId);
                                this.classList.remove("selected");
                            } else {
                                if (selectedSeats.size < maxSeats) {
                                    selectedSeats.add(seatId);
                                    this.classList.add("selected");
                                } else {
                                    alert(`You can only select up to ${maxSeats} seats.`);
                                }
                            }
                            updateConfirmButton();
                        };
                    }
            
                    rowDiv.appendChild(seatBtn);
                });
            
                seatContainer.appendChild(rowDiv);
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
