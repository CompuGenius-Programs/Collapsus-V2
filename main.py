import json
import os
import random
from asyncio import sleep

import discord
import dotenv
import emoji
from discord import Option
from titlecase import titlecase

import parsers
from commands.core import help_function
from commands.grotto import grotto_command, translate_grotto
from commands.songs import song, play
from utils import create_embed, guild_id, stream_channel, quests_channel, clean_text, dev_tag, krak_pop_image_url, \
    item_images_url, weapon_images_url, armor_images_url, accessory_images_url, shields_images_url, int_from_string, \
    monster_images_url, create_paginator, character_image_url, rules_channel_en, rules_channel_fr, rules_channel_de, \
    rules_channel_jp, welcome_channel, role_en, role_fr, role_de, role_jp, role_celestrian

dotenv.load_dotenv()
token = os.getenv("TOKEN")

bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name="over The Quester's Rest. Type /help ."))


@bot.command(name="help", description="Get help for using the bot.")
async def _help(ctx):
    await ctx.respond(embed=help_function())


@bot.command(name="migrate_resources")
async def _migrate_resources(ctx):
    await ctx.defer()

    test_mode = os.getenv("TEST_MODE", "FALSE").lower() == "true"

    test_resources_channel = 1142886986949087272
    resources_channel = 1143509536783736965

    if test_mode:
        resources_channel = test_resources_channel

    migrations = [
        {
            "test_channel": 1142195240833388655,
            "channel": 891711067976249375,
            "thread": True,
            "title": "Grotto Info"
        },
        {
            "test_channel": 1142195242494337034,
            "channel": 788454671684468771,
            "thread": True,
            "title": "Vocation Info"
        },
        {
            "test_channel": 1142195244264345670,
            "channel": 655463607030644747,
            "title": "EXP Manipulation",
        },
        {
            "test_channel": 1142195245661032479,
            "channel": 706892011718049802,
            "title": "Seed Farming",
        },
        {
            "test_channel": 1142195247158411274,
            "channel": 691066485279424582,
            "title": "Alchemy",
        },
        {
            "test_channel": 1142195248429269022,
            "channel": 766039065849495574,
            "thread": True,
            "title": "Quests List"
        },
        {
            "test_channel": 1142195249721118780,
            "channel": 688861170236391626,
            "title": "Hoimi Table",
        },
        {
            "test_channel": 1142195251159765044,
            "channel": 695401106305712228,
            "title": "Accolades",
        },
        {
            "test_channel": 1142195255446356030,
            "channel": 655392079819833354,
            "title": "Other Info"
        }
    ]

    large_messages = []

    for migration in reversed(migrations):
        if test_mode:
            migration["channel"] = migration["test_channel"]

        if migration.get("thread", False):
            all_messages = []

            archived_threads = await bot.get_channel(migration["channel"]).archived_threads().flatten()
            for thread in archived_threads:
                messages = await thread.history().flatten()
                messages.sort(key=lambda message: message.created_at)
                all_messages.append(messages)

            all_messages.sort(key=lambda messages: messages[0].created_at)

            first_message_too_long = True
            while first_message_too_long:
                try:
                    post = await bot.get_channel(resources_channel).create_thread(migration["title"],
                                                                                  all_messages[0][0].content)
                    message = await post.fetch_message(post.id)
                    await message.edit(files=[await f.to_file() for f in all_messages[0][0].attachments])
                    first_message_too_long = False
                except discord.errors.HTTPException as ex:
                    if "Must be 2000 or fewer in length." in str(ex):
                        large_messages.append(all_messages[0][0])
                        all_messages[0] = all_messages[0][1:]

            all_messages[0] = all_messages[0][1:]

            for t, messages in enumerate(all_messages):
                for i, message in enumerate(messages):
                    try:
                        await post.send(content=message.content,
                                        files=[await f.to_file() for f in message.attachments])
                    except discord.errors.HTTPException as ex:
                        if "Must be 2000 or fewer in length." in str(ex):
                            large_messages.append(message)

            await post.edit(locked=True)

            embed = create_embed("Migrated messages from <#%s> to <#%s>." % (migration["channel"], post.id))
            await ctx.send(embed=embed)

        else:
            messages = await bot.get_channel(migration["channel"]).history().flatten()
            messages.sort(key=lambda message: message.created_at)

            first_message_too_long = True
            while first_message_too_long:
                try:
                    if migration["title"] == "Accolades":
                        first_part = """**Game Completion Accolades In order of Priority**:
```yml
Light-Speed Champion - clear time under 12 hours
Jot to Trot - clear time 12-19 hours
Sleeper on the Job - clear time 228+ hours
Easy Rider - clear time 152-227:59 hours
Exterminator - win 1500 battles
Shopaholic - wardrobe collection at 50%
Pacifist - 250 or fewer battles
Socialite - multiplayer time is 50%+ of total time played
Philanthropist - 60 quests cleared
Cartographer - 30 grottos cleared
Mighty Inviter - 50 tags (or maybe it's multiplayer sessions)
Entitled Adventurer - 60 accolades
Completely Potty - alchemy 120 times
Zoologist - defeated monster list 75%+
Punchbag - party wiped out 24+ times
Snappy Dresser - wardrobe collection at 38-49%
Recipe Researcher - recipes at 30%+
Moneybags - 90000+ gold (carried money + bank)
Grievous Angel - party wiped out 16-23 times
Monster Masher - 1000-1499 battles
Fleet Completer - clear time 19-26:59 hours
Steady Eddie/Edwina - clear time 76-151:59 hours
Party Hopper - multiplayer is 30% but less than 50% total time played
Immaculate Completion - party wiped out 0 times
Guardian Angel/Lionheart/Sent from Above/Watched-over One/Storied Saviour: Default titles. They depend on your class/level when completing.```"""
                        second_part = """**Grotto Accolades**:
```yml
1: Celestial Sentinel -- Awarded to xxx on the occasion of his/her victory over various renowned denizens of the depths.
[Defeat all Legacy Bosses.]

2: Heralded Hero/Heralded Heroine -- Awarded to xxx to commemorate his/her victory over a grotto boss of level 25 or above.

3: Superhero/Superheroine -- Awarded to xxx to commemorate his/her victory over a grotto boss of level 50 or above.

4: Heavenly Hero/Heavenly Heroine -- Awarded to xxx to commemorate his/her victory over a grotto boss of level 75 or above.

5: Legendary Hero/Legendary Heroine -- Awarded to xxx to commemorate his/her victory over a grotto boss of level 99.

6: Spelunker -- Presented to xxx for clearance of a grotto of level 25 or above.

7: Spunky Spelunker -- Presented to xxx for clearance of a grotto of level 50 or above.

8: Spelunking Specialist -- Presented to xxx for clearance of a grotto of level 75 or above.

9: Supreme Spelunker -- Presented to xxx for clearance of a grotto of level 99.

10: Cave Dweller -- Awarded to xxx on the occasion of his/her 10th grotto clearance.

11: Cave Craver -- Awarded to xxx on the occasion of his/her 50th grotto clearance.

12: From Cradle to Cave -- Awarded to xxx on the occasion of his/her 100th grotto clearance.

13: Stalag Mighty -- Awarded to xxx on the occasion of his/her 500th grotto clearance.

14: Caving Lunatic -- The Cavers' Cooperative would like to congratulate xxx for the outstanding achievement of completing 1000 grottoes.```"""

                        post = await bot.get_channel(resources_channel).create_thread(migration["title"],
                                                                                      first_part)
                        await post.send(content=second_part)
                    else:
                        post = await bot.get_channel(resources_channel).create_thread(migration["title"],
                                                                                      messages[0].content)
                        message = await post.fetch_message(post.id)
                        await message.edit(files=[await f.to_file() for f in messages[0].attachments])
                    first_message_too_long = False
                except discord.errors.HTTPException as ex:
                    if "Must be 2000 or fewer in length." in str(ex):
                        large_messages.append(messages[0])
                        messages = messages[1:]

            for message in messages[1:]:
                try:
                    await post.send(content=message.content, files=[await f.to_file() for f in message.attachments])
                except discord.errors.HTTPException as ex:
                    if "Must be 2000 or fewer in length." in str(ex):
                        large_messages.append(message)

            await post.edit(locked=True)

            embed = create_embed("Migrated messages from <#%s> to <#%s>." % (migration["channel"], post.id))
            await ctx.send(embed=embed)

    if large_messages:
        desc = ""
        for message in large_messages:
            desc += "%s\n" % message.jump_url

        embed = create_embed("The following messages were too large to migrate.", desc)
        await ctx.send(embed=embed)

    embed = create_embed("Finished migration.")
    await ctx.followup.send(embed=embed)


