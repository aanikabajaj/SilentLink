import google.generativeai as genai

# Load Gemini API key and model
genai.configure(api_key="AIzaSyBEqBbtxdEgJ3iGrgfiz4O5MfADvx3mFJw")
model = genai.GenerativeModel('gemini-2.5-pro')

# Read latest log line from logs/audit.log
with open("logs/backup_audit.log") as f:
    log_line = f.readlines()[-1]

# Generate AI insight
prompt = f"Of course. As an AI security analyst, analyze this log: {log_line}"
response = model.generate_content(prompt)

# Save analysis
with open("logs/ai_insights.log", "a") as f:
    f.write(response.text + "\n\n")
