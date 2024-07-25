import os
import requests
from twilio.rest import Client

def get_weather_data(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to get weather data. HTTP Status code: {response.status_code}")
        print("Response:", response.json())  
        return None

def is_heat_wave(temp, threshold=35):
    return temp >= threshold

def send_alert(to_phone, message, from_phone, account_sid, auth_token):
    client = Client(account_sid, auth_token)
    client.messages.create(
        to=to_phone,
        from_=from_phone,
        body=message
    )

def main():
    api_key = os.getenv('WEATHER_API_KEY', 'your_weather_api_key')
    location = "any_location"
    weather_data = get_weather_data(api_key, location)
    
    if weather_data:
        print("Weather data retrieved:", weather_data)  
        if 'main' in weather_data:
            current_temp = weather_data['main']['temp']
            print(f"Current temperature in {location}: {current_temp}°C")

            account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
            from_phone = os.getenv('TWILIO_FROM_PHONE', 'your_twilio_number')
            to_phone = os.getenv('TO_PHONE', 'recipient_phone_number')
            message = f"Heat wave alert! Current temperature is {current_temp}°C. Stay hydrated and avoid going out in the sun."

            if is_heat_wave(current_temp):
                try:
                    send_alert(to_phone, message, from_phone, account_sid, auth_token)
                    print("Alert sent.")
                except Exception as e:
                    print(f"Failed to send alert: {e}")
            else:
                print("No alert sent.")
        else:
            print("'main' key not found in weather data. Response may have failed due to incorrect API key or location.")
    else:
        print("Failed to retrieve temperature data.")

if __name__ == "__main__":
    main()