@bot.command(name="migrate_challenges")
async def _migrate_challenges(ctx):
    await ctx.defer()

    test_mode = os.getenv("TEST_MODE", "FALSE").lower() == "true"

    test_challenges_channel = 1143641065560227910
    challenges_channel = 1143670710443716680

    if test_mode:
        challenges_channel = test_challenges_channel

    migrations = [
        {
            "test_channel": 1142195226312704061,
            "channel": 1020384998567706694,
            "title": "Challenges"
        },
        {
            "test_channel": 1142195227742969877,
            "channel": 724610856565997599,
            "title": "Challenge Runs"
        }
    ]

    large_messages = []

    for migration in reversed(migrations):
        if test_mode:
            migration["channel"] = migration["test_channel"]

        archived_threads = await bot.get_channel(migration["channel"]).archived_threads().flatten()
        for thread in archived_threads:
            messages = await thread.history().flatten()
            messages.sort(key=lambda message: message.created_at)

            first_message_too_long = True
            while first_message_too_long:
                try:
                    post = await bot.get_channel(challenges_channel).create_thread(
                        migration["title"] + " - " + thread.name.replace(" " + migration["title"], ""), messages[0].content)
                    message = await post.fetch_message(post.id)
                    await message.edit(files=[await f.to_file() for f in messages[0].attachments])
                    first_message_too_long = False
                except discord.errors.HTTPException as ex:
                    if "Must be 2000 or fewer in length." in str(ex):
                        large_messages.append(messages[0])
                        messages = messages[1:]

            messages = messages[1:]

            for i, message in enumerate(messages):
                try:
                    await post.send(content=message.content,
                                    files=[await f.to_file() for f in message.attachments])
                except discord.errors.HTTPException as ex:
                    if "Must be 2000 or fewer in length." in str(ex):
                        large_messages.append(message)

            await post.edit(locked=True)

            embed = create_embed("Migrated messages from <#%s> to <#%s>." % (thread.id, post.id))
            await ctx.send(embed=embed)

    if large_messages:
        desc = ""
        for message in large_messages:
            desc += "%s\n" % message.jump_url

        embed = create_embed("The following messages were too large to migrate.", desc)
        await ctx.send(embed=embed)

    embed = create_embed("Finished migration.")
    await ctx.followup.send(embed=embed)


