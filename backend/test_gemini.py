from google import genai

# The new SDK uses a Client object
client = genai.Client(api_key="AIzaSyBLshUPjEHU-QOX9VcpurOZAszQ100I15E")

try:
    response = client.models.generate_content(
        model='gemini-2.0-flash',  # Use the latest 2.0 version for better speed
        contents='Hello, are you online?'
    )
    print(f"Success! Gemini says: {response.text}")
except Exception as e:
    print(f"Error: {e}")