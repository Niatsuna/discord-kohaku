''' CONSTANTS '''
# > ---------------------------------------------------------------------------------
# > Imports
from discord import Embed
from os import listdir
from os.path import isfile, join
# > ---------------------------------------------------------------------------------
# > General
COGS = [f[:-3] for f in listdir('Bot/Cogs/') if isfile(join('Bot/Cogs/', f))]
COLOR = 0x1b6c8f
EMPTY_CHAR = '\u200b'
INVOKE = '-'
RANK_MAP = {
    0 : 'Member', 1335 : 'Moderator', 1336 : 'Admin', 1337 : 'Owner'
}
TIMEOUT = {}

# > Error
ERROR_MISSIM_PARAM      = Embed(description='Please give me something to work with or try `{}help` for futher information.'.format(INVOKE), color=COLOR)
ERROR_PERMISSION_DENIED = Embed(description='You are not allowed to do that.', color=COLOR)
ERROR_SEARCH_FAIL       = Embed(description='Couldn\'t find what you are looking for! Please check your spelling or try `{}help` for further information.'.format(INVOKE), color=COLOR)
ERROR_WHOOPS            = Embed(description='Whooops! Something went totally wrong! Please contact an admin!', color=COLOR)

# > Firebase
FIRE_URL = 'https://discord-kohaku.firebaseio.com/'
FIRE_CON = None

# > GitHub
GITHUB_URL_CODE = 'https://github.com/Niatsuna/discord-kohaku'
GITHUB_URL_BOARD = 'https://github.com/Niatsuna/discord-kohaku/projects/1'

# > Levels
LVLS = [0]
MAX_EXP = 2000000000