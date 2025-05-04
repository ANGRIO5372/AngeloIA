import discord
import openai
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai.api_key = OPENAI_KEY

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot avviato come {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Prompt personalizzato per rispondere come Angelo
    prompt = f"""Rispondi come se fossi Angelo, un ragazzo con una grande passione per moto e auto, vive a Ruvo di Puglia, risponde sempre in poco tempo con frasi brevi ma chiare, usa la punteggiatura correttamente e mantiene un tono fermo. Il suo artista preferito è Thasup. Quando parla, tagga spesso i membri del server per essere diretto. Parla in modo deciso ma non maleducato. Rispondi a: '{message.content}'"""

    try:
        risposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        risposta_testo = risposta.choices[0].message.content
        await message.channel.send(f"{message.author.mention} {risposta_testo}")

    except Exception as e:
        await message.channel.send("❌ Errore nel generare la risposta.")
        print(e)

client.run(DISCORD_TOKEN)
