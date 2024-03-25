from utils import create_embed, server_invite_url, dev_id, logo_url, website_url


def help_function():
    description = '''
    A bot created by <@%s> for The Quester's Rest (<%s>).

    **/character** - *Generate a random character*
    **/gg** - *Get grotto info (location required)*
    **/grotto** - *Get grotto info*
    **/monster** - *Get monster info*
    **/quest** - *Get quest info*
    **/recipe** - *Get an item's recipe*
    **/song** - *Play a song*
    **/songs_all** - *Play all songs*
    **/stop** - *Stop playing songs*
    **/translate** - *Translate a word or phrase*
    **/grotto_translate(\_[language])** - *Translate a grotto name*

    **/help** - *Displays this message*
    ''' % (dev_id, server_invite_url)

    return create_embed("Collapsus v2 Help [Click For Server Website]", description=description, error="",
                        image=logo_url, url=website_url)