async def get_songs(ctx: discord.AutocompleteContext):
    return [song for song in parsers.songs if ctx.value.lower() in song.lower()]


@bot.command(name="song", description="Plays a song.")
async def _song(ctx, song_name: Option(str, "Song Name", autocomplete=get_songs, required=True)):
    await song(ctx, song_name)


@bot.command(name="songs_all", description="Plays all songs.")
async def _all_songs(ctx):
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

        await ctx.respond("Playing all songs. Please wait...")

        with open("data/songs.json", "r", encoding="utf-8") as fp:
            data = json.load(fp)
        songs = data["songs"]

        if voice_client is None:
            voice_client = await bot.get_channel(channel).connect()

        message = None
        for index, s in enumerate(songs):
            if not voice_client.is_connected():
                break

            song = parsers.Song.from_dict(s)
            await play(ctx, voice_client, song, channel)

            embed = create_embed("Playing all songs. Currently playing `%s` in <#%s>" % (song.title, channel))
            try:
                await message.edit(embed=embed)
            except:
                message = await ctx.send(embed=embed)

            while voice_client.is_playing():
                await sleep(1)
        await voice_client.disconnect()
    else:
        embed = create_embed("I'm already playing a song. Please wait until it's finished.")
        return await ctx.respond(embed=embed, ephemeral=True)


@bot.command(name="stop", description="Stops playing a song.")
async def _stop_song(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=bot.get_guild(guild_id))
    if voice_client is None or not voice_client.is_playing():
        embed = create_embed("I'm not playing a song.")
        return await ctx.respond(embed=embed, ephemeral=True)

    await voice_client.disconnect()

    embed = create_embed("Stopped playing.")
    await ctx.respond(embed=embed)


