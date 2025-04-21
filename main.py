# main.py – GPT ChatBot API mit FastAPI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# CORS (damit Website auf API zugreifen darf)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für Produktion ggf. Domain angeben
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# /chat Endpoint
@app.get("/chat")
async def chat(request: Request):
    question = request.query_params.get("question", "")
    if not question:
        return {"error": "Keine Frage erhalten."}

    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher ChatBot für bepresent-webdesign.de. Antworte klar, verständlich und freundlich."},
                {"role": "user", "content": question}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}
