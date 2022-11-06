import re
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Recipe:
    """Class for a recipe."""
    type: str = ""
    result: str = ""
    qty1: int = ""
    item1: str = ""
    qty2: int = ""
    item2: str = ""
    qty3: int = ""
    item3: str = ""
    alchemiracle: bool = False
    notes: str = ""
    image: str = ""


@dataclass_json
@dataclass
class Quest:
    """Class for a quest."""
    number: int = 0
    name: str = ""
    story: bool = False
    location: str = ""
    request: str = ""
    solution: str = ""
    reward: str = ""
    prerequisite: str = ""
    repeat: bool = False


@dataclass_json
@dataclass
class Monster:
    """Class for a monster."""
    number: int = 0
    num_str: str = ""
    level: int = 0
    name: str = ""
    exp: int = 0
    gold: int = 0
    family: str = ""
    hp: int = 0
    mp: int = 0
    atk: int = 0
    defn: int = 0
    agi: int = 0
    fire: int = 0
    ice: int = 0
    wind: int = 0
    blast: int = 0
    earth: int = 0
    dark: int = 0
    light: int = 0
    dazzle: int = 0
    sleep: int = 0
    death: int = 0
    haunts: str = ""
    drop1: str = ""
    drop2: str = ""
    drop3: str = ""
    image: str = ""


@dataclass_json
@dataclass
class Translation:
    """Class for a translation."""
    english: str = ""
    japanese: str = ""
    spanish: str = ""
    french: str = ""
    german: str = ""
    italian: str = ""


translation_languages = [
    "English",
    "Japanese (日本語)",
    "Spanish (Español)",
    "French (Français)",
    "German (Deutsch)",
    "Italian (Italiano)"
]

translation_languages_simple = [
    "english",
    "japanese",
    "spanish",
    "french",
    "german",
    "italian"
]

translation_files = [
    "items_translated.json",
    "grottos_translated.json",
    "accolades_translated.json",
    "places_translated.json",
    "attributes_translated.json"
]

grotto_prefixes = ['Clay', 'Rock', 'Granite', 'Basalt', 'Graphite', 'Iron', 'Copper', 'Bronze', 'Steel', 'Silver',
                   'Gold', 'Platinum', 'Ruby', 'Emerald', 'Sapphire', 'Diamond']
grotto_environments = ['Cave', 'Tunnel', 'Mine', 'Crevasse', 'Marsh', 'Lair', 'Icepit', 'Lake', 'Crater', 'Path',
                       'Snowhall', 'Moor', 'Dungeon', 'Crypt', 'Nest', 'Ruins', 'Tundra', 'Waterway', 'World',
                       'Abyss', 'Maze', 'Glacier', 'Chasm', 'Void']
grotto_suffixes = ['of Joy', 'of Bliss', 'of Glee', 'of Doubt', 'of Woe', 'of Dolour', 'of Regret', 'of Bane',
                   'of Fear', 'of Dread', 'of Hurt', 'of Gloom', 'of Doom', 'of Evil', 'of Ruin', 'of Death']

grotto_prefixes_japanesh = ['はかなき', 'ちいさな', 'うす暗き', 'ゆらめく', 'ざわめく', 'ねむれる', '怒れる', '呪われし', '放たれし',
                            'けだかき', 'わななく', '残された', '見えざる', 'あらぶる', 'とどろく', '大いなる']
grotto_environments_japanesh = ['洞くつ', '地下道', '坑道', '雪道', '沼地', 'アジト', '氷穴', '地底湖', '火口', '道', '雪原',
                                '湿原', '牢ごく', '墓場', '巣', '遺跡', '凍土', '水脈', '世界', '奈落', '迷宮',
                                '氷河', '眠る地', 'じごく']
grotto_suffixes_japanesh = ['花の', '岩の', '風の', '空の', '獣の', '夢の', '影の', '大地の', '運命の', '魂の', '闇の', '光の',
                            '魔神の', '星々の', '悪霊の', '神々の']

grotto_prefixes_spanish = ['de Arcilla', 'de Roca', 'de Granito', 'de Basalto', 'de Grafita', 'de Hierro', 'de Cobre',
                           'de Bronce', 'de Acero', 'de Plata', 'de Oro', 'de Platino', 'de Rubí', 'de Esmeralda',
                           'de Zafiro', 'de Diamante']
grotto_environments_spanish = ['Cueva', 'Galería', 'Mina', 'Sima', 'Marisma', 'Guarida', 'Sima Helada', 'Laguna',
                               'Boca', 'Galería', 'Nevera', 'Landa', 'Mazmorra', 'Cripta', 'Covacha', 'Ruina', 'Tundra',
                               'Rivera', 'Guarida', 'Tierra', 'Cuenca', 'Laberinto', 'Madriguera', 'Sima']
grotto_suffixes_spanish = ['de la Alegría', 'de la Felicidad', 'del Júbilo', 'de la Duda', 'de la Congoja', 'del Dolor',
                           'de los Lamentos', 'de la Ruina', 'del Miedo', 'del Terror', 'del Sufrimiento',
                           'de la Melancolía', 'del Sino', 'del Mal', 'de la Desgracia', 'de la Muerte']

grotto_prefixes_french = ['d’argile', 'de pierre', 'de granit', 'de basalte', 'de graphite', 'de fer', 'de cuivre',
                          'de bronze', 'd’acier', 'd’argent', 'd’or', 'de platine', 'de rubis', 'd’émeraude',
                          'de saphir', 'de diamant']
