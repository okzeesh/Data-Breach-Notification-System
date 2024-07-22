import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
def check_breaches(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract data breaches (this will depend on the specific website structure)
    breaches = []
    for breach in soup.find_all('div', class_='breach-info'):
        breaches.append(breach.text.strip())
    return breaches                                                                                                        
def send_notification(email, password, to_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, to_email, text)
    server.quit()
def monitor_breaches(url, email, password, to_email):
    known_breaches = set()
    while True:
        breaches = check_breaches(url)
        new_breaches = set(breaches) - known_breaches
        if new_breaches:
            for breach in new_breaches:
                send_notification(email, password, to_email, 'New Data Breach Detected', breach)
                print(f"Notification sent for breach: {breach}")
            known_breaches.update(new_breaches)
        else:
            print("No new breaches detected.")
        time.sleep(3600)  # Check every hour
        # Input your details
breach_url = " https://breachdirectory.org/"  # Replace with the actual URL
email = input("Enter your email: ")
password = input("Enter your email password: ")
to_email = input("Enter the recipient email: ")

# Start monitoring
monitor_breaches(breach_url, email, password, to_email)