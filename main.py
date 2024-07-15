import discord
from discord.ext import commands
import requests
import json

# importamos variables de apikeys
from apikeys import *

client = commands.Bot(command_prefix='!', intents=discord.Intents.all()) #Establece las propiedades del cliente, intents los permisos, lo inicializamos con todos, ademas del prefijo de comandos

@client.event
async def on_ready(): # establece que hacer una vez el bot este encendido, en este caso imprime un mensaje en pantalla
    print("Zitra ha sido conectada con exito!")
    print("----------------------------------")


@client.command() # si escribimos el comando, hola, escribira esto en pantalla
async def hola(ctx):
    await ctx.send("Hola , encantada de conocerte")

@client.command() # suelta una broma aleatoria usando de llamada a una pagina externa
async def broma(ctx):
    
    url = "https://jokes-always.p.rapidapi.com/common"

    headers = {
	    "x-rapidapi-key": tokenBromas,
	    "x-rapidapi-host": "jokes-always.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    await ctx.send(json.loads(response.text)['data']) # formateamos el texto para que nos suelte un chiste

client.run(token)





