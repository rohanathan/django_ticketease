// Fetch Data from API
    document.addEventListener("DOMContentLoaded", function () {
        const eventId = document.getElementById("event-container").dataset.id;

        fetch(`/events/api/events/${eventId}/`)
            .then(response => response.json())
            .then(data => {
                console.log("API Response:", data);

                document.getElementById("event-title").innerText = data.event_title;
                document.getElementById("event-category").innerText = data.event_category;
                document.getElementById("event-date").innerText = data.event_date;
                document.getElementById("event-location").innerText = data.event_location;
                document.getElementById("event-description").innerText = data.description;
                document.getElementById("book-now-btn").href = `/events/${eventId}/book/`;

                // 🎟️ Populate Ticket Prices (Now Higher in the UI)
                const ticketDiv = document.getElementById("ticket-prices");
                ticketDiv.innerHTML = Object.keys(data.ticket_types).length > 0
                    ? Object.entries(data.ticket_types).map(([type, price]) => `<p><strong>${type}:</strong> £${price}</p>`).join("")
                    : "<p>No ticket pricing available.</p>";

                // 🕒 Populate Schedule
                const scheduleDiv = document.getElementById("event-schedule");
                scheduleDiv.innerHTML = data.schedule.split("\n").map(item => `<p>${item}</p>`).join("");

                // 🎤 Populate Speakers
                const speakersDiv = document.getElementById("speakers-section");
                speakersDiv.innerHTML = data.speakers.length > 0
                    ? data.speakers.map(speaker => `
                        <div class="speaker">
                            <img src="${speaker.image}" alt="${speaker.name}" class="img-thumbnail" style="width: 80px; height: 80px; border-radius: 50%;">
                            <p><strong>${speaker.name}</strong> - ${speaker.role}<br>${speaker.bio}</p>
                        </div>
                    `).join("")
                    : "<p>No speakers announced.</p>";

                // 🏆 Populate Sponsors
                const sponsorsDiv = document.getElementById("sponsors-section");
                sponsorsDiv.innerHTML = data.sponsors.length > 0 
                    ? data.sponsors.map(sponsor => `<p>${sponsor.name} (${sponsor.sponsorship_level})</p>`).join("") 
                    : "<p>No sponsors listed.</p>";

                // ⭐ Populate Reviews
                const reviewsDiv = document.getElementById("reviews-section");
                reviewsDiv.innerHTML = data.reviews_enabled
                    ? `<p>“An amazing event! Can't wait for the next one.” - Jane Doe</p>
                       <p>“Loved the music and the atmosphere!” - John Smith</p>`
                    : "<p>Reviews are disabled for this event.</p>";

                // 📍 Google Maps Embed
                document.getElementById("google-maps").src = data.google_maps_embed 
                    || `https://www.google.com/maps/embed/v1/place?q=${encodeURIComponent(data.event_location)}&key=YOUR_GOOGLE_MAPS_API_KEY`;

                

                // 📢 Social Sharing
                document.getElementById("facebook-share").href = `https://www.facebook.com/sharer/sharer.php?u=${window.location.href}`;
                document.getElementById("twitter-share").href = `https://twitter.com/intent/tweet?url=${window.location.href}&text=${data.event_title}`;

                // ⏳ Countdown Timer
                function updateCountdown() {
                    const eventDate = new Date(data.event_date).getTime();
                    const now = new Date().getTime();
                    const difference = eventDate - now;

                    if (difference > 0) {
                        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
                        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
                        document.getElementById("countdown").innerHTML = `${days}d ${hours}h ${minutes}m`;
                    } else {
                        document.getElementById("countdown").innerHTML = "Event has started!";
                    }
                }
                updateCountdown();
                setInterval(updateCountdown, 60000);
            })
            .catch(error => console.error("Error fetching event details:", error));
    });
