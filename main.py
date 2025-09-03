import os
import discord
from threading import Thread
from flask import Flask
from dotenv import load_dotenv

# Importar módulos
from anime_search import buscar_anime
from serie_search import buscar_serie
from genero_search import handle_genero_command, handle_genre_interaction

# -------------------------
# Carregar variáveis de ambiente
# -------------------------
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("⚠️ Token do Discord não encontrado. Defina a variável de ambiente DISCORD_TOKEN.")

# -------------------------
# Servidor Flask (mantém vivo)
# -------------------------
app = Flask('')

@app.route('/')
def home():
    return "O bot está rodando no Render!"

def run():
    port = int(os.environ.get("PORT", 8080))  # Porta do Render
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

# -------------------------
# Configuração do bot Discord
# -------------------------
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# -------------------------
# Eventos do bot
# -------------------------
@client.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component:
        await handle_genre_interaction(interaction)

@client.event
async def on_ready():
    print(f'🤖 Bot logado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!anime'):
        await buscar_anime(client, message)

    if message.content.startswith('!serie'):
        await buscar_serie(client, message)

    if message.content.startswith('!genero'):
        await handle_genero_command(client, message)

# -------------------------
# Inicia Flask + Bot
# -------------------------
keep_alive()
client.run(TOKEN)
