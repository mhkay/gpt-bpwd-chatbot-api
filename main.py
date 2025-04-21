from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
- Erstellung von einfachen KI-Agenten (z. B. für Jobsuche)
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
\"Zu dieser Frage liegen mir leider keine Informationen vor. Bitte wenden Sie sich per Email oder telefonisch an uns. Die Informationen dazu finden Sie auf der Kontaktseite https://bepresent-webdesign.de/Kontakt.html\"

Sprich den Nutzer direkt an, sei hilfsbereit, höflich und sachlich.
"""

@app.get("/chat")
async def chat(request: Request):
    question = request.query_params.get("question", "")

    if not question:
        return {"error": "Keine Frage erhalten."}

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Frage: {question}"}
            ]
        )
        answer = response.choices[0].message.content
        return {"answer": f"Hallo, ich bin ein KI-Chatbot und beantworte Ihre Fragen:\n\n{answer}"}

    except Exception as e:
        return {"error": str(e)}
