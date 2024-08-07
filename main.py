import discord
from discord.ext import commands
import bromas
# importamos variables de apikeys
from apikeys import *
import reproductor
import asyncio


client = commands.Bot(command_prefix='!', intents=discord.Intents.all()) #Establece las propiedades del cliente, intents los permisos, lo inicializamos con todos, ademas del prefijo de comandos


@client.event
async def on_ready(): # establece que hacer una vez el bot este encendido, en este caso imprime un mensaje en pantalla
    print("Zitra ha sido conectada con exito!")
    print("----------------------------------")
    
@client.command(pass_context = True) 
async def broma(ctx):
    await bromas.bromaActua(ctx)

@client.command(pass_context = True) 
async def play(ctx,url):
    await reproductor.play(ctx,url,client)

@client.command(pass_context = True)
async def stop(ctx):
    await reproductor.stop(ctx,client)

@client.command(pass_context = True)
async def para(ctx):
    await reproductor.para(ctx,client)

@client.command(pass_context = True)
async def continua(ctx):
    await reproductor.continua(ctx,client)

@client.command(pass_context = True) 
async def skip(ctx):
    await reproductor.skip(ctx,client)

@client.command(pass_context = True) 
async def cola(ctx):
    await reproductor.mostrar_cola(ctx,client)

@client.command(pass_context = True)
async def ayuda(ctx):
    await ctx.send("--Comandos de tu servidora Zitra--\n\n"
           + "--!broma :Te escribire una maginifica broma que hara que te deleites en ti mismo\n"
           + "--!play + url de youtube : Si no estoy en un canal de voz me unire y reproducire el video que quieras, tambien en caso de estar reproduciendo audio añadire"
           + " esa cancion a la cola\n"
           + "--!cola te muestro la lista de canciones en cola\n"
           + "--!skip me salto la cancion actual, si no quedan mas canciones, me desconecto\n"
           + "--!para : parare el audio que este reproduciendo\n"
           + "--!continua : reiniciare el audio que allas pausado\n"
           + "--!stop : si quieres que me vaya del canal y parar la cancion actual escribe este comando\n\n"
           + "(>owo)>Ante cualquier problema contacta con mi creadora veroshe_her <(owo<)") 

@client.command(pass_context = True)
async def unete(ctx):
    await ctx.send("Comando desactivado, por favor usa !play + url de youtube de tu cancion para que el bot se una a tu canal :)")

    
client.run(token)





