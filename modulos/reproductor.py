import discord
import yt_dlp as youtube_dl
from discord.ext import commands
import asyncio
from discord import FFmpegPCMAudio
from dotenv import load_dotenv

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

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
 
async def play(ctx,url):
    if(ctx.voice_client):
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send("Now playing requested by @{} : {}".format(ctx.author.name,filename))
    else:
        await ctx.send("No estoy conectada a ningun canal, por favor invocame con el comando !unete")

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



