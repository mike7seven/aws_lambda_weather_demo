import requests
import json
import os
import smtplib
import logging
from datetime import datetime

# https://openweathermap.org/api/one-call-api
# https://openweathermap.org/api/one-call-3

# empire state building
lat = '40.75009231913161'
lon = '-73.98638285425646'
exclude = 'minutely,hourly,alerts'

# 2.5 API Call
url = (
    'https://api.openweathermap.org/data/2.5/onecall?' +
    'lat={lat}&lon={lon}&exclude={exclude}&appid={API_key}&units=imperial'
)

""" 3.0 API Call
url = ( 
    'https://api.openweathermap.org/data/3.0/onecall?' +
    'lat={lat}&lon={lon}&exclude={exclude}&appid={API_key}&units=imperial'
)
"""

if os.path.isfile('.env'):
    from dotenv import load_dotenv
    load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def __send_email(msg: str) -> None:
    gmail_user = os.getenv('EMAIL_USER')
    gmail_password = os.getenv('EMAIL_PASSWORD')
    logger.error(__send_email)

    # Create Email
    mail_from = gmail_user
    mail_to = gmail_user
    mail_subject = f'Weather Today {datetime.today().strftime("%m/%d/%Y")}'
    mail_message = f'Subject: {mail_subject}\n\n{msg}'

    # Send Email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(mail_from, mail_to, mail_message)
    server.close()


def handler(event, context):
    response = requests.get(url.format(
        lat=lat,
        lon=lon,
        exclude=exclude,
        API_key=os.getenv('WEATHER_API_KEY')
    ))

    data = response.json()

    rain_conditions = ['rain', 'thunderstorm', 'drizzle']
    snow_conditions = ['snow']

    today_weather = data['daily'][0]['weather'][0]['main'].lower()

    if today_weather in rain_conditions:
        msg = 'The weather is rainy today at the Empire State building, pack an umbrella!'
    elif today_weather in snow_conditions:
        msg = 'The weather is and snowy today at the Empire State building, pack your snow boots!'
    else:
        msg = 'The weather is nice today at the Empire State building, prepare for clear skies today!'

    __send_email(msg)

handler(None, None)
