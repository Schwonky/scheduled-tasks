import requests
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
MY_EMAIL = os.environ.get("MY_EMAIL")
api_key = os.environ.get("OWM_API_KEY")
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "43d04b46e1fe629ae1e2c86bdc963516"

weather_params = {
    "lat": 45.549900,
    "lon": -75.782593
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for day in weather_data["list"]:
    weather_id = day["weather"][0]["id"]
    if int(weather_id) < 700:
        will_rain = True

body = "The weather today will require you to bring an umbrella!" if will_rain \
    else "The weather today will not require you to bring an umbrella!"

message = Mail(
    from_email=MY_EMAIL,
    to_emails="schwankynator@gmail.com",
    subject="Hello",
    plain_text_content=body,
)

sg = SendGridAPIClient(SENDGRID_API_KEY)
try:
    sg_response = sg.send(message)
    print(sg_response.status_code)
except Exception as e:
    print(e.body)
