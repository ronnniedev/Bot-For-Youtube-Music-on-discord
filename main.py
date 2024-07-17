import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import yt_dlp as youtube_dl
from discord import FFmpegPCMAudio
# from modulos.bromas import *
# importamos variables de apikeys
import requests
import json
from apikeys import *

client = commands.Bot(command_prefix='!', intents=discord.Intents.all()) #Establece las propiedades del cliente, intents los permisos, lo inicializamos con todos, ademas del prefijo de comandos

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
        
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop 
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@client.event
async def on_ready(): # establece que hacer una vez el bot este encendido, en este caso imprime un mensaje en pantalla
    print("Zitra ha sido conectada con exito!")
    print("----------------------------------")


@client.command() # si escribimos el comando, hola, escribira esto en pantalla
async def hola(ctx):
    await ctx.send("Hola , encantada de conocerte")

@client.command() # si escribimos el comando, hola, escribira esto en pantalla
async def broma(ctx):
    
    url = "https://jokes-always.p.rapidapi.com/common"

    headers = {
	    "x-rapidapi-key": tokenBromas,
	    "x-rapidapi-host": "jokes-always.p.rapidapi.com"
    }

    response= requests.get(url, headers=headers)
    texto = json.loads(response.text)['data']
    # await ctx.send(texto)
    # formateamos el texto para que nos suelte un chiste
    
    url = "https://google-translator9.p.rapidapi.com/v2"

    payload = {
	    "q": texto,
	    "source": "en",
	    "target": "es",
	    "format": "text"
    }
    headers = {
	    "x-rapidapi-key": tokenBromas,
	    "x-rapidapi-host": "google-translator9.p.rapidapi.com",
	    "Content-Type": "application/json"
    }

    respuesta = requests.post(url, json=payload, headers=headers)
    #Convertimos la respuesta de jason en un dato de tipo diccionario 
    respuesta = respuesta.json() 
    """le indicamos donde esta el texto a escribir, le decimos que esta en data, seccion translations, elemento 0 y translated text"""
    texto = respuesta['data']['translations'][0]['translatedText'] 
    
    await ctx.send(texto)

@client.command(pass_context = True)
async def unete(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
    else:
        await ctx.send("No estas en ningun canal de voz, por favor unete a uno")

@client.command(pass_context = True)
async def vete(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Me he desconectado")
    else:
        await ctx.send("No estoy en ningun canal")

@client.command(pass_context = True)
async def play(ctx,url):
    if(ctx.voice_client):
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    else:
        await ctx.send("No estoy conectada a ningun canal, por favor invocame con el comando !unete")


client.run(token)