@bot.command(name="parse_quests", description="Parses the quests.")
async def _parse_quests(ctx):
    await ctx.defer()

    quests = []
    channel = bot.get_channel(quests_channel)
    archived_threads = await channel.archived_threads().flatten()
    for thread in archived_threads:
        messages = await thread.history().flatten()
        for message in messages:
            quests.append(parsers.parse_regex(parsers.Quest, message.content))

    data = {
        "quests": sorted(quests, key=lambda quest: quest["number"])
    }
    with open("data/quests.json", "w+", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2)

    embed = create_embed("%i Quests Parsed Successfully" % len(quests))
    await ctx.followup.send(embed=embed)


@bot.command(name="quest", description="Sends info about a quest.")
async def _quest(ctx, quest_number: Option(int, "Quest Number (1-184)", required=True)):
    with open("data/quests.json", "r", encoding="utf-8") as fp:
        data = json.load(fp)

    quests = data["quests"]
    index = quest_number - 1
    if index >= len(quests) or index < 0:
        embed = create_embed("No quest found with the number `%s`. Please check number and try again." % quest_number)
        return await ctx.respond(embed=embed)

    quest = parsers.Quest.from_dict(quests[index])

    title = ":star: Quest #%i - %s :star:" % (quest.number, quest.name) if quest.story \
        else "Quest #%i - %s" % (quest.number, quest.name)
    color = discord.Color.gold() if quest.story else discord.Color.green()
    embed = create_embed(title, color=color)
    if quest.location != "":
        embed.add_field(name="Location", value=quest.location, inline=False)
    if quest.request != "":
        embed.add_field(name="Request", value=quest.request, inline=False)
    if quest.solution != "":
        embed.add_field(name="Solution", value="||%s||" % quest.solution, inline=False)
    if quest.reward != "":
        embed.add_field(name="Reward", value=quest.reward, inline=False)
    embed.add_field(name="Repeat", value="Yes" if quest.repeat else "No", inline=False)
    embed.add_field(name="Pre-reqs", value=quest.prerequisite, inline=False)

    await ctx.respond(embed=embed)


@bot.command(name="translate", description="Translate a word or phrase to a different language.")
async def _translate(ctx,
                     phrase: Option(str, "Word or Phrase (Ex. Copper Sword)", required=True),
                     language_input: Option(str, "Input Language (Ex. English)", choices=parsers.translation_languages,
                                            required=True),
                     language_output: Option(str, "Output Language (Ex. Japanese)",
                                             choices=parsers.translation_languages, required=False)):
    data = {
        "translations": []
    }
    for file in parsers.translation_files:
        with open(file, "r", encoding="utf-8") as fp:
            data["translations"] += json.load(fp)["translations"]

    translations = data["translations"]

    index = next(filter(lambda r: clean_text(r[parsers.translation_languages_simple[
        parsers.translation_languages.index(language_input)]].lower()) == clean_text(phrase.lower()), translations),
                 None)
    if index is None:
        embed = create_embed("No word or phrase found matching `%s`. Please check phrase and try again." % phrase,
                             error="Any errors? Want to contribute? Please speak to %s" % dev_tag)
        return await ctx.respond(embed=embed)

    translation = parsers.Translation.from_dict(index)
    all_languages = [
        translation.english,
        translation.japanese,
        translation.spanish,
        translation.french,
        translation.german,
        translation.italian
    ]

    title = "Translation of: %s" % titlecase(all_languages[parsers.translation_languages.index(language_input)])
    color = discord.Color.green()
    embed = create_embed(title, color=color, error="Any errors? Want to contribute? Please speak to %s" % dev_tag)
    if language_output is not None:
        value = titlecase(all_languages[parsers.translation_languages.index(language_output)])
        if value != "":
            embed.add_field(name=language_output, value=value, inline=False)
        else:
            embed = create_embed("The word or phrase `%s` has not been translated to `%s`." % (phrase, language_output),
                                 error="Any errors? Want to contribute? Please speak to %s" % dev_tag)
            return await ctx.respond(embed=embed)
    else:
        for language, translation in zip(parsers.translation_languages, all_languages):
            if translation != "":
                embed.add_field(name=language, value=titlecase(translation), inline=False)

    await ctx.respond(embed=embed)


