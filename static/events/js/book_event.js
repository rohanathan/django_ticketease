document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("event-booking-container");
    const eventId = container.dataset.id;

    const ticketContainer = document.getElementById("ticket-selection");
    const totalPriceElement = document.getElementById("total-price");
    const proceedBtn = document.getElementById("proceed-btn");
    const errorMessage = document.getElementById("error-message");

    let totalTickets = 0;
    let ticketPrices = {};
    let selectedTickets = {};

    fetch(`/events/api/events/${eventId}/`)
        .then(response => response.json())
        .then(data => {
            ticketPrices = data.ticket_types;
            for (const [type, price] of Object.entries(ticketPrices)) {
                selectedTickets[type] = 0;

                const ticketRow = document.createElement("div");
                ticketRow.classList.add("d-flex", "align-items-center", "mb-3");
                ticketRow.innerHTML = `
                    <div class="flex-grow-1">
                        <h5 class="mb-0">${type}</h5>
                        <p class="text-muted">£${price}</p>
                    </div>
                    <div class="d-flex align-items-center">
                        <button class="btn btn-outline-secondary btn-sm decrease" data-type="${type}">-</button>
                        <span class="mx-2" id="${type}-count">0</span>
                        <button class="btn btn-outline-secondary btn-sm increase" data-type="${type}">+</button>
                    </div>
                `;
                ticketContainer.appendChild(ticketRow);
            }

            document.querySelectorAll(".increase").forEach(button => {
                button.addEventListener("click", () => updateTicketCount(button.dataset.type, 1));
            });

            document.querySelectorAll(".decrease").forEach(button => {
                button.addEventListener("click", () => updateTicketCount(button.dataset.type, -1));
            });

            proceedBtn.addEventListener("click", proceedToPayment);
        })
        .catch(error => console.error("Error fetching ticket details:", error));

    function updateTicketCount(ticketType, change) {
        const countElement = document.getElementById(`${ticketType}-count`);
        const newCount = selectedTickets[ticketType] + change;
        if (newCount < 0) return;

        const newTotal = totalTickets + change;
        if (newTotal > 5) {
            errorMessage.style.display = "block";
            return;
        }
        errorMessage.style.display = "none";

        selectedTickets[ticketType] = newCount;
        totalTickets = newTotal;
        countElement.innerText = newCount;

        let total = 0;
        for (const [type, price] of Object.entries(ticketPrices)) {
            total += selectedTickets[type] * parseFloat(price);
        }
        totalPriceElement.innerText = total.toFixed(2);

        proceedBtn.disabled = totalTickets === 0;
    }

    function proceedToPayment() {
        let ticketType = Object.keys(selectedTickets).find(type => selectedTickets[type] > 0);
        let count = selectedTickets[ticketType];
        if (!ticketType || count === 0) {
            alert("Please select at least one ticket!");
            return;
        }

        let price = ticketPrices[ticketType];
        window.location.href = `/events/${eventId}/create-checkout-session/?category=event&id=${eventId}&ticket_type=${ticketType}&tickets=${count}&price=${price}`;
    }
});
