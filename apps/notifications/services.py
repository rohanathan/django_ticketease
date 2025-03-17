from .utils import send_email_notification

def notify_user_payment_success(user, transaction_id, amount, currency):
    """Sends a payment success notification to the user."""
    subject = "Payment Confirmation - TicketEase"
    message = f"""
    Dear {user.username},

    Your payment of {amount} {currency} was successfully processed.
    Transaction ID: {transaction_id}

    Thank you for using TicketEase.

    Regards,
    TicketEase Team
    """
    send_email_notification(user.email, subject, message)
