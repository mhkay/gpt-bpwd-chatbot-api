from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI Client vorbereiten
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/chat")
async def chat(request: Request):
    question = request.query_params.get("question", "")

    if not question:
        return {"error": "Keine Frage erhalten."}

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Oder gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher ChatBot für bepresent-webdesign.de. Antworte klar, freundlich und ehrlich."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}

