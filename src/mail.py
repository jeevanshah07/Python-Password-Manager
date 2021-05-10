import smtplib


def send_test(sender_address, receiver_address, password):
    """
    Sends a test email to a user to make sure they passed the correct email

    Args:
        sender_address (str): The address used to send the email
        receiver_address (str): The address to receive the sent email
        password (str): The password for the sender address

    Notes:
        No return value
    """

    sender_address = sender_address

    receiver_address = receiver_address

    account_password = password

    subject = "Test Email using Python"

    body = "Here is the test email from the sql password manager!\n\nHappy to hear from you!\nWith regards,\n\tDeveloper"

    # Endpoint for the SMTP Gmail server (Don't change this!)
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # Login with your Gmail account using SMTP
    smtp_server.login(sender_address, account_password)

    # Let's combine the subject and the body onto a single message
    message = f"Subject: {subject}\n\n{body}"

    # We'll be sending this message in the above format (Subject:...\n\nBody)
    smtp_server.sendmail(sender_address, receiver_address, message)

    # Close our endpoint
    smtp_server.close()


def send_secret(sender_address, receiver_address, password, oneTimeKey):
    """
    Sends a one time password in an email to a user

    Args:
        sender_address (str): The address used to send the email
        receiver_address (str): The address to receive the sent email
        password (str): The password for the sender address
        oneTimeKey (int or str): A time base one time key used for authentication

    Notes:
        No return value
    """

    sender_address = sender_address

    receiver_address = receiver_address

    account_password = password

    subject = "Secret Key"

    body = f"Here is your secret key, Use this to login.\n\n{oneTimeKey}\nSave,\n\tDeveloper"

    # Endpoint for the SMTP Gmail server (Don't change this!)
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # Login with your Gmail account using SMTP
    smtp_server.login(sender_address, account_password)

    # Let's combine the subject and the body onto a single message
    message = f"Subject: {subject}\n\n{body}"

    # We'll be sending this message in the above format (Subject:...\n\nBody)
    smtp_server.sendmail(sender_address, receiver_address, message)

    # Close our endpoint
    smtp_server.close()
