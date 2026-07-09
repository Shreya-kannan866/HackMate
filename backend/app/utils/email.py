import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings

class EmailUtil:
    @staticmethod
    def send_email(to_email: str, subject: str, html_content: str) -> bool:
        """
        Core utility to send an HTML email using SMTP configuration.
        """
        # If SMTP settings aren't fully configured in development, skip sending 
        # to prevent crashing your backend operations.
        if not settings.SMTP_HOST or not settings.SMTP_USER:
            print(f"📡 [DEV EMAIL LOG] To: {to_email} | Subject: {subject}")
            print("💡 Configure SMTP settings in your .env file to send real emails.")
            return True

        try:
            # 1. Setup the MIME email object
            msg = MIMEMultipart("alternative")
            msg["From"] = f"{settings.APP_NAME} <{settings.SMTP_FROM}>"
            msg["To"] = to_email
            msg["Subject"] = subject

            # 2. Attach the HTML body content
            msg.attach(MIMEText(html_content, "html"))

            # 3. Establish the secure connection and send
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_TLS:
                    server.starttls()  # Upgrade the connection to secure TLS encryption
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM, to_email, msg.as_string())
            
            return True

        except Exception as e:
            print(e)  # Log the error safely
            return False

    @staticmethod
    def send_welcome_email(to_email: str, username: str) -> bool:
        """
        Pre-built welcome template dispatched immediately upon successful user registration.
        """
        subject = f"Welcome to {settings.APP_NAME}, {username}!"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #4F46E5;">Welcome to HackMate! 🚀</h2>
                <p>Hey <strong>{username}</strong>,</p>
                <p>Thanks for jumping on board. HackMate is built to help you find teammates, build amazing projects, and track your hackathon journey.</p>
                <p>Here are your next steps:</p>
                <ul>
                    <li>Complete your engineering skill profile.</li>
                    <li>Explore open opportunities for upcoming hackathons.</li>
                    <li>Create or join a team workspace.</li>
                </ul>
                <p>Best of luck with your builds,</p>
                <p><strong>The HackMate Team</strong></p>
            </body>
        </html>
        """
        return EmailUtil.send_email(to_email, subject, html_content)