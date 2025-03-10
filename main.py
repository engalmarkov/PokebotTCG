import discord
import random
import requests
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró el token en el archivo .env")

intents = discord.Intents.default()
intents.messages = True  
intents.dm_messages = True 
intents.message_content = True
bot = discord.Client(intents=intents)

def get_random_pokemon():
    pokemon_id = random.randint(1, 1025) #Actual Pokédex
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}")

    if response.status_code == 200:
        data = response.json()
        name = data["name"].capitalize()
        entries = data["flavor_text_entries"]

        #Switch to spanish
        entry = next((e["flavor_text"] for e in entries if e["language"]["name"] == "es"), "No entry found.") #In case Spanish doesnt exist, return no entry

    card_response = requests.get(f"https://api.pokemontcg.io/v2/cards?q=name:{name}")
    if card_response.status_code == 200:
        card_data = card_response.json()
        if card_data['data']:
            card_image_url = card_data['data'][0]['images']['small']
        else: card_image_url = 'No card found'

    else: 
        card_image_url = 'Error fetching card image'


    return name, entry, card_image_url
    return None, None, None

name, entry, card_image_url = get_random_pokemon()

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    print(f'Bot está conectado a los siguientes servidores:')
    for guild in bot.guilds:
        print(f' - {guild.name}')

# Evento cuando el bot recibe un mensaje
@bot.event
async def on_message(message):
    # No hacer nada si el mensaje es enviado por el propio bot
    print(f"Mensaje recibido: {message.content} en el canal {message.channel}")
    if message.author == bot.user:
        return
    
 # Comando para generar un Pokémon aleatorio
    if message.content.lower() == "!getpokemon":
        name, entry, card_image_url = get_random_pokemon()

        if name:  # Si se obtuvo un Pokémon
            response = f"**Nombre:** {name}\n**Entrada de la Pokédex:** {entry}\n"
            await message.channel.send(response)
            await message.channel.send(card_image_url)  # Enviar la imagen de la carta
        else:
            await message.channel.send("No se pudo obtener un Pokémon en este momento.")

# Ejecutar el bot
bot.run(TOKEN)


