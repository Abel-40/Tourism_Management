from django.shortcuts import render

# Create your views here.
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import escape
from datetime import datetime

def send_payment_confirmation_email(email_recipient, username, package_name, amount, booking_date):
    try:
        username = escape(username)  # Sanitize input
        package_name = escape(package_name)  # Sanitize input
        subject = "Booking Payment Confirmation"
        from_email = settings.EMAIL_HOST_USER  # Use dynamic sender email
        to = [email_recipient]
        text_content = "Your payment has been confirmed!"  # Plain text fallback
        current_year = datetime.now().year

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head></head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4;">
            <div style="background-color: #ffffff; padding: 20px; max-width: 600px; margin: 20px auto; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                <h1 style="text-align: center; color: #0056b3;">Payment Confirmation</h1>
                <p>Dear <b>{username}</b>,</p>
                <p>
                    We are thrilled to inform you that your payment for the booking has been successfully processed. 
                    Below are the details of your transaction:
                </p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><b>Package Name:</b></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{package_name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><b>Amount Paid:</b></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">${amount}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><b>Booking Date:</b></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{booking_date}</td>
                    </tr>
                </table>
                <p>
                    Your booking is now confirmed, and we look forward to providing you with an exceptional travel experience.
                    You can view your booking details and manage your reservations by clicking the button below.
                </p>
                <a href="http://127.0.0.1:8000/api/bookings/" style="display: inline-block; padding: 10px 20px; background-color: #28a745; color: #ffffff; text-decoration: none; border-radius: 4px; margin-top: 20px;">View Booking Details</a>
                <div style="text-align: center; font-size: 12px; color: #777; margin-top: 20px;">
                    © {current_year} Abel Adventures. All Rights Reserved.
                </div>
            </div>
        </body>
        </html>
        """

        # Create and send the email
        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
