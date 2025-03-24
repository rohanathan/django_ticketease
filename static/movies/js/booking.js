/* static/movies/js/booking.js */

document.addEventListener("DOMContentLoaded", function() {
    // -- Grab DOM elements:
    const bookingDataDiv     = document.getElementById("booking-data");
    const datePicker         = document.getElementById("datePicker");
    const venuePicker        = document.getElementById("venuePicker");
    const showtimePicker     = document.getElementById("showtimePicker");
    const ticketClassPicker  = document.getElementById("ticketClassPicker");
    const ticketQuantity     = document.getElementById("ticketQuantity");
    const totalPriceElement  = document.getElementById("totalPrice");
    const confirmBookingBtn  = document.getElementById("confirmBookingBtn");
    const bookingForm        = document.getElementById("bookingForm");
    const ticketsInput       = document.getElementById("ticketsInput");
    const priceInput         = document.getElementById("priceInput");
  
    // -- Pull data from data-* attributes in the hidden <div>
    const movieId = bookingDataDiv.dataset.movieId;  // e.g. "3"
    // const today   = bookingDataDiv.dataset.today; // if needed
  
    // -- Local state:
    let selectedDate       = "";
    let selectedVenue      = "";
    let selectedShowtimeId = "";
    let selectedClassPrice = 15; // default to 15 (Gold)
    let selectedQuantity   = 0;
  
    /** Utility: disable showtime & quantity if no data */
    function disableShowtimeSelection(message) {
      showtimePicker.innerHTML = `<option value="" selected disabled>${message}</option>`;
      showtimePicker.disabled  = true;
      ticketQuantity.disabled  = true;
      confirmBookingBtn.disabled = true;
    }
  
    /** Utility: enable the showtimePicker with the data we got from the server */
    function populateShowtimeOptions(showtimes) {
      const optionsHtml = showtimes.map(st => {
        // I'm assuming your API returns something like {id: 12, time: "08:00 PM"}
        return `<option value="${st.id}">${st.time}</option>`;
      }).join("");
      showtimePicker.innerHTML = optionsHtml;
      showtimePicker.disabled = false;
    }
  
    /** Called whenever date or venue changes. Pull showtimes from server. */
    function updateShowtimes() {
      if (!selectedDate || !selectedVenue) {
        disableShowtimeSelection("Select a date & venue first");
        return;
      }
      // *** Make sure the URL matches your Django API endpoint
      // If you have something like path('movies/api/showtimes/', ...) with name='api_showtimes',
      // you can do something like:
      // const apiShowtimesUrl = `/movies/api/showtimes/?movie_id=${movieId}&date=${selectedDate}&venue_id=${selectedVenue}`;
      // or use the url tag in a small inline script to define a global variable, etc.
      const apiShowtimesUrl = `/movies/api/showtimes/?movie_id=${movieId}&date=${selectedDate}&venue_id=${selectedVenue}`;
  
      fetch(apiShowtimesUrl)
        .then(response => response.json())
        .then(data => {
          if (!Array.isArray(data) || data.length === 0) {
            disableShowtimeSelection("No showtimes available");
            return;
          }
          populateShowtimeOptions(data);
        })
        .catch(err => {
          console.error("Error fetching showtimes:", err);
          disableShowtimeSelection("Error fetching showtimes");
        });
    }
  
    /** Recalculate and display total price. */
    function updateTotalPrice() {
      const total = selectedQuantity * selectedClassPrice;
      totalPriceElement.innerText = total > 0 ? total.toFixed(2) : "0.00";
    }
  
    /** Enable or disable Confirm button. */
    function updateConfirmButton() {
      // Confirm is valid only if we have a showtime ID and a quantity
      confirmBookingBtn.disabled = (!selectedShowtimeId || !selectedQuantity);
    }
  
    /** Update the form’s action and hidden inputs. */
    function updateFormData() {
      // E.g. if your checkout URL is /movies/<movie_id>/showtime/<showtime_id>/payment/
      // adapt as needed:
      bookingForm.action = `/movies/${movieId}/showtime/${selectedShowtimeId}/payment/`;
  
      // Pass them as GET parameters:
      ticketsInput.value = selectedQuantity;   // e.g. "5"
      priceInput.value   = selectedClassPrice; // e.g. "20"
    }
  
    // -- Attach event listeners:
  
    // date changed
    datePicker.addEventListener("change", () => {
      selectedDate = datePicker.value;
      updateShowtimes();
    });
  
    // venue changed
    venuePicker.addEventListener("change", () => {
      selectedVenue = venuePicker.value;
      updateShowtimes();
    });
  
    // showtime changed
    showtimePicker.addEventListener("change", () => {
      selectedShowtimeId = showtimePicker.value;
      ticketQuantity.disabled = false;  // user can select tickets now
      updateConfirmButton();
      updateFormData();
    });
  
    // ticket class changed
    ticketClassPicker.addEventListener("change", () => {
      selectedClassPrice = parseFloat(ticketClassPicker.value);
      updateTotalPrice();
      updateFormData();
    });
  
    // ticket quantity changed
    ticketQuantity.addEventListener("change", () => {
      selectedQuantity = parseInt(ticketQuantity.value);
      updateTotalPrice();
      updateConfirmButton();
      updateFormData();
    });
  
    // form submit
    bookingForm.addEventListener("submit", (e) => {
      updateFormData();
      // The form will do a GET to the above bookingForm.action
    });
  
    // -- Initialize everything:
    disableShowtimeSelection("Select a date & venue first");
    updateTotalPrice();
    updateConfirmButton();
  });
  