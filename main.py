import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import os
import time
from modulos import bromas
# importamos variables de apikeys
from apikeys import *


client = commands.Bot(command_prefix='!', intents=discord.Intents.all()) #Establece las propiedades del cliente, intents los permisos, lo inicializamos con todos, ademas del prefijo de comandos
filename = ""

@client.event
async def on_ready(): # establece que hacer una vez el bot este encendido, en este caso imprime un mensaje en pantalla
    print("Zitra ha sido conectada con exito!")
    print("----------------------------------")
    channel = client.get_channel(1259826510727086252)
    await channel.send("-------Version 0.2-------\n\nEste bot ahora esta en la nube!\n\n--!play hara que el bot se una a tu canal de voz y reproduzca un audio"+
                       "\n\n--!stop hara que se pare y se vaya del canal")

@client.command(pass_context = True) # si escribimos el comando, hola, escribira esto en pantalla
async def test(ctx):
    os.remove("hola.txt")

@client.command(pass_context = True) # si escribimos el comando, hola, escribira esto en pantalla
async def broma(ctx):
    await bromas.bromaActua(ctx)

@client.command(pass_context = True)
async def unete(ctx):
    await ctx.send("Este comando ya no funciona: Usa !play + url de tu video para que me conecte a tu canal :)")

@client.command(pass_context = True)
async def vete(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Me he desconectado")
    else:
        await ctx.send("No estoy en ningun canal")

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'mp4',
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
    def __init__(self, source, *, data, volume=0.1):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
        
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
 
@client.command(pass_context = True)
async def play(ctx,url):
    global filename
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    if(ctx.voice_client):
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            def after_playing_callback(error):
                coro = after_playing(ctx, filename)
                fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                try:
                    fut.result()
                except Exception as e:
                    print(f"Error al desconectar: {e}")
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename),after=after_playing_callback)
        await ctx.send("Now playing requested by @{} : {}".format(ctx.author.name,filename))
    else:
        await ctx.send("No estoy conectada a ningun canal, por favor invocame con el comando !unete")

async def after_playing(ctx, filename):
    os.remove(filename)

@client.command(pass_context = True)
async def para(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()   
    else:
        await ctx.send("No estoy reproduciendo audio en este momento")

@client.command(pass_context = True)
async def continua(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()   
    else:
        await ctx.send("No estoy reproduciendo audio en este momento")

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.voice_client.disconnect() 
    os.remove(filename)   

client.run(token)





