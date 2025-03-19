// /* document.addEventListener("DOMContentLoaded", function() {
//     const movieId = document.getElementById("seatContainer").dataset.movieId;
//     const showtimeId = document.getElementById("seatContainer").dataset.showtimeId;
//     const seatContainer = document.getElementById("seatContainer");
//     const confirmButton = document.getElementById("confirmSeatsBtn");

//     confirmButton.disabled = true; // Ensure confirm button is disabled initially

//     fetch(`/movies/${movieId}/showtime/${showtimeId}/get-seats/`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error("Failed to load seat data");
//             }
//             return response.json();
//         })
//         .then(data => {
//             seatContainer.innerHTML = ''; // Clear previous content

//             data.seats.forEach(seat => {
//                 let seatBtn = document.createElement("button");
//                 seatBtn.innerText = seat.row + seat.number;
//                 seatBtn.classList.add("seat-btn");

//                 if (seat.is_booked) {
//                     seatBtn.disabled = true;
//                     seatBtn.classList.add("unavailable");
//                 } else {
//                     seatBtn.onclick = function() {
//                         this.classList.toggle("selected");
//                         updateConfirmButton();
//                     };
//                 }

//                 seatContainer.appendChild(seatBtn);
//             });
//         })
//         .catch(error => {
//             console.error("Error fetching seats:", error);
//             seatContainer.innerHTML = "<p class='text-danger'>Error loading seats. Please try again later.</p>";
//         });

//     function updateConfirmButton() {
//         let selectedSeats = document.querySelectorAll(".seat-btn.selected").length;
//         confirmButton.disabled = selectedSeats === 0;
//     }
// });

// function confirmSeats() {
//     let selectedSeats = [];
//     document.querySelectorAll(".seat-btn.selected").forEach(btn => {
//         selectedSeats.push(btn.innerText);
//     });

//     if (selectedSeats.length === 0) {
//         alert("Please select at least one seat!");
//         return;
//     }

//     // Redirect to booking confirmation page
//     const movieId = document.getElementById("seatContainer").dataset.movieId;
//     const showtimeId = document.getElementById("seatContainer").dataset.showtimeId;
//     window.location.href = `/movies/${movieId}/showtime/${showtimeId}/confirm-booking/?seats=${selectedSeats.join(",")}`;
// }
//  */


// document.addEventListener("DOMContentLoaded", function() {
//     const movieId = document.getElementById("seatContainer").dataset.movieId;
//     const showtimeId = document.getElementById("seatContainer").dataset.showtimeId;
//     const seatContainer = document.getElementById("seatContainer");
//     const confirmButton = document.getElementById("confirmSeatsBtn");
//     const seatCounter = document.getElementById("seatCounter");
//     const quantitySelect = document.getElementById("seatQuantity");

//     let selectedSeats = new Set();
//     let maxSeats = 1; // Default quantity

//     confirmButton.disabled = true; // Ensure confirm button is disabled initially

//     // Fetch seat data from backend
//     fetch(`/movies/${movieId}/showtime/${showtimeId}/get-seats/`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error("Failed to load seat data");
//             }
//             return response.json();
//         })
//         .then(data => {
//             seatContainer.innerHTML = ''; // Clear previous content

//             data.seats.forEach(seat => {
//                 let seatBtn = document.createElement("button");
//                 seatBtn.innerText = seat.row + seat.number;
//                 seatBtn.classList.add("seat-btn");

//                 if (seat.is_booked) {
//                     seatBtn.disabled = true;
//                     seatBtn.classList.add("unavailable");
//                 } else {
//                     seatBtn.onclick = function() {
//                         if (selectedSeats.has(seat.row + seat.number)) {
//                             selectedSeats.delete(seat.row + seat.number);
//                             this.classList.remove("selected");
//                         } else {
//                             if (selectedSeats.size < maxSeats) {
//                                 selectedSeats.add(seat.row + seat.number);
//                                 this.classList.add("selected");
//                             } else {
//                                 alert(`You can only select up to ${maxSeats} seats.`);
//                             }
//                         }
//                         updateConfirmButton();
//                     };
//                 }

//                 seatContainer.appendChild(seatBtn);
//             });
//         })
//         .catch(error => {
//             console.error("Error fetching seats:", error);
//             seatContainer.innerHTML = "<p class='text-danger'>Error loading seats. Please try again later.</p>";
//         });

//     // Update maxSeats when quantity is changed
//     quantitySelect.addEventListener("change", function() {
//         maxSeats = parseInt(this.value);
//         selectedSeats.clear();
//         document.querySelectorAll(".seat-btn.selected").forEach(btn => btn.classList.remove("selected"));
//         updateConfirmButton();
//     });

//     function updateConfirmButton() {
//         let count = selectedSeats.size;
//         seatCounter.innerText = `Selected Seats: ${count}`;
//         confirmButton.innerText = count > 0 ? `Confirm Selection (${count} Seats)` : "Confirm Selection";
//         confirmButton.disabled = count === 0;
//     }
// });

// function confirmSeats() {
//     let selectedSeats = Array.from(document.querySelectorAll(".seat-btn.selected")).map(btn => btn.innerText);

//     if (selectedSeats.length === 0) {
//         alert("Please select at least one seat!");
//         return;
//     }

//     const movieId = document.getElementById("seatContainer").dataset.movieId;
//     const showtimeId = document.getElementById("seatContainer").dataset.showtimeId;
//     window.location.href = `/bookings/${movieId}/showtime/${showtimeId}/confirm-booking/?seats=${selectedSeats.join(",")}`;
// }

document.addEventListener("DOMContentLoaded", function () {
    const seatContainer = document.getElementById("seatContainer");
    const seatQuantity = document.getElementById("seatQuantity");
    const confirmBtn = document.getElementById("confirmSeatsBtn");

    // Get Movie and Showtime IDs correctly
    const movieId = seatContainer.dataset.movieId;
    const showtimeId = seatContainer.dataset.showtimeId;

    console.log("🎬 Loaded seat selection page for Movie:", movieId, "Showtime:", showtimeId);

    // Enable button when a valid seat count is selected
    seatQuantity.addEventListener("change", function () {
        if (seatQuantity.value !== "") {
            confirmBtn.disabled = false;
            console.log("Seat count selected:", seatQuantity.value);
        }
    });

    // Redirect to confirm booking page on button click
    confirmBtn.addEventListener("click", function () {
        const seatCount = seatQuantity.value;
        console.log("🔗 Redirecting to confirmation with seat count:", seatCount);
        window.location.href = `/movies/${movieId}/showtime/${showtimeId}/confirm-booking/?seats=${seatCount}`;
    });
});
