''' CONSTANTS '''
# > ---------------------------------------------------------------------------------
# > Imports
from discord import Embed
from os import listdir
from os.path import isfile, join
# > ---------------------------------------------------------------------------------
# > General
USER_DATA = {}
COGS = [f[:-3] for f in listdir('Bot/Cogs/') if isfile(join('Bot/Cogs/', f))]
COLOR = 0x1b6c8f
EMPTY_CHAR = '\u200b'
EMPTY_USER = {'rank' : 0, 'prestige' : 0, 'xp' : 0, 'description' : '-'}
INVOKE = '-'
MISSING_PICTURE = 'https://cdn.discordapp.com/attachments/637574177657847809/762666189524172800/question_mark.png'
RANK_MAP = {
    0 : 'Member', 1335 : 'Moderator', 1336 : 'Admin', 1337 : 'Owner'
}
TIMEOUT = {}
VERSION = '2.0'

# > API
API_URL = 'https://niatsuna.github.io/api-kohaku/data'

# > Error
ERROR_LOCKED            = Embed(description='This function is currently locked (not behind a paywall), because of development.', color=COLOR)
ERROR_MISSING_PARAM     = Embed(description='Please give me something to work with or try `{}help` for futher information.'.format(INVOKE), color=COLOR)
ERROR_PERMISSION_DENIED = Embed(description='You are not allowed to do that.', color=COLOR)
ERROR_SEARCH_FAIL       = Embed(description='Couldn\'t find what you are looking for! Please check your spelling or try `{}help` for further information.'.format(INVOKE), color=COLOR)
ERROR_TIMEOUT           = Embed(description='Timeout! Please try again ... and this time: Please shut the door behind you.', color=COLOR)
ERROR_WHOOPS            = Embed(description='Whooops! Something went totally wrong! Please contact an admin!', color=COLOR)

# > Google
FIRE_URL = 'https://discord-kohaku.firebaseio.com/'
FIRE_CON = None

# > GIF
GIF_URL = 'https://api.tenor.com/v1/search?q={}&limit=50'

# > GitHub
GITHUB_URL_CODE = 'https://github.com/Niatsuna/discord-kohaku'
GITHUB_URL_BOARD = 'https://github.com/Niatsuna/discord-kohaku/projects/1'

# > Levels
LVLS = [0]
MAX_EXP = 2000000000

# > Never Have I Ever
NHIE_URL = 'https://api.nhie.io/v1/statements/random'

# > Would you rather
WYR_URL = 'http://either.io/{}'