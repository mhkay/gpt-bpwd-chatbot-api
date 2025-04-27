# main.py - GPT-4o Anbindung an bepresent-webdesign.de, mit sauberen Fehler-Logs und stabilem CORS

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

# FastAPI App initialisieren
app = FastAPI()

# CORS Einstellungen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API-Key aus Umgebungsvariablen holen
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
- Welche Regionen decken Sie ab? → Online bundesweit, vor Ort im Raum Landshut.
"""


# Endpoint für den ChatBot
@app.get("/chat")
async def chat(request: Request):
    try:
        question = request.query_params.get("question")
        if not question:
            return {"error": "Keine Frage übermittelt."}

        # Anfrage an OpenAI senden
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein freundlicher Assistent für die Webseite bepresent-webdesign.de. Wenn du eine Frage nicht beantworten kannst, verweise bitte auf die Kontaktseite https://bepresent-webdesign.de/Kontakt.html."},
                {"role": "user", "content": question}
            ],
            max_tokens=400
        )

        # Antwort extrahieren
        answer = response['choices'][0]['message']['content'].strip()

        # Antwort an den Browser schicken
        return {"frage": question, "antwort": answer}

    except Exception as e:
        # Fehler abfangen und in Render-Log ausgeben
        print(f"❗ Fehler im Chat-Endpunkt: {e}")
        return {"error": f"Interner Serverfehler: {str(e)}"}

# (Optional) Root-Endpunkt, falls Render eine Startseite verlangt
@app.get("/")
async def root():
    return {"message": "ChatBot API laeuft!"}
