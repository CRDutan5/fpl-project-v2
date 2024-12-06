import requests
from dotenv import load_dotenv
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime
import sys

load_dotenv()

my_team_key = os.getenv("MY_TEAM_ID")
my_email = os.getenv("MY_EMAIL")
credentials = os.getenv("CREDENTIALS")

# Main api response
def get_main_response():
    main_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    main_response = requests.get(main_url).json()
    return main_response

# function to grab prev gameweek to look at picks
def determine_gameweek_for_picks():
    main_response = get_main_response()
    gameweeks = main_response["events"]
    for i in range(len(gameweeks)):
        if gameweeks[i]["is_current"] == True:
            return gameweeks[i]["id"]

# Grabs my players ids for the week
def my_current_team_picks_ids():
    current_gameweek = determine_gameweek_for_picks()
    url = (f"https://fantasy.premierleague.com/api/entry/{my_team_key}/event/{current_gameweek}/picks/")
    res = requests.get(url).json()
    current_team_df = pd.DataFrame(res["picks"])
    current_team_ids = current_team_df["element"].tolist()
    return current_team_ids

def send_email(gameweek):
    sender_email = my_email
    sender_credentials = credentials
    receiver_email = my_email

    # Create Container
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = f'FPL Recommendations - Gameweek: {gameweek}'

    # Text
    body = f"Here are your FPL recommendations for Gameweek: {gameweek}"
    msg.attach(MIMEText(body, "plain"))

    # Attach the file
    filename = f"Gameweek-{gameweek}.txt"
    with open(filename, "r") as f:
        # Create attachment
        attachment = MIMEApplication(f.read(), _subtype="txt")
        # Add header
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        # put the attachment in the box
        msg.attach(attachment)

    # Send the package
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_credentials)
            server.send_message(msg)
            return True
    except Exception as e:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Error sending email: {str(e)}", file=sys.stderr)
        return False


