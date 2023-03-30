import requests
import os
from datetime import datetime

APP_ID = os.environ.get("NUTRITIONIX_APP_ID")
API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
WORKOUT_KEY = os.environ.get("SHEETY_KEY")
WORKOUT_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
EXERCISE_ENDPOINT = os.environ.get("NUTRITIONIX_ENDPOINT")
WORKOUT_BEARER_TOKEN = os.environ.get("SHEETY_BEARER_TOKEN")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

query = input("Tell me which exercise you did: ")
request_body = {
    "query": query,
    "gender": "male",
    "weight_kg": 75,
    "height_cm": 180,
    "age": 24
}

workout_headers = {
    "Authorization": f"Bearer {WORKOUT_BEARER_TOKEN}"
}

response = requests.post(url=EXERCISE_ENDPOINT, json=request_body, headers=headers)
response.raise_for_status()
exercises = response.json()['exercises']

for exercise in exercises:
    workout_body = {
        "workout": {
            "date": datetime.now().strftime("%Y/%m/%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "exercise": exercise['name'],
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']
        }
    }
    workout_res = requests.post(url=f"{WORKOUT_ENDPOINT}/{WORKOUT_KEY}/copyOfMyWorkouts/workouts", json=workout_body,
                                headers=workout_headers)
    workout_res.raise_for_status()
    print(workout_res.json())
