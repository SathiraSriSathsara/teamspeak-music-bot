import os
import discord
import youtube_dl
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Set up discord client and bot
client = discord.Client()
bot = commands.Bot(command_prefix='!')

# Set up Spotify client credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='your_client_id',
                                                           client_secret='your_client_secret'))

# Set up youtube-dl options
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
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


# Function to search and play songs from YouTube
def search_and_play_youtube(query):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        except Exception:
            return False

    url = info['webpage_url']
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url))
    return source


# Function to search and play songs from Spotify
def search_and_play_spotify(query):
    results = sp.search(q=query, limit=1)
    if results['tracks']['total'] == 0:
        return False

    track_uri = results['tracks']['items'][0]['uri']
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"spotify:{track_uri}"))
    return source


# Function to search and play songs from SoundCloud
def search_and_play_soundcloud(query):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"scsearch:{query}", download=False)['entries'][0]
        except Exception:
            return False

    url = info['webpage_url']
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url))
    return source


# Command to play music from YouTube
@bot.command()
async def play_youtube(ctx, *, query):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    await voice_channel.connect()

    source = search_and_play_youtube(query)
    if not source:
        await ctx.send(f"Could not find {query} on YouTube!")
        return

    ctx.voice_client.play(source, after=lambda _: print(f"Finished playing {query}"))
    await ctx.send(f"Playing {query}")


# Command to play music from Spotify
@bot.command()
async def play_spotify(ctx, *, query):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    await voice_channel.connect()

    source = search_and_play_spotify(query)
    if not source
