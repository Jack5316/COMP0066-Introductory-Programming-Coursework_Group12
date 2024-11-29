import smtplib

def send_email(recipient_emails, subject, body):
    sender_email = 'pythonlover677@gmail.com'
    sender_password = 'iclg xbgj clss dkzk'

    message = f"""
To: {", ".join(recipient_emails)}
Subject: {subject}

{body}
"""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(sender_email, sender_password) 
        server.sendmail(sender_email, recipient_emails, message)  
        print("Email sent")
    except Exception:
        print("Failed to send email")
    finally:
        server.quit()