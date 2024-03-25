import json
from asyncio import sleep

import discord

import parsers
from main import bot
from utils import guild_id, create_embed, stream_channel


async def song(ctx, song_name):
    voice_client = discord.utils.get(bot.voice_clients, guild=bot.get_guild(guild_id))
    if voice_client is None or not voice_client.is_playing():
        voice_state = ctx.author.voice
        if voice_state is None:
            embed = create_embed("You need to be in a voice channel to use this command.")
            return await ctx.respond(embed=embed, ephemeral=True)

        channel = voice_state.channel.id
        if channel == stream_channel:
            embed = create_embed("You can't use this command in the stream channel.")
            return await ctx.respond(embed=embed, ephemeral=True)

        await ctx.defer()

        with open("data/songs.json", "r", encoding="utf-8") as fp:
            data = json.load(fp)
        songs = data["songs"]

        index = next(filter(lambda s: s["title"].lower() == song_name.lower(), songs), None)
        song = parsers.Song.from_dict(index)

        if voice_client is None:
            voice_client = await bot.get_channel(channel).connect()
        await play(ctx, voice_client, song, channel)

        embed = create_embed("Playing `%s` in <#%s>" % (song.title, channel))
        await ctx.followup.send(embed=embed)

        while voice_client.is_playing():
            await sleep(1)
        await voice_client.disconnect()
    else:
        embed = create_embed("I'm already playing a song. Please wait until it's finished.")
        return await ctx.respond(embed=embed, ephemeral=True)


async def play(ctx, voice_client, song: parsers.Song, channel):
    if voice_client.is_connected():
        source = discord.FFmpegPCMAudio(song.url, executable="ffmpeg")
        voice_client.play(source)