@bot.command(name="grotto_translate", description="Translate a grotto from English to a different language.")
async def _translate_grotto_english(ctx,
                                    material: Option(str, "Material (Ex. Granite)", choices=parsers.grotto_prefixes,
                                                     required=True),
                                    environment: Option(str, "Environment (Ex. Tunnel)",
                                                        choices=parsers.grotto_environments,
                                                        required=True),
                                    suffix: Option(str, "Suffix (Ex. Woe)", choices=parsers.grotto_suffixes,
                                                   required=True),
                                    language_output: Option(str, "Output Language (Ex. Japanese)",
                                                            choices=parsers.translation_languages, required=False),
                                    level: Option(int, "Level (Ex. 1)", required=False),
                                    location: Option(str, "Location (Ex. 05)", required=False)):
    await translate_grotto_command(ctx, material, environment, suffix, 0, language_output, level, location)


@bot.command(name="grotto_translate_japanese", description="Translate a grotto from Japanese to a different language.")
async def _translate_grotto_japanese(ctx,
                                     material: Option(str, "Material (Ex. Granite)",
                                                      choices=parsers.grotto_prefixes_japanese, required=True),
                                     suffix: Option(str, "Suffix (Ex. Woe)", choices=parsers.grotto_suffixes_japanesh,
                                                    required=True),
                                     environment: Option(str, "Environment (Ex. Tunnel)",
                                                         choices=parsers.grotto_environments_japanesh, required=True),
                                     language_output: Option(str, "Output Language (Ex. Japanese)",
                                                             choices=parsers.translation_languages, required=False),
                                     level: Option(int, "Level (Ex. 1)", required=False),
                                     location: Option(str, "Location (Ex. 05)", required=False)):
    await translate_grotto_command(ctx, material, environment, suffix, 1, language_output, level, location)


@bot.command(name="grotto_translate_spanish", description="Translate a grotto from Spanish to a different language.")
async def _translate_grotto_spanish(ctx,
                                    environment: Option(str, "Environment (Ex. Tunnel)",
                                                        choices=parsers.grotto_environments_spanish, required=True),
                                    material: Option(str, "Material (Ex. Granite)",
                                                     choices=parsers.grotto_prefixes_spanish, required=True),
                                    suffix: Option(str, "Suffix (Ex. Woe)", choices=parsers.grotto_suffixes_spanish,
                                                   required=True),
                                    language_output: Option(str, "Output Language (Ex. Japanese)",
                                                            choices=parsers.translation_languages, required=False),
                                    level: Option(int, "Level (Ex. 1)", required=False),
                                    location: Option(str, "Location (Ex. 05)", required=False)):
    await translate_grotto_command(ctx, material, environment, suffix, 2, language_output, level, location)


@bot.command(name="grotto_translate_french", description="Translate a grotto from French to a different language.")
async def _translate_grotto_french(ctx,
                                   environment: Option(str, "Environment (Ex. Tunnel)",
                                                       choices=parsers.grotto_environments_french, required=True),
                                   material: Option(str, "Material (Ex. Granite)",
                                                    choices=parsers.grotto_prefixes_french, required=True),
                                   suffix: Option(str, "Suffix (Ex. Woe)", choices=parsers.grotto_suffixes_french,
                                                  required=True),
                                   language_output: Option(str, "Output Language (Ex. Japanese)",
                                                           choices=parsers.translation_languages, required=False),
                                   level: Option(int, "Level (Ex. 1)", required=False),
                                   location: Option(str, "Location (Ex. 05)", required=False)):
    await translate_grotto_command(ctx, material, environment, suffix, 3, language_output, level, location)


@bot.command(name="grotto_translate_german", description="Translate a grotto from German to a different language.")
async def _translate_grotto_german(ctx,
                                   material: Option(str, "Material (Ex. Granite)",
                                                    choices=parsers.grotto_prefixes_german, required=True),
                                   environment: Option(str, "Environment (Ex. Tunnel)",
                                                       choices=parsers.grotto_environments_german, required=True),
                                   suffix: Option(str, "Suffix (Ex. Woe)", choices=parsers.grotto_suffixes_german,
                                                  required=True),
                                   language_output: Option(str, "Output Language (Ex. English)",
                                                           choices=parsers.translation_languages, required=False),
                                   level: Option(int, "Level (Ex. 1)", required=False),
                                   location: Option(str, "Location (Ex. 05)", required=False)):
    await translate_grotto_command(ctx, material, environment, suffix, 4, language_output, level, location)


