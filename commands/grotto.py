import io
import json

import aiohttp
from parsel import Selector
from titlecase import titlecase

import parsers
import discord

from utils import create_paginator, create_collage, create_embed, grotto_search_url, dev_tag


async def grotto_command(ctx, material, environment, suffix, level, location):
    if not ctx.response.is_done():
        await ctx.defer()

    embeds, files = await grotto_func(material, environment, suffix, level, location)

    if len(embeds) > 1:
        paginator = create_paginator(embeds, files)
        await paginator.respond(ctx.interaction)
    else:
        if len(embeds) == 1:
            embed = embeds[0]
            fs = [file["file"] for file in files if file["id"] == 0]
            file_name = "collages/collage0.png"
            create_collage(fs, file_name)
            with open(file_name, 'rb') as fp:
                data = io.BytesIO(fp.read())
            file = discord.File(data, file_name.removeprefix("collages/"))
            embed.set_image(url="attachment://%s" % file_name.removeprefix("collages/"))
        else:
            embed = create_embed("No grotto found. Please check parameters and try again.")
            file = None

        if file is not None:
            await ctx.followup.send(embed=embed, file=file)
        else:
            await ctx.followup.send(embed=embed)


async def grotto_func(material, environment, suffix, level, location):
    async with aiohttp.ClientSession() as session:
        params = {
            "search": "Search",
            "prefix": str(parsers.grotto_prefixes.index(titlecase(material)) + 1),
            "envname": str(parsers.grotto_environments.index(titlecase(environment)) + 1),
            "suffix": str(parsers.grotto_suffixes.index(suffix) + 1),
            "level": str(level),
        }

        if location is not None:
            try:
                params["loc"] = str(int(location, base=16))
            except ValueError:
                pass

        async with session.get(grotto_search_url, params=params) as response:
            text = await response.text()
            selector = Selector(text=text)
            divs = selector.xpath('//div[@class="inner"]//text()')
            grottos = divs.getall()

            embeds = []
            files = []

            for parsed in parsers.create_grotto(grottos):
                special = parsers.is_special(parsed)
                color = discord.Color.gold() if special else discord.Color.green()
                embed = create_embed(None, color=color)

                if special:
                    parsed = parsed[1:]

                zipped = zip(range(len(parsed)), parsers.grotto_keys, parsed)

                for i, key, value in zipped:
                    if key == "Name":
                        if special:
                            value = ":star: %s :star:" % value
                        embed.title = "%s\n[Click For Full Info]" % value
                    else:
                        if key == "Seed":
                            value = str(value).zfill(4)
                        if key == "Chests":
                            values = [str(x) for x in parsed[i:i + 10]]
                            chests = list(zip(parsers.grotto_ranks, values))
                            value = ", ".join([': '.join(x) for x in chests])
                        if key == "Locations":
                            values = [str(x).zfill(2) for x in parsed[i + 9:]]
                            for v in values:
                                files.append({"id": len(embeds), "file": "grotto_images/%s.png" % v})
                            value = ', '.join(values)
                        embed.add_field(name=key, value=value, inline=False)
                embed.url = str(response.url)
                embeds.append(embed)

        return embeds, files


async def translate_grotto(material, environment, suffix, language_input, language_output):
    with open("data/grottos_translated.json", "r", encoding="utf-8") as fp:
        data = json.load(fp)

    translations = data["translations"]

    translation = parsers.Translation

    translation_english = []
    translation_japanese = []
    translation_spanish = []
    translation_french = []
    translation_german = []
    translation_italian = []

    phrases = [material, environment, suffix]
    for p in phrases:
        index = next(filter(lambda r: r[language_input].lower() == p.lower(), translations), None)

        translation = parsers.Translation.from_dict(index)

        translation_english.append(translation.english)
        translation_japanese.append(translation.japanese)
        translation_spanish.append(translation.spanish)
        translation_french.append(translation.french)
        translation_german.append(translation.german)
        translation_italian.append(translation.italian)

    translation.english = "%s %s %s" % (translation_english[0], translation_english[1], translation_english[2])
    translation.japanese = "%s%s%s" % (translation_japanese[0], translation_japanese[2], translation_japanese[1])
    translation.spanish = "%s %s %s" % (translation_spanish[1], translation_spanish[0], translation_spanish[2])
    translation.french = "%s %s %s" % (translation_french[1], translation_french[0], translation_french[2])
    translation.german = "%s%s %s" % (translation_german[0], translation_german[1], translation_german[2])
    translation.italian = "%s %s %s" % (translation_italian[1], translation_italian[0], translation_italian[2])

    all_languages = [
        translation.english,
        translation.japanese,
        translation.spanish,
        translation.french,
        translation.german,
        translation.italian
    ]

    title = "Translation of: %s" % titlecase(all_languages[parsers.translation_languages_simple.index(language_input)])
    color = discord.Color.green()
    embed = create_embed(title, color=color, error="Any errors? Want to contribute? Please speak to %s" % dev_tag)
    if language_output is not None:
        value = all_languages[parsers.translation_languages.index(language_output)]
        if value != "":
            embed.add_field(name=language_output, value=value, inline=False)
    else:
        for language, translation in zip(parsers.translation_languages, all_languages):
            if translation != "":
                embed.add_field(name=language, value=translation, inline=False)

    return embed, translation_english[0], translation_english[1], translation_english[2]