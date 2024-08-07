"""
    ----------------Version 0_32---------------
    Bot de discord especializado en youtube aun asi incluye otras particularidades:
    - Reproductor de audio a traves de youtube
    - Colas de audio totalmente interactuable
    - Funcionales de play,skip,stop integradas
    - Un modulo que realiza bromas mediante el uso de apis
"""


import discord
from discord.ext import commands
import bromas
import reproductor
from apikeys import token


# Establece las propiedades del cliente, intents los permisos,
# lo inicializamos con todos, ademas del prefijo de comandos
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@client.event
async def on_ready():
    """
    Inicia el bot y imprime un mensaje en consola para aclarar su arranque con exito
    """
    print("Zitra ha sido conectada con exito!")
    print("----------------------------------")


@client.command(pass_context=True)
async def broma(ctx):
    """
        Llama al modulo de bromas
        @:param ctx : context
    """
    await bromas.bromaActua(ctx)


@client.command(pass_context=True)
async def play(ctx,url):
    """
        Reproduce una cancion alojada en la url proporcionada
        @:param ctx : context
        @:param url : string
    """
    await reproductor.play(ctx,url,client)


@client.command(pass_context=True)
async def stop(ctx):
    """
        Para y desconecta al bot del canal de voz en caso de necesidad
        @:param ctx : context
    """
    await reproductor.stop(ctx,client)


@client.command(pass_context=True)
async def para(ctx):
    """
        Para la cancion que se este reproducciendo
        @:param ctx : context
    """
    await reproductor.para(ctx,client)


@client.command(pass_context=True)
async def continua(ctx):
    """
        Continua la cancion si esta se encontraba pausada
        @:param ctx : context
    """
    await reproductor.continua(ctx,client)


@client.command(pass_context=True)
async def skip(ctx):
    """
        Salta la cancion a la siguiente en la cola, si no se desconecta del canal de voz
        @:param ctx : context
    """
    await reproductor.skip(ctx,client)


@client.command(pass_context=True)
async def cola(ctx):
    """
        Muestra en el chat las canciones que se encuentran en cola
        @:param ctx : context
    """
    await reproductor.mostrar_cola(ctx)


@client.command(pass_context=True)
async def ayuda(ctx):
    """
        Muestra en el chat los comandos con los que funciona el bot
        @:param ctx : context
    """
    await ctx.send("--Comandos de tu servidora Zitra--\n\n"
           + "--!broma :Te escribire una maginifica broma que hara que te deleites en ti mismo\n"
           + "--!play + url de youtube : Si no estoy en un canal de voz me unire y reproducire el video que quieras, "
           + "tambien en caso de estar reproduciendo audio añadire"
           + " esa cancion a la cola\n"
           + "--!cola te muestro la lista de canciones en cola\n"
           + "--!skip me salto la cancion actual, si no quedan mas canciones, me desconecto\n"
           + "--!para : parare el audio que este reproduciendo\n"
           + "--!continua : reiniciare el audio que allas pausado\n"
           + "--!stop : si quieres que me vaya del canal y parar la cancion actual escribe este comando\n\n"
           + "(>owo)>Ante cualquier problema contacta con mi creadora veroshe_her <(owo<)") 


@client.command(pass_context=True)
async def version(ctx):
    """
    Imprime la informacion de version en pantalla
    @:param ctx:
    """
    await ctx.send("-------Version 0.321 Optimizacion y refactorizacion-------\n"
                       + "--Se mejora el borrado de archivos \n"
                       + "--Se refactoriza el codigo siguiendo convenciones de Python\n"
                       + "-- Se añade el comando -!version\n")


client.run(token)
