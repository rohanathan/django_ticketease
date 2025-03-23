from .utils import send_notification
import logging

from .utils import send_notification
import logging

from django.conf import settings  # Import settings for email configurations
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def notify_user_registration(user):
    """Sends a welcome email when a user registers."""
    subject = "Welcome to TicketEase! 🎉"
    message = f"""
    Dear {user.first_name},

    Welcome to TicketEase! We're excited to have you on board. 🎟️

    You can now book movies and events with ease.

    Thank you for joining us!

    Regards,
    TicketEase Team
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    print(f" Registration email sent to {user.email}")  # Debugging




def notify_user_payment_success(user, transaction_id, amount, currency, payment_email=None):
    """Sends a payment success notification to the user and logs any issues."""
    subject = "Payment Confirmation - TicketEase"
    message = f"""
    Dear {user.first_name},

    Your payment of {amount} {currency} was successfully processed.
    Transaction ID: {transaction_id}

    Thank you for using TicketEase.

    Regards,
    TicketEase Team
    """

    recipient_email = payment_email if payment_email else user.email
    logger.info(f"📧 Attempting to send payment email to: {recipient_email}")

    try:
        send_notification(recipient_email, subject, message)
        logger.info(f"Payment email successfully sent to {recipient_email}")
    except Exception as e:
        logger.error(f"❌ Failed to send payment email: {e}")


def notify_user_booking_cancelled(user, booking):
    subject = "TicketEase Booking Cancelled"

    item = booking.movie.title if booking.category == "movie" else booking.event.title
    date = booking.showtime.datetime if booking.category == "movie" else booking.event.date

    message = f"""
    Dear {user.first_name},

    Your booking for '{item}' on {date.strftime('%A, %d %B %Y')} has been successfully cancelled.

    A refund of £{booking.total_price} will be processed within 5–7 business days.

    We're sorry to see you cancel. If you need any assistance, feel free to contact us.

    – TicketEase Team
    """

    send_notification(user.email, subject, message)

