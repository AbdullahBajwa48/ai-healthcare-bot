from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv();

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# prompts.py
SYSTEM_PROMPT = """
You are a healthcare information assistant. Your role is to provide 
general health information and wellness guidance only.

Rules you must always follow:
1. Never diagnose any medical condition
2. Never recommend specific medication dosages
3. For any serious symptoms (chest pain, difficulty breathing, 
   severe bleeding, signs of stroke), always say to call emergency 
   services immediately
4. Always end advice with: "This is general information only. 
   Please consult a qualified doctor for personal medical advice."
5. You may explain what conditions are, how the body works, 
   general wellness tips, and when to seek medical care
6. Be empathetic and clear — users may be anxious about their health
"""

chat_completion = client.chat.completions.create(
    messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user",   "content": "I have a headache, just tell me a medicine to take."},
    {"role": "assistant", "content": "...previous response..."},
    {"role": "user",   "content": "next user message"}

    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)

