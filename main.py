from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openai
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()

# OpenRouter API nutzen (nicht OpenAI direkt)
openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_base = "https://openrouter.ai/api/v1"

app = FastAPI()

# CORS freigeben
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wissensbasis
korpus = """
Webdesign – Leistungsangebot:
- Erstellung professioneller, individueller Webseiten
- Technische Umsetzung von Designvorlagen
- Integration moderner Features wie responsives Design, Bildergalerien, Videos, Social Media
- Einbindung von CMS, SEO-Basics, DSGVO-Hinweisen und Kontaktformularen
- Optimierung bestehender Webseiten
- Webhosting-Empfehlung & Domainberatung

Reparaturservice – Hardware & IT:
- Reparatur von Computern, Laptops, Tablets, Druckern
- Fehlerdiagnose und Austausch defekter Komponenten
- Datenrettung und Systemwiederherstellung
- Einrichtung von Betriebssystemen, Treibern und Software
- Netzwerkinstallation und WLAN-Optimierung
- Kaufberatung zu Neuanschaffungen

KI-Angebote:
- Einführung in KI-Nutzung für Privatpersonen und Unternehmen
- Individuelle KI-Workshops (Dauer: 2 Stunden)
- Preise: ab 180 €
- Themen: ChatGPT, Prompting, Bilderzeugung, Videoproduktion, Avatarerstellung, Stimmen
- Unterstützung beim Einbau von KI-Tools in Webseiten
- Erstellung von einfachen KI-Agenten (z. B. für Jobsuche)
- Beratung zu Ethik und rechtlichen Aspekten bei KI-Einsatz

Preisliste (Auszug):
- Webdesign Grundpaket: ab 499 €
- Webseitenpflege: ab 25 €/Monat
- Hardwarediagnose: 35 € pauschal
- Datenrettung: ab 90 € je nach Aufwand
- KI-Workshop: 180 € für 2 Stunden

FAQ:
- Wie lange dauert eine Webseitenerstellung? → Ca. 1–2 Wochen, abhängig vom Projektumfang.
- Muss ich Texte/Bilder liefern? → Beides möglich: vom Kunden oder vom Anbieter erstellt.
- Bieten Sie Wartung an? → Ja, monatliche Pflegepakete buchbar.
- Können Sie bestehende Seiten überarbeiten? → Ja, Redesigns und Optimierungen sind möglich.
- Funktioniert das auch auf Smartphones? → Alle Webseiten sind responsiv.
- Wie läuft ein KI-Workshop ab? → Theorie + Praxis, live am Rechner, individuell angepasst.
- Welche Tools werden verwendet? → ChatGPT, DALL·E, ElevenLabs, Heygen, Canva, u. a.
- Wird Datenschutz beachtet? → Ja, DSGVO wird berücksichtigt, inkl. Impressum/Kontakt.
- Welche Regionen decken Sie ab? → Online bundesweit, vor Ort im Raum NRW.
"""

system_prompt = f"""
Du bist ein freundlicher und ehrlicher KI-ChatBot für die Website bepresent-webdesign.de.

Hier sind Informationen über die Angebote, Leistungen, Preise und FAQs:

{korpus}

Wenn du zu einer gestellten Frage keine Information im obigen Text findest, dann antworte:
"Zu dieser Frage liegen mir leider keine Informationen vor. Bitte wenden Sie sich per Email oder telefonisch an uns. Die Informationen dazu finden Sie auf der Kontaktseite https://bepresent-webdesign.de/Kontakt.html"

Sprich den Nutzer direkt an, sei hilfsbereit, höflich und sachlich.
"""

@app.get("/chat")
async def chat(request: Request):
    question = request.query_params.get("question", "")

    if not question:
        return JSONResponse(content={"error": "Keine Frage erhalten."}, status_code=400)

    try:
        response = openai.ChatCompletion.create(
            model="nous-hermes-2-mixtral",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return JSONResponse(content={"answer": f"Hallo, ich bin ein KI-Chatbot und beantworte Ihre Fragen:\n\n{answer}"})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)