@bot.command(name="grotto_translate_italian", description="Translate a grotto from Italian to a different language.")
async def _translate_grotto_italian(ctx,
                                    environment: Option(str, "Environment (Ex. Tunnel)",
                                                        choices=parsers.grotto_environments_italian, required=True),
                                    material: Option(str, "Material (Ex. Granite)",
                                                     choices=parsers.grotto_prefixes_italian, required=True),
                                    suffix: Option(str, "Suffix (Ex. Woe)", choices=parsers.grotto_suffixes_italian,
                                                   required=True),
                                    language_output: Option(str, "Output Language (Ex. English)",
                                                            choices=parsers.translation_languages, required=False),
                                    level: Option(int, "Level (Ex. 1)", required=False),
                                    location: Option(str, "Location (Ex. 05)", required=False)):
    await translate_grotto_command(ctx, material, environment, suffix, 5, language_output, level, location)


async def translate_grotto_command(ctx, material, environment, suffix, language_input, language_output, level,
                                   location):
    await ctx.defer()

    embed, material, environment, suffix = await translate_grotto(material, environment, suffix,
                                                                  parsers.translation_languages_simple[language_input],
                                                                  language_output)
    await ctx.followup.send(embed=embed)

    if level is not None:
        await grotto_command(ctx, material, environment, suffix, level, location)


async def get_recipes(ctx: discord.AutocompleteContext):
    with open("data/recipes.json", "r", encoding="utf-8") as fp:
        data = json.load(fp)
    recipes = data["recipes"]
    results = []
    for r in recipes:
        recipe = parsers.Recipe.from_dict(r)
        if ctx.value.lower() in recipe.result.lower():
            results.append(titlecase(recipe.result))
    return results


@bot.command(name="recipe", description="Sends info about a recipe.")
async def _recipe(ctx, creation_name: Option(str, "Creation (Ex. Special Medicine)", autocomplete=get_recipes,
                                             required=True)):
    with open("data/recipes.json", "r", encoding="utf-8") as fp:
        data = json.load(fp)

    recipes = data["recipes"]

    index = next(filter(lambda r: clean_text(r["result"]) == clean_text(creation_name.lower()), recipes), None)

    if index is None:
        embed = create_embed("Ahem! Oh dear. I'm afraid I don't seem to be\nable to make anything with that particular"
                             "\ncreation name of `%s`." % creation_name, image=krak_pop_image_url)
        return await ctx.respond(embed=embed)

    recipe = parsers.Recipe.from_dict(index)

    title = ":star: %s :star:" % titlecase(recipe.result) if recipe.alchemiracle else titlecase(recipe.result)
    color = discord.Color.gold() if recipe.alchemiracle else discord.Color.green()

    if recipe.image == "":
        recipe_images_url = ""
        if recipe.type.lower() in parsers.item_types:
            recipe_images_url = item_images_url
        elif recipe.type.lower() in parsers.weapon_types:
            recipe_images_url = weapon_images_url
        elif recipe.type.lower() in parsers.armor_types:
            recipe_images_url = armor_images_url
        elif recipe.type.lower() in parsers.accessory_types:
            recipe_images_url = accessory_images_url
        elif recipe.type.lower() == "shields":
            recipe_images_url = shields_images_url

        if recipe_images_url != "":
            recipe.image = recipe_images_url % clean_text(recipe.result, False, True)
    embed = create_embed(title, color=color, image=recipe.image)

    embed.add_field(name="Type", value=recipe.type, inline=False)
    if recipe.item1 != "":
        embed.add_field(name="Item 1", value="%ix %s" % (recipe.qty1, titlecase(recipe.item1)), inline=False)
    if recipe.item2 != "":
        embed.add_field(name="Item 2", value="%ix %s" % (recipe.qty2, titlecase(recipe.item2)), inline=False)
    if recipe.item3 != "":
        embed.add_field(name="Item 3", value="%ix %s" % (recipe.qty3, titlecase(recipe.item3)), inline=False)
    if recipe.notes != "":
        embed.add_field(name="Notes", value="%s" % recipe.notes, inline=False)

    await ctx.respond(embed=embed)


async def get_monsters(ctx: discord.AutocompleteContext):
    with open("data/monsters.json", "r", encoding="utf-8") as fp:
        data = json.load(fp)
    monsters = data["monsters"]
    results = []
    for m in monsters:
        monster = parsers.Monster.from_dict(m)
        if ctx.value.lower() in monster.name.lower() or ctx.value.lower() in monster.number.lower():
            results.append(monster.number + " - " + titlecase(monster.name))
    return results


