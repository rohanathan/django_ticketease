from .utils import send_notification
import logging

from .utils import send_notification
import logging



logger = logging.getLogger(__name__)

def notify_user_registration(user):
    """Sends a welcome email when a user registers."""
    subject = "Welcome to TicketEase! 🎉"
    message = f"""
    Dear {user.username},

    Welcome to TicketEase! We're excited to have you on board. 🎟️

    You can now book movies and events with ease.

    Thank you for joining us!

    Regards,
    TicketEase Team
    """

    logger.info(f"📧 Attempting to send registration email to: {user.email}")

    try:
        send_notification(user.email, subject, message)
        logger.info(f"✅ Registration email sent to {user.email}")
    except Exception as e:
        logger.error(f"❌ Failed to send registration email: {e}")




def notify_user_payment_success(user, transaction_id, amount, currency, payment_email=None):
    """Sends a payment success notification to the user and logs any issues."""
    subject = "Payment Confirmation - TicketEase"
    message = f"""
    Dear {user.username},

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
        logger.info(f"✅ Payment email successfully sent to {recipient_email}")
    except Exception as e:
        logger.error(f"❌ Failed to send payment email: {e}")
