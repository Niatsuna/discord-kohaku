''' UTILS.py '''
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
def map_function(data):
    ''' Maps data with the syntax\n 
    [function, param1, param2, ...]\n
    as\n
    function(param1, param2, ...)'''
    return data[0](*data[1:])

async def map_function_async(data):
    ''' Maps data with the syntax\n
    [function, param1, param2, ...]\n
    as\n
    await function(param1, param2, ...)'''
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
        count = math.ceil(len(fields)/25)
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
        return await ctx.message.channel.send(embed=embed, file=file)
    else:
        if isinstance(file, list) and len(file) < len(embed):
            file = file + [None] * (len(embed) - len(file))
        elif not isinstance(file, list):
            file = [file] * len(embed)
        for i in range(0, len(embed)):
            await ctx.message.channel.send(embed=embed[i], file=file[i])
        return -1

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

# > Levels
def total_exp(lvl):
    ''' Calculates how many experience points must be gathered to reach a level.\n
    Calculated as follows: 10 * (lvl ^ 2) + total_exp(lvl-1)'''
    if lvl < 1:
        return None
    elif lvl <= len(constants.LVLS):
        return constants.LVLS[lvl-1]
    else: # lvl > len(constants.LVLS)
        for i in range(len(constants.LVLS), lvl+1):
            constants.LVLS.append(10 * ((i+1)**2) + constants.LVLS[i-1])
        return constants.LVLS[lvl-1]

def level(experience):
    ''' Determines which level is reached with the given experience points. '''
    if experience > constants.LVLS[-1]:
        i = len(constants.LVLS) + 1
        total_exp(i)
        return level(experience)
    elif experience == constants.LVLS[-1]:
        return len(constants.LVLS)
    else: #xp < LEVEL[-1]
        for i in range(0,len(constants.LVLS)):
            if experience == constants.LVLS[i]:
                return i+1
            elif experience < constants.LVLS[i]:
                return i

# > Logger
logging.basicConfig(format='%(levelname)s-%(message)s', level=logging.INFO)
logger = logging.getLogger()

def critical(message):
    ''' Logs a critical situation into the console. '''
    logger.critical(message)

def log(message):
    ''' Logs an information into the console. '''
    logger.info(message)

def warn(message):
    ''' Logs a warning into the console. '''
    logger.warning(message)

# > Spreadsheet

def spreadsheet_to_json(key, sheets):
    ''' Converts a public google spreadsheet to json. Each sheet will be converted to an array of rows and every row to a dict (keys are first row). '''
    result = {}
    for sheet in sheets:
        # > Get Sheet
        URL = 'https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}'.format(key, sheet)
        try:
            response = str(requests.get(URL).content).split('\\n')
        except:
            response = None
        # > Convert Sheet to json
        content = []
        if response != None:
            # > Clear up rows (Delete extra characters on the beginning and end)
            c_rows = []
            for i in range(0, len(response)):
                line = response[i].split(',')
                if i == 0:
                    line[0] = line[0][2:]
                elif i == len(response) - 1:
                    line[-1] = line[-1][:-2]
                for j in range(0, len(line)):
                    line[j] = line[j][1:-1].replace('\\\'', '\'')
                    if line[j] == 'TRUE' or line[j] == 'FALSE':
                        line[j] = (line[j] == 'TRUE')
                c_rows.append(line)
            # > Use keys to convert each row into a dict
            keys = c_rows[0] # First row = Keys
            for i in range(0, len(c_rows[1:])):
                row = {}
                for j in range(0, len(keys)):
                    row[keys[j]] = c_rows[i][j]
                content.append(row)
        # > Store converted content in json
        result[sheet] = content
    return result