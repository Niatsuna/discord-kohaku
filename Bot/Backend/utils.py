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
async def map_function(data):
    return await data[0](*data[1:])


# > Embed
def embed_create(title=Embed.Empty, description=Embed.Empty, fields=[], image=None, thumbnail=None, footer={'text': Embed.Empty, 'icon_url': Embed.Empty}):
    '''Creates an Embed or a list of Embeds if the given parameters exceed the limits.'''
    count = math.ceil(len(fields)/constants.EMBED_MAX_FIELD)
    description = [description] + [Embed.Empty] * (count-1)
    embeds = []
    for i in range(0, count):
        embed = Embed(  title=title if count == 1 or title == Embed.Empty else title + ' - [{}/{}]'.format(i+1,count),
                        description=description[i], color=constants.COLOR)
        if thumbnail != None:
            embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=footer['text'], icon_url=footer['icon_url'])
        embeds.append(embeds)
    if image != None:
        embeds[-1].set_image(url=image)
    if len(embeds) == 1:
        return embeds[0]
    return embeds

async def embed_send(ctx, embed, file=None):
    '''Sends the Embed or a list of Embeds to the given channel in the context.'''
    if isinstance(embed, Embed.__class__):
        await ctx.message.channel.send(embed=embed, file=file)
    else:
        for e in embed[:-1]:
            await ctx.message.channel.send(embed=e)
        await ctx.message.channel.send(embed=embed[-1], file=file)

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
    with open(local_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def json_load_url(url):
    '''Loads the content of a remote stored json file (API).'''
    try:
        response = requests.get(url).json()
    except:
        response = None
    return response

def json_store(local_path, json_content):
    '''Stores the given content at the given path.'''
    with open(local_path, 'w') as f:
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
