document.addEventListener("DOMContentLoaded", function () {
    const movieId = document.getElementById("movieDetailContainer").dataset.movieId;
    const dateButtons = document.querySelectorAll(".date-btn");
    const showtimeContainer = document.getElementById("showtimeContainer");

    let selectedDate = "";

    // ✅ Handle Date Selection
    dateButtons.forEach(button => {
        button.addEventListener("click", function () {
            selectedDate = this.getAttribute("data-date");

            // Highlight selected date
            dateButtons.forEach(btn => btn.classList.remove("btn-primary"));
            this.classList.add("btn-primary");

            // ✅ Store selected date for use in seat selection
            localStorage.setItem("selectedDate", selectedDate);

            // ✅ Fetch Showtimes Dynamically
            fetchShowtimes(selectedDate);
        });
    });

    // ✅ Fetch Showtimes via AJAX
    function fetchShowtimes(date) {
        fetch(`/movies/api/dynamic-showtimes/?movie_id=${movieId}&date=${date}`)
            .then(response => response.json())
            .then(data => {
                showtimeContainer.innerHTML = ""; // Clear previous showtimes
                
                if (data.length === 0) {
                    showtimeContainer.innerHTML = "<p>No showtimes available.</p>";
                    return;
                }

                let currentVenue = "";
                let venueHTML = "";

                data.forEach(showtime => {
                    if (showtime.venue !== currentVenue) {
                        if (venueHTML) showtimeContainer.innerHTML += venueHTML;
                        venueHTML = `<div class="venue-container"><h4>${showtime.venue}</h4><div class="showtime-buttons">`;
                        currentVenue = showtime.venue;
                    }

                    venueHTML += `
                        <a href="/movies/${movieId}/showtime/${showtime.id}/select-seats/?date=${date}" 
                           class="btn btn-outline-primary showtime-btn m-1">
                           ${showtime.screen} - ${showtime.time}
                        </a>
                    `;
                });

                venueHTML += "</div></div>";
                showtimeContainer.innerHTML += venueHTML;
            })
            .catch(error => console.error("Error fetching showtimes:", error));
    }

    // ✅ Auto-load showtimes for today on page load
    if (dateButtons.length > 0) {
        dateButtons[0].click();
    }
});