@bot.command(name="monster", description="Sends info about a monster.")
async def _monster(ctx,
                   monster_identifier: Option(str, "Monster Identifier (Ex. Slime or 1)", autocomplete=get_monsters,
                                              required=True)):
    with open("data/monsters.json", "r", encoding="utf-8") as fp:
        data = json.load(fp)

    monsters = data["monsters"]

    monster_number = 0

    if " - " in monster_identifier:
        monster_number = monster_identifier.split(" - ")[0]
        indexes = list(filter(lambda r: clean_text(r["name"].lower()) == clean_text(
            monster_identifier.split(" - ")[1].lower()) or clean_text(
            r.get("altname", "").lower()) == clean_text(monster_identifier.split(" - ")[1].lower()), monsters))
    else:
        indexes = list(filter(
            lambda r: clean_text(r["name"].lower()) == clean_text(monster_identifier.lower()) or clean_text(
                r.get("altname", "").lower()) == clean_text(
                monster_identifier.lower()), monsters))
        if not indexes:
            monster_number = "#" + "%03d" % int_from_string(monster_identifier) + monster_identifier[-1] if \
                monster_identifier[-1].isalpha() else ""
            indexes = list(
                filter(lambda r: int_from_string(r["number"]) == int_from_string(monster_identifier), monsters))

    if len(indexes) == 0:
        embed = create_embed("No monster found with the identifier `%s`. Please check spelling and try again."
                             % monster_identifier)
        return await ctx.respond(embed=embed)

    proper_page = 0
    embeds = []
    for index in indexes:
        monster = parsers.Monster.from_dict(index)

        title = "%s - %s (Level: %s)" % (monster.number, titlecase(monster.name), monster.level)
        description = '''
**Family:** %s | **EXP:** %s | **Gold:** %s

**HP:** %s | **MP:** %s | **ATK:** %s | **DEF:** %s | **AGI:** %s

**Fire:** %s | **Ice:** %s | **Wind:** %s
**Blast:** %s | **Earth:** %s | **Dark:** %s | **Light:** %s

**Haunts:** %s
''' % (
            monster.family, monster.exp, monster.gold, monster.hp, monster.mp, monster.atk, monster.defn, monster.agi,
            monster.fire, monster.ice, monster.wind, monster.blast, monster.earth, monster.dark, monster.light,
            titlecase(monster.haunts)
        )
        if monster.drop1 != "":
            description += "\n**__Drop 1 | Common Drop__**\n%s\n" % titlecase(monster.drop1)
        if monster.drop2 != "":
            description += "\n**__Drop 2 | Rare Drop__**\n%s\n" % titlecase(monster.drop2)
        if monster.drop3 != "":
            description += "\n**__Drop 3__**\n%s\n" % titlecase(monster.drop3)

        if monster.image == "":
            monster.image = monster_images_url % clean_text(monster.name, False, True)

        embed = create_embed(title, description, image=monster.image)
        embeds.append(embed)

        if monster_number != 0 and monster_number == monster.number:
            proper_page = len(embeds) - 1

    if len(embeds) > 1:
        paginator = create_paginator(embeds, None)
        await paginator.respond(ctx.interaction)
        await paginator.goto_page(proper_page)
    else:
        await ctx.respond(embed=embeds[0])


@bot.command(name="character", description="Sends info for a randomly-generated character.")
async def _character(ctx):
    gender = random.choice(["Male", "Female"])
    body_type = random.randint(1, 5)
    hair_style = random.randint(1, 10)
    hair_color = random.randint(1, 10)
    face_style = random.randint(1, 10)
    skin_tone = random.randint(1, 8)
    eye_color = random.randint(1, 8)

    keys = {
        "headcolor": skin_tone,
        "hairnum": hair_style,
        "haircolor": hair_color,
        "eyecolor": eye_color,
    }

    remapped_eyes_female = {
        1: 1,
        2: 2,
        3: 3,
        4: 12,
        5: 13,
        6: 14,
        7: 15,
        8: 16,
        9: 17,
        10: 20,
    }

    remapped_eyes_male = {
        1: 4,
        2: 5,
        3: 6,
        4: 7,
        5: 8,
        6: 9,
        7: 10,
        8: 11,
        9: 18,
        10: 19,
    }

    if gender == "Male":
        keys["hairnum"] += 10
        keys["eyesnum"] = remapped_eyes_male[face_style]
    else:
        keys["eyesnum"] = remapped_eyes_female[face_style]

    description = '''
**Gender:** %s
    
**Body Type:** %s
    
**Hair Style:** %s
    
**Hair Color:** %s
    
**Face Style:** %s
    
**Skin Tone:** %s
    
**Eye Color:** %s
''' % (gender, body_type, hair_style, hair_color, face_style, skin_tone, eye_color)

    params = ""
    for key, value in keys.items():
        params += "%s=%s&" % (key, value)

    embed = create_embed("Random Character Generator", description, image=character_image_url + params[:-1])

    await ctx.respond(embed=embed)