grotto_environments_french = ['Grotte', 'Tunnel', 'Mine', 'Crevasse', 'Marais', 'Repaire', 'Puits', 'Lac', 'Cratėre',
                              'Sentier', 'Fosse', 'Lande', 'Donjon', 'Crypte', 'Vestiges', 'Steppe',
                              'Riviėre', 'Taniėre', 'Monde', 'Gouffre', 'Déale', 'Glacier', 'Faille', 'Néant']
grotto_suffixes_french = ['de la Joie', 'de la Félicité', 'de l’Allégresse', 'de l’Incertitude', 'de la Détresse',
                          'de l’Affliction', 'du Regret', 'du Malheur', 'de la Peur', 'de l’Effroi', 'de la Souffrance',
                          'de la Mélancolie', 'de l’Infortune', 'de l’Horreur', 'du Désastre', 'de la Mort']

grotto_prefixes_german = ['Lehm-', 'Fels-', 'Granit-', 'Basalt-', 'Graphit-', 'Eisen-', 'Kupfer-', 'Bronze-', 'Stahl-',
                          'Silber-', 'Gold-', 'Platin-', 'Rubin-', 'Smaragd-', 'Saphir-', 'Diamant-']
grotto_environments_german = ['Höhle', 'Tunnel', 'Mine', 'Spalte', 'Marsch', 'Versteck', 'Eisgrube', 'See', 'Krater',
                              'Pfad', 'Eispalast', 'Moor', 'Kerker', 'Krypta', 'Ruine', 'Tundra', 'Gewässer',
                              'Nest', 'Welt', 'Abgrund', 'Labyrinth', 'Gletscher', 'Kluft', 'Leere']
grotto_suffixes_german = ['der Freude', 'der Seligkeit', 'der Wonne', 'des Zweifels', 'des Grams', 'des Schmerzes',
                          'der Reue', 'des Verderbens', 'der Furcht', 'des Grauens', 'der Qual', 'der Trübsal',
                          'des Schicksals', 'des Bösen', 'des Ruins', 'des Todes']

grotto_prefixes_italian = ['Argilla', 'Roccia', 'Granito', 'Basalto', 'Grafite', 'Ferro', 'Rame', 'Bronzo', 'Acciaio',
                           'Argento', 'Oro', 'Platino', 'Rubino', 'Smeraldo', 'Zaffiro', 'Diamante']
grotto_environments_italian = ['Grotta', 'Galleria', 'Miniera', 'Crepaccio', 'Palude', 'Tana', 'Abisso', 'Lago',
                               'Cratere', 'Sentiero', 'Dedalo', 'Brughiera', 'Segreta', 'Cripta', 'Rovina',
                               'Tundra', 'Canale', 'Nido', 'Reame', 'Abisso', 'Dedalo', 'Ghiacciaio', 'Spelonca',
                               'Vuoto']
grotto_suffixes_italian = ['della Gioia', 'della Benedizione', 'dell’Esultanza', 'della Miseria', 'dell’Angoscia',
                           'della Pena', 'della Nostalgia', 'della Disgrazia', 'della Paura', 'della Fobia',
                           'della Sofferenza', 'della Malasorte', 'della Maledizione', 'della Malvagità', 'della Fine',
                           'della Morte']

grotto_special = "Has a special floor"
grotto_keys = ("Seed", "Rank", "Name",
               "Boss", "Type", "Floors",
               "Monster Rank", "Chests")

grotto_ranks = ["**S**", "**A**", "**B**", "**C**", "**D**", "**E**", "**F**", "**G**", "**H**", "**I**"]

quests_regex = r'^(?:(?:(⭐) )?\*\*Quest #(\d+) - (.+)\*\*(?: \1)?(?:```yml)?|(\w+): (.+?)(?:```)?)$'
cleanup_regex = r'([\w\d\.\-:/() ]+)'


def _hex(value):
    n = int(value)
    if n <= 16:
        return n
    n = int(value, base=16)

    hex_str = str.upper(hex(n)[2:])
    return hex_str.zfill(4)


def is_special(data: tuple):
    try:
        return data[0] == grotto_special
    except ValueError:
        return False


def create_grotto(datas):
    converters = (_hex, int, str)

    magic = 17
    ye = []

    for data in datas:
        match_found = re.compile(cleanup_regex).match(data)

        if match_found:
            stripped = str.strip(match_found.group(), "' ")

            if stripped != "":
                for i, converter in enumerate(converters):
                    try:
                        converted = converter(stripped)
                    except:
                        continue
                    else:
                        if isinstance(converted, str):
                            if converted.find(":") > -1:
                                continue
                            elif converted == grotto_special:
                                magic = 18
                                ye.insert(0, converted)
                            else:
                                ye.append(converted)
                        else:
                            ye.append(converted)
                        break
                    finally:
                        if len(ye) == magic:
                            yield tuple(ye)
                            magic = 17
                            ye = []

    if len(ye) > 0:
        yield tuple(ye)


def parse_regex(type, string):
    regex = ""
    if type == Quest:
        regex = quests_regex

    matches = re.findall(regex, string, flags=re.MULTILINE)

    if type == Quest:
        number = int(matches[0][1])
        name = matches[0][2]
        story = matches[0][0] == "⭐"

        location = ""
        request = ""
        solution = ""
        reward = ""
        prerequisite = ""
        repeat = False

        for info in matches[1:]:
            title = info[3].lower()
            data = info[4].strip()
            if title == "location":
                location = data
            if title == "request":
                request = data
            if title == "solution":
                solution = data
            if title == "reward":
                reward = data
            if title == "prerequisite":
                prerequisite = data
            if title == "repeat":
                repeat = data.lower() == "yes"

        quest = Quest(number, name, story, location, request, solution, reward, prerequisite, repeat)
        return quest.to_dict()
