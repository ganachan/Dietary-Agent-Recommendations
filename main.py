import os
import requests
import base64
from dotenv import load_dotenv
from pymongo import MongoClient
import time

# Load environment variables (if any)
load_dotenv(override=True)

# Configuration
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT").rstrip("/")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
IMAGE_PATH = "./Data/sample/image1.jpg"
COSMOS_CONN_STR = os.getenv("COSMOS_CONNSTR")

# Initialize MongoDB client
client = MongoClient(COSMOS_CONN_STR)
db = client["HealthData"]
collection = db["SugarLevels"]

# Function to get patient data by name
def get_patient_data(name):
    return collection.find_one({"name": name})

# Function to create a prompt for recommendations
def create_prompt(patient_data, food_analysis):
    recommendation_hint = ""
    if patient_data['sugar_level_evening'] > 180:
        recommendation_hint = "The patient's evening sugar levels are high. Consider low-GI foods in the evening."

    return (
        f"Patient Name: {patient_data['name']}\n"
        f"Morning Sugar Level: {patient_data['sugar_level_morning']} mg/dL\n"
        f"Evening Sugar Level: {patient_data['sugar_level_evening']} mg/dL\n"
        f"Food Sensitivity: {patient_data['food_sensitivity']}\n\n"
        f"Image Analysis:\n{food_analysis}\n\n"
        f"{recommendation_hint}\n"
        "Based on the above information, provide personalized dietary recommendations to manage the patient's blood sugar levels."
    )


# Encode the image in base64
with open(IMAGE_PATH, 'rb') as f:
    encoded_image = base64.b64encode(f.read()).decode('ascii')

# API endpoint for your GPT-4V deployment
api_url = f"{ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-15-preview"

# Set up headers for the API request
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}


# Encode the image in base64
with open(IMAGE_PATH, 'rb') as f:
    encoded_image = base64.b64encode(f.read()).decode('ascii')

# Payload for the image analysis request
payload = {
    "messages": [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                     "text": "You are a dietary assistant. Analyze the food items provided in the image, "
                            "estimate portion sizes and calories, and provide general insights on how they might "
                            "impact blood sugar levels"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Here is an image for you to analyze."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
                {"type": "text", "text": "Can you analyze the image for me?"}
            ]
        }
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 800
}

# Measure time for API call
print("Sending image analysis request...")
start_time = time.time()  # Start timer

# Send the request to the Azure OpenAI GPT-4V API

try:
    response = requests.post(
        f"{ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-15-preview",
        headers={"Content-Type": "application/json", "api-key": API_KEY},
        json=payload
    )
    response.raise_for_status()
    result = response.json()
    food_analysis = result['choices'][0]['message']['content']
    end_time = time.time()  # End timer
    print(f"Image analysis took {end_time - start_time:.2f} seconds.")
    print("Image Analysis:\n", food_analysis)
except requests.RequestException as e:
    raise SystemExit(f"Image analysis request failed with error: {e}")

# Get the patient's name from user input
patient_name = input("Enter the patient's name: ")
patient_data = get_patient_data(patient_name)

# Generate recommendations based on patient data and image analysis
if patient_data:
    print(f"Patient Data for {patient_name}:\n", patient_data)

    # Create the prompt using patient data and food analysis
    prompt = create_prompt(patient_data, food_analysis)
    print("\nGenerated Prompt for Recommendations:\n", prompt)

    # Optional: Send the prompt to Azure OpenAI for generating personalized recommendations
else:
    print(f"No data found for {patient_name}.")

# End the total execution timer and print the total time
total_end_time = time.time()
print(f"Image analysis took {end_time - start_time:.2f} seconds.")
