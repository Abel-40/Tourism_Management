from django.shortcuts import render

# Create your views here.
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import escape
from datetime import datetime

def send_welcome_email(email_recipient, username):
    try:
        username = escape(username)  # Sanitize input
        subject = "Welcome to Our Service"
        from_email = settings.EMAIL_HOST_USER  # Use dynamic sender email
        to = [email_recipient]
        text_content = "Thank you for registering!"  # Plain text fallback
        current_year = datetime.now().year

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head></head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4;">
            <div style="background-color: #ffffff; padding: 20px; max-width: 600px; margin: 20px auto; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                <h1 style="text-align: center; color: #0056b3;">Welcome {username} to Explore with Abel</h1>
                <p>
                    We are delighted to offer you an unparalleled experience in tourism management.
                    Our wide range of travel packages is designed to suit all your needs, whether you're seeking an adventurous getaway or a relaxing retreat.
                </p>
                <ul>
                    <li><b>Comprehensive Packages:</b> Explore customized packages that cater to your preferences.</li>
                    <li><b>Integrated Payment System:</b> Enjoy seamless and secure payment options for your bookings.</li>
                    <li><b>Fast Response:</b> Our team ensures quick responses to your inquiries and bookings.</li>
                    <li><b>Exceptional Experiences:</b> We prioritize creating unforgettable memories for our clients.</li>
                </ul>
                <a href="http://127.0.0.1:8000/api/get_packages/" style="display: inline-block; padding: 10px 20px; background-color: #28a745; color: #ffffff; text-decoration: none; border-radius: 4px; margin-top: 20px;">Explore Packages Now</a>
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