@bot.command(name="grotto", description="Sends info about a grotto.")
async def _grotto(ctx,
                  material: Option(str, "Material (Ex. Granite)", choices=parsers.grotto_prefixes, required=True),
                  environment: Option(str, "Environment (Ex. Tunnel)", choices=parsers.grotto_environments,
                                      required=True),
                  suffix: Option(str, "Suffix (Ex. Woe)", choices=parsers.grotto_suffixes, required=True),
                  level: Option(int, "Level (Ex. 1)", required=True),
                  location: Option(str, "Location (Ex. 05)", required=False)):
    await grotto_command(ctx, material, environment, suffix, level, location)


@bot.command(name="gg", description="Sends info about a grotto with location required.")
async def _grotto_location(ctx,
                           material: Option(str, "Material (Ex. Granite)", choices=parsers.grotto_prefixes,
                                            required=True),
                           environment: Option(str, "Environment (Ex. Tunnel)", choices=parsers.grotto_environments,
                                               required=True),
                           suffix: Option(str, "Suffix (Ex. Woe)", choices=parsers.grotto_suffixes, required=True),
                           level: Option(int, "Level (Ex. 1)", required=True),
                           location: Option(str, "Location (Ex. 05)", required=True)):
    await grotto_command(ctx, material, environment, suffix, level, location)


@bot.event
async def on_raw_reaction_add(payload):
    emoji_name = emoji.demojize(payload.emoji.name)
    channel = bot.get_channel(payload.channel_id)
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)

    rules_channels = [
        bot.get_channel(rules_channel_en),
        bot.get_channel(rules_channel_fr),
        bot.get_channel(rules_channel_de),
        bot.get_channel(rules_channel_jp)
    ]

    message = await channel.fetch_message(payload.message_id)
    if message.channel == bot.get_channel(welcome_channel):
        role_id = 0
        if emoji_name == ":United_Kingdom:":
            role_id = role_en
        if emoji_name == ":France:":
            role_id = role_fr
        if emoji_name == ":Germany:":
            role_id = role_de
        if emoji_name == ":Japan:":
            role_id = role_jp

        await user.add_roles(discord.utils.get(guild.roles, id=role_id), reason="User assigned role to themselves.")

    elif message.channel in rules_channels:
        if emoji_name == ":thumbs_up:":
            await user.add_roles(discord.utils.get(guild.roles, id=role_celestrian), reason="User accepted rules.")
            await message.remove_reaction(payload.emoji, user)


@bot.event
async def on_raw_reaction_remove(payload):
    emoji_name = emoji.demojize(payload.emoji.name)
    channel = bot.get_channel(payload.channel_id)
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)

    message = await channel.fetch_message(payload.message_id)
    if message.channel == bot.get_channel(welcome_channel):
        role_id = 0
        if emoji_name == ":United_Kingdom:":
            role_id = role_en
        if emoji_name == ":France:":
            role_id = role_fr
        if emoji_name == ":Germany:":
            role_id = role_de
        if emoji_name == ":Japan:":
            role_id = role_jp

        await user.remove_roles(discord.utils.get(guild.roles, id=role_id), reason="User removed role from themselves.")


@bot.event
async def on_voice_state_update(member, before, after):
    voice_client = discord.utils.get(bot.voice_clients, guild=bot.get_guild(guild_id))
    if voice_client is None:
        return
    music_voice_channel = voice_client.channel
    if len(music_voice_channel.members) <= 1:
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()


bot.run(token)
