''' UTILS.py - Stores Bot Functions like Image concat, etc. '''
# > ---------------------------------------------------------------------------
# > Imports
from io import BytesIO
import Bot.Backend.constants as constants
from discord import Embed, File
from PIL import Image
import json
import logging
import math
import requests

# > ---------------------------------------------------------------------------
# > General
def emote_load(key):
    '''Loads an emote from the internal list or sends a '<key>' back if the emote was not found.'''
    if key in constants.EMOTES.keys():
        return constants.EMOTES[key]
    return '<{}>'.format(key)

def map_function(data):
    return data[0](*data[1:])

async def map_function_async(data):
    return await data[0](*data[1:])

# > Embed
def embed_create(title=Embed.Empty, description=Embed.Empty, fields=[], image=None, thumbnail=None, footer={'text': Embed.Empty, 'icon_url': Embed.Empty}):
    '''Creates an Embed or a list of Embeds if the given parameters exceed the limits.'''
    if 'icon_url' not in footer.keys():
        footer['icon_url'] = Embed.Empty
    if 'text' not in footer.keys():
        footer['text'] = Embed.Empty
    if fields == []:
        count = 1
    else:
        count = math.ceil(len(fields)/constants.EMBED_MAX_FIELD)
    description = [description] + [Embed.Empty] * (count-1)
    embeds = []
    for i in range(0, count):
        embed = Embed(  title=title if count == 1 or title == Embed.Empty else title + ' - [{}/{}]'.format(i+1,count),
                        description=description[i], color=constants.COLOR)
        fields_ = fields[i*25:(min(i*25 + len(fields[i*25:]),(i+1)*25))]
        for f in fields_:
            if f[0] == None:
                embed.add_field(name=constants.EMPTY_CHAR, value=constants.EMPTY_CHAR, inline=f[1])
            else:
                embed.add_field(name=f[0], value=f[1], inline=f[2])
        if thumbnail != None:
            embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=footer['text'], icon_url=footer['icon_url'])
        embeds.append(embed)
    if image != None:
        embeds[-1].set_image(url=image)
    if len(embeds) == 1:
        return embeds[0]
    return embeds

async def embed_send(ctx, embed, file=None):
    '''Sends the Embed or a list of Embeds to the given channel in the context.'''
    if isinstance(embed, Embed):
        await ctx.message.channel.send(embed=embed, file=file)
    else:
        if isinstance(file, list) and len(file) < len(embed):
            file = file + [None] * (len(embed) - len(file))
        elif not isinstance(file, list):
            file = [file] * len(embed)
        for i in range(0, len(embed)):
            await ctx.message.channel.send(embed=embed[i], file=file[i])

# > Image
filters = {1 : Image.NEAREST, 2 : Image.BOX, 3 : Image.BILINEAR, 4 : Image.HAMMING, 5 : Image.BICUBIC, 6 : Image.LANCZOS}

def image_concat_lr(left : Image, right : Image):
    '''Concats two images horizontaly.'''
    img = Image.new('RGBA', (left.width + right.width, left.height), 0)
    img.paste(left, (0, 0))
    img.paste(right, (left.width, 0))
    return img

def image_concat_ud(up : Image, down : Image):
    '''Concats two images verticaly.'''
    img = Image.new('RGBA', (up.width, up.height + down.height), 0)
    img.paste(up, (0, 0),0)
    img.paste(down, (0, up.height), 0)
    return img

def image_resize(image, width, height, mode=1):
    '''Resizes given Picture. Mode: 1=NEAREST, 2=BOX, 3=BILINEAR, 4=HAMMING, 5=BICUBIC, 6=LANCZOS'''
    return image.resize((width, height), filters[mode])

def image_resize_factor(image, factor, mode=1):
    '''Resizes given Picture by a factor. Mode: 1=NEAREST, 2=BOX, 3=BILINEAR, 4=HAMMING, 5=BICUBIC, 6=LANCZOS'''
    x = math.ceil(image.width * factor)
    y = math.ceil(image.width * factor)
    return image_resize(image, x, y, mode)

def image_open(local_path):
    '''Opens a local stored Image.'''
    try:
        return Image.open(local_path)
    except:
        return None

def image_open_url(url):
    '''Opens a remote stored Image.'''
    try:
        response = requests.get(url)
        return Image.open(BytesIO(response.content))
    except:
        return None

def image_to_arr(image):
    '''Converts a given Image to a bytes array.'''
    arr = BytesIO()
    image.save(arr, format='PNG', **image.info)
    arr.seek(0)
    return arr

def image_to_file(image):
    '''Converts agiven Image to a Discord.File.'''
    return File(image_to_arr(image), filename='image.png')

# > JSON
def json_load(local_path):
    '''Loads the content of a local stored json file at the given path.'''
    try:
        with open(local_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def json_load_url(url):
    '''Loads the content of a remote stored json file (API).'''
    try:
        response = requests.get(url).json()
    except:
        response = None
    return response

def json_store(local_path, json_content):
    '''Stores the given content at the given path.'''
    with open(local_path, 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_content, ensure_ascii=False, indent=4))

# > Logger
logging.basicConfig(format='%(levelname)s-%(message)s', level=logging.INFO)
logger = logging.getLogger()

def critical(message):
    logger.critical(message)

def log(message):
    logger.info(message)

def warn(message):
    logger.warning(message)
