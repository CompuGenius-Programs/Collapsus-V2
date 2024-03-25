import io
import math

import discord
from PIL import Image
from discord.ext.pages import Paginator, Page as _Page


dev_id = 496392770374860811
dev_tag = "@CompuGeniusPrograms"
dev_paypal = "paypal.me/cgprograms | venmo.com/CompuGeniusCode"

guild_id = 655390550698098700
testing_channel = 973619817317797919

quests_channel = 766039065849495574

welcome_channel = 965688638295924766
rules_channel_en = 688480621856686196
rules_channel_fr = 965694046049800222
rules_channel_de = 965693961907875850
rules_channel_jp = 965693827568529448

role_en = 879436700256964700
role_fr = 965696709290262588
role_de = 965696853951795221
role_jp = 859563030220374057
role_celestrian = 655438935278878720

grotto_bot_channel = 845339551173050389

stream_channel = 655390551138631704

logo_url = "https://cdn.discordapp.com/emojis/856330729528361000.png"
website_url = "https://dq9.carrd.co"
server_invite_url = "https://discord.gg/DQ9"

grotto_search_url = "https://www.yabd.org/apps/dq9/grottosearch.php"

character_image_url = "https://www.woodus.com/den/games/dq9ds/characreate/index.php?"

monster_images_url = "https://www.woodus.com/den/gallery/graphics/dq9ds/monster/%s.webp"

krak_pop_image_url = "https://cdn.discordapp.com/attachments/698157074420334612/982389321506099300/unknown.png"
item_images_url = "https://www.woodus.com/den/gallery/graphics/dq9ds/item/%s.png"
weapon_images_url = "https://www.woodus.com/den/gallery/graphics/dq9ds/weapon/%s.png"
armor_images_url = "https://www.woodus.com/den/gallery/graphics/dq9ds/armor/%s.png"
shields_images_url = "https://www.woodus.com/den/gallery/graphics/dq9ds/shield/%s.png"
accessory_images_url = "https://www.woodus.com/den/gallery/graphics/dq9ds/accessory/%s.png"


def int_from_string(string):
    integer = ''.join(filter(str.isdigit, string))
    if integer != "":
        return int(integer)
    else:
        return ""


def clean_text(text, remove_spaces=True, url=False):
    text = text.lower().replace("'", "").replace("’", "").replace("ñ", "n").replace("ó", "o").replace(
        ".", "")
    text = text.replace("-", "_") if url else text.replace("-", "")
    if remove_spaces:
        text = text.replace(" ", "")
    else:
        text = text.replace(" ", "_")

    return text


class Page(_Page):
    def update_files(self) -> list[discord.File] | None:
        """Updates :class:`discord.File` objects so that they can be sent multiple
        times. This is called internally each time the page is sent.
        """
        for file in self._files:
            if file.fp.closed and (fn := getattr(file.fp, "name", None)):
                file.fp = open(fn, "rb")
            file.reset()
            file.fp.close = lambda: None
        return self._files


def create_paginator(embeds, files):
    pages = []
    for entry in embeds:
        if files is None:
            page = Page(embeds=[entry])
        else:
            fs = [file["file"] for file in files if file["id"] == embeds.index(entry)]
            file_name = "collages/collage%s.png" % embeds.index(entry)
            create_collage(fs, file_name)
            with open(file_name, 'rb') as fp:
                data = io.BytesIO(fp.read())
            file = discord.File(data, file_name.removeprefix("collages/"))
            entry.set_image(url="attachment://%s" % file_name.removeprefix("collages/"))
            page = Page(embeds=[entry], files=[file])
        pages.append(page)
    return Paginator(pages=pages)


def create_collage(files, file_name):
    columns = math.ceil(math.sqrt(len(files)))
    rows = math.ceil(len(files) / columns)
    collage = Image.new("RGBA", (128 * columns, 96 * rows))
    index = 0
    for row in range(rows):
        for col in range(columns):
            if index < len(files):
                image = Image.open(files[index])
                collage.paste(image, (128 * col, 96 * row))
                index += 1

    collage.save(file_name)


def create_embed(title, description=None, color=discord.Color.green(),
                 footer="Consider supporting the developer at %s" % dev_paypal,
                 error="Any errors? Please report to %s" % dev_tag,
                 image="", *, url="", author=""):
    embed = discord.Embed(title=title, description=description, url=url, color=color)
    embed.set_footer(text="%s\n%s" % (footer, error))
    if image != "":
        embed.set_image(url=image)
    embed.set_author(name=author)
    return embed
