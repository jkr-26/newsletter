import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import re
from email.utils import formataddr

# URL of the PHP script
url = "https://ibeeanalytics.com/newsletter/testing.php"

# Send a GET request to the PHP script
response = requests.get(url)

# Check if the response was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    emails = [[item['usr_id'], item['email'], item['count']] for item in data]

else:
    print("Failed to retrieve data:", response.status_code)

# SMTP server configuration
SMTP_SERVER = 'sg2plzcpnl505626.prod.sin2.secureserver.net'  
SMTP_PORT = 25
SENDER_NAME = 'iBee Analytics Newsletter'
SENDER_EMAIL = 'newsletter@ibeeanalytics.com'  
SENDER_PASSWORD = 'sM6W6z+#cjju'

# List of recipients (example list, replace with your actual recipients)

# Email content
subject = "Git Automation"

# Throttling settings
emails_per_batch = 10  # Number of emails to send in one batch
sleep_time_between_batches = 10  # Time to sleep between batches (in seconds)

# Create the SMTP session
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SENDER_EMAIL, SENDER_PASSWORD)

# Log file
log_file = open("email_log.txt", "w")

# Send emails in batches
for i in range(0, len(emails), emails_per_batch):
    batch = emails[i:i + emails_per_batch]
    for recipient in batch:
        try:
            html_content = """
            <h1> Git Test By Janakiraman.</h1>
                   """
            msg = MIMEMultipart()
            msg['From'] = formataddr((SENDER_NAME, SENDER_EMAIL))
            msg['To'] = recipient[1]
            msg['Subject'] = subject

            # Attach the body with the msg instance
            msg.attach(MIMEText(html_content, 'html'))

            # Send the email
            server.sendmail(SENDER_EMAIL, recipient[1], msg.as_string())
            log_file.write(f"Email sent to {recipient[1]} (User ID: {recipient[0]})\n")
            print(f"Email sent to {recipient[1]} (User ID: {recipient[0]})")

        except Exception as e:
            # log_file.write(f"Failed to send email to {recipient[1]}-{recipient[0]} {e}\n")
            # print(f"Failed to send email to {recipient[1]}-{recipient[0]} {e}")
            max_retries = 5
            retry_count = 0
            while retry_count < max_retries:
                try:
                    # Create the SMTP session
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls()
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    break
                except smtplib.SMTPException as e:
                    print(f"Failed to connect to SMTP server: {e}")
                    print(f"Retrying ({retry_count+1}/{max_retries}) in 5 seconds...")
                    time.sleep(5)
                    retry_count += 1
            if retry_count == max_retries:
                print("Failed to connect to SMTP server after maximum retries. Exiting.")
                sys.exit(1)

    # Sleep between batches
    print(f"Sleeping for {sleep_time_between_batches} seconds or press Ctrl C")
    time.sleep(sleep_time_between_batches)

# Terminate the SMTP session
server.quit()

log_file.close()

print("All emails sent successfully! Check the log file for details.")
# check subject 
# check add page
# check referral section link
# send mail automation