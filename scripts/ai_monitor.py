import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key="AIzaSyBEqBbtxdEgJ3iGrgfiz4O5MfADvx3mFJw")

# Load correct model for v1 endpoint
model = genai.GenerativeModel("gemini-2.5-pro")

# Example log to analyze
log_text = "Example: Failed login attempt from IP 192.168.1.2"

response = model.generate_content(
    f"You are an AI security analyst. Analyze the following server logs:\n\n{log_text}"
)

print(response.text)

