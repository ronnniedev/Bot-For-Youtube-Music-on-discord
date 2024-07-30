"""
    Version 0.9
    Autor: Ronnie
    Reproductor de audio especializado en Youtube:
    -1º El sistema descarga videos de Youtube a traves de la url proporcionada
    -2º Reproduce el sonido en el canal donde se encuentra el usuario, en caso de no encontrarse en el lanza un mensaje de aviso
    -3º Se borra el arvhivo alojado en el sistema, esto hace que el bot sea compatible con uso en la nube ya que no sobrecarga el sistema donde se encuentra con archivos
    -4º Los videos se alojan en cola para su reproduccion secuenciada
"""


import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import os


en_cola = False
cola = {}


"""
    Preparacion de la configuracion del reproductor, en formato dejamos puesto el bestAudio para que el bot recoga el formato con mejor claidad
"""


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
    'source_address': '0.0.0.0' 
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


"""
    Reproduce el audio alojado en la url proporcionada
    @param: ctx context
    @param: url string
    @param: client
"""


async def reproducir_audio(ctx,url,client,guild_id):

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
                    coro = after_playing(ctx, filename,guild_id,client)
                    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                    try:
                        fut.result()
                    except Exception as e:
                        print(f"Error al desconectar: {e}")
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename),after=after_playing_callback)
            await ctx.send('Reproduciendo: {}'.format(url))
    else: 
        await ctx.send('ERROR: No puedo unirme a tu canal')


"""
    Subrutina llamada tras la reproduccion de audio , elimina el archivo alojado con el nombre proporcionado y
    en caso de que la cola no halla terminado reproduce la siguiente cancion, si no termina la cola
    @param: ctx context
    @param: filename string
    @param: guild_id string
    @param: client
"""


async def after_playing(ctx, filename,guild_id,client):
    global en_cola
    os.remove(filename)
    if len(cola[guild_id]) != 0:
        await reproducir_cola(ctx,client,guild_id)
    else:
        en_cola = False
        await ctx.voice_client.disconnect()
        await ctx.send('Cola terminada')
        


"""
    Funcion que crea o añade una cancion a la cola, si la flag de "en cola" no esta en True crea una cola nueva
    en caso contrario añade una url a la cola
    @param: ctx context
    @param: url string
    @param: client
"""


async def play(ctx,url,client):
    global en_cola
    global cola
    guild_id = ctx.message.guild.id
    if not en_cola:
        en_cola = True
        cola[guild_id] = []
        cola[guild_id].append([url])
        await ctx.send('Se ha creado una cola')
        await reproducir_cola(ctx,client,guild_id) 
    else:
        cola[guild_id].append([url])
        await ctx.send('Se ha añadido a la cola')


"""
    Reproduce un elemento de la cola, eliminando el primero
    @param: ctx : context
    @param: guild_id : string
    @param: client
"""


async def reproducir_cola(ctx,client,guild_id):
    global en_cola
    global cola
    url = cola[guild_id].pop(0)
    url = url[0]
    await reproducir_audio(ctx,url,client,guild_id)


"""
    Muestra los videos en cola
    @param: ctx : context
    @param: client
"""


async def mostrar_cola(ctx,client):
    global en_cola
    global cola
    cont = 0
    texto = "En cola:\n"
    await ctx.send(texto)
    guild_id = ctx.message.guild.id
    for item in cola[guild_id]:
        cont += 1
        await ctx.send(str(cont) + " : " + item[0] + "\n")

    
"""
    Pausa el audio si se esta reproduciendo
    @param: ctx context
    @param: client
"""


async def para(ctx,client):
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


"""
    Si el audio ha sido pausado este reanuda el audio desde donde se pauso
    @param: ctx context
    @param: client
"""


async def continua(ctx,client):
    if(ctx.voice_client):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice.is_paused():
            voice.resume()   
        else:
            await ctx.send("La cancion ya esta sonando")
    else:
        await ctx.send("No estoy en ningun canal en este momento") 


"""
    Skipea el audio dentro de la cola, si no hay una url alojada en el diccionario el bot se desconecta
    @param: ctx context
    @param: client
"""


async def skip(ctx,client):
    global cola
    global en_cola
    guild_id = ctx.message.guild.id
    if(ctx.voice_client):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            #esperamos 2 segundos para que se borre la cancion reproducida
            await asyncio.sleep(2) 
            os.remove(filename) 
            if not len(cola[guild_id]) != 0:
                en_cola = False
                await ctx.voice_client.disconnect() 
                await ctx.send("No hay mas canciones en cola, desconexion")
            else:
                await reproducir_cola(ctx,client,guild_id) 
        else: 
            await ctx.send("ERROR: no estoy reproduciendo audio")    
    else:
        await ctx.send("No estoy en ningun canal en este momento")


"""
    Si el audio se esta reproduciendo este es cortado y el bot se va del canal, si no y solo esta el bot en espera simplemente se va.
    @param: ctx context
    @param: client
"""


async def stop(ctx,client):
    global cola
    global en_cola
    guild_id = ctx.message.guild.id
    if(ctx.voice_client):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            voice.stop() 
            await ctx.voice_client.disconnect()
            # esto lo usamos para evitar el error de acceso, al esperar 2 segundos le damos al bot tiempo a cerrar el proceso 
            await asyncio.sleep(2) 
            os.remove(filename)
            cola[guild_id] = [] 
            en_cola = False
        else: 
            await ctx.voice_client.disconnect()    
    else:
        await ctx.send("No estoy en ningun canal en este momento")