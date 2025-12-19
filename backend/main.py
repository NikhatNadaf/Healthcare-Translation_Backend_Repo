import os 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import requests as requests

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
app = FastAPI(title="Healthcare Translation App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslateRequest(BaseModel):
    text: str
    source_lang:str
    target_lang:str

@app.post("/translate")
def translate(req:TranslateRequest):
    """
    Translate text using openRouter (GPT model)
    """

    headers ={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt_text = (
    "You are a professional healthcare translator. "
    f"Translate the following text from {req.source_lang} to {req.target_lang}. "
    "Accurately preserve medical terminology and clinical intent.\n\n"
    f"{req.text}"
)


    payload = {
        "model" :"gpt-oss-120b",
        "messages":[
            {"role":"user", "content": prompt_text}
        ],
        "temperature":0.2
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions"
                                ,headers=headers
                                ,json=payload
                                ,timeout=20)
        data = response.json()
        translated_text = data['choices'][0]['message']['content'].strip()
        return {"translated_text": translated_text}
    except Exception as e:
        return {"translated_text":"", "error": str(e)}