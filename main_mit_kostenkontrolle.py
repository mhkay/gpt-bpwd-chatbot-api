from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI
import datetime
import httpx  # NEU: Für HTTP-Requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USAGE_LIMIT = 0.20  # Tageslimit in USD

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

async def check_usage_limit():
    today = datetime.datetime.utcnow().date()
    start_date = today.strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            usage_data = response.json()
            total_usage = usage_data.get("total_usage", 0) / 100  # OpenAI gibt usage in Cent
            return total_usage
        else:
            return 0  # Wenn die Abfrage fehlschlägt, lieber nicht blockieren

@app.get("/chat")
async def chat(request: Request):
    question = request.query_params.get("question", "")

    if not question:
        return {"error": "Keine Frage erhalten."}

    usage_today = await check_usage_limit()  # ✅ richtig eingerückt!
    if usage_today > USAGE_LIMIT:
        return {
            "error": "Das tägliche Nutzungslimit für den KI-ChatBot wurde erreicht. Bitte versuchen Sie es morgen erneut oder kontaktieren Sie uns direkt."
        }

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


