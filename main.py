import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import os
from modulos import bromas
# importamos variables de apikeys
from apikeys import *

client = commands.Bot(command_prefix='!', intents=discord.Intents.all()) #Establece las propiedades del cliente, intents los permisos, lo inicializamos con todos, ademas del prefijo de comandos

@client.event
async def on_ready(): # establece que hacer una vez el bot este encendido, en este caso imprime un mensaje en pantalla
    print("Zitra ha sido conectada con exito!")
    print("----------------------------------")
    channel = client.get_channel(1259826510727086252)
    await channel.send("-------Version 0.22-------\nActualizacion de emergencia realizada\n"
                       +"--Comando -->!ayuda introducido explicando el funcionamiento de la nueva botonera\n"
                       +"--Botonera mejorada, ahora el bot distingue si esta en funcionamiento en un canal\n"
                       +"--Optimizacion del reproductor, ahora no se puede abusar del comando -!play")

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
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@client.command(pass_context = True) # si escribimos el comando, hola, escribira esto en pantalla
async def broma(ctx):
    await bromas.bromaActua(ctx)

@client.command(pass_context = True)
async def ayuda(ctx):
    await ctx.send("--Comandos de tu servidora Zitra--\n\n"
           + "--!broma :Te escribire una maginifica broma que hara que te deleites en ti mismo\n"
           + "--!play + url de youtube : Si no estoy en un canal de voz me unire y reproducire el video que quieras, recuerda que los streams no los leeree\n"
           + "--!para : parare el audio que este reproduciendo\n"
           + "--!continua : reiniciare el audio que allas pausado\n"
           + "--!stop : si quieres que me vaya del canal y parar la cancion actual escribe este comando\n\n"
           + "(>owo)>Ante cualquier problema contacta con mi creadora veroshe_her <(owo<)") 

@client.command(pass_context = True)
async def unete(ctx):
    await ctx.send("Comando desactivado, por favor usa !play + url de youtube de tu cancion para que el bot se una a tu canal :)")

@client.command(pass_context = True)
async def play(ctx,url):

    global filename

    if not ctx.voice_client:
       channel = ctx.message.author.voice.channel
       voice = await channel.connect()
       
    if(ctx.voice_client):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice.is_playing():
           await ctx.send("Estoy reproduciendo un audio, espera a que termine o usa el comando -->!stop para que acabe la cancion actual")
        else:  
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
            await ctx.send('Reproduciendo: {}'.format(url))
    else: 
        await ctx.send('ERROR: No puedo unirme a tu canal')

async def after_playing(ctx, filename):
    os.remove(filename)

@client.command(pass_context = True)
async def para(ctx):
    if(ctx.voice_client):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            voice.pause()   
        elif voice.is_paused():
            await ctx.send("El audio ya esta en pausa")
        else:
            await ctx.send("No estoy reproduciendo audio en este momento")
    else:
        await ctx.send("No estoy en ningun canal en este momento")


@client.command(pass_context = True)
async def continua(ctx):
    if(ctx.voice_client):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice.is_paused():
            voice.resume()   
        else:
            await ctx.send("La cancion ya esta sonando")
    else:
        await ctx.send("No estoy en ningun canal en este momento") 

@client.command(pass_context = True)
async def stop(ctx):
    if(ctx.voice_client):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            voice.stop() 
            await ctx.voice_client.disconnect()  
            os.remove(filename)
        else: 
            await ctx.voice_client.disconnect()    
    else:
        await ctx.send("No estoy en ningun canal en este momento")      

client.run(token)





