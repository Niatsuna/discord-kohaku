''' CONSTANTS.py - Stores Bot Constants like Color, Invoke etc. '''
# > ---------------------------------------------------------------------------
# > Imports
from discord import Embed
from os import listdir
from os.path import isfile, join

# > ---------------------------------------------------------------------------
# > General
COGS = [f[:-3] for f in listdir('Bot/Cogs/') if isfile(join('Bot/Cogs/', f))]
COLOR = 0x1b6c8f
INVOKE = '-'

# > Embed
EMBED_MAX_TITLE = 256
EMBED_MAX_DESCRIPTION = 2048
EMBED_MAX_FIELD = 25
EMBED_MAX_LINE_LEN = 55

# > Error
ERROR_MISSIM_PARAM      = Embed(description='Please give me something to work with or try `{}help` for futher information.'.format(INVOKE), color=COLOR)
ERROR_PERMISSION_DENIED = Embed(description='You are not allowed to do that.', color=COLOR)
ERROR_SEARCH_FAIL       = Embed(description='Couldn\'t find what you are looking for! Please check your spelling or try `{}help` for further information.'.format(INVOKE), color=COLOR)
ERROR_WHOOPS            = Embed(description='Whooops! Something went totally wrong! Please contact an admin!', color=COLOR)

# > GitHub
GITHUB_URL_CODE = 'https://github.com/Niatsuna/discord-kohaku'
GITHUB_URL_BOARD = 'https://github.com/Niatsuna/discord-kohaku/projects/1'

# > Cog : Animal Crossing New Horizons
AC_REST_API = 'https://acnhapi.com/v1/'
AC_WIKI_URL = 'https://nookipedia.com/wiki/'

# > Cog : Dead by Daylight
DBD_REST_API = 'https://dbd-stats.info/api/'
DBD_WIKI_URL = 'https://deadbydaylight.gamepedia.com/'

# > Cog : Fate/Grand Order
FGO_REST_API = 'https://api.atlasacademy.io/nice/NA/'
FGO_WIKI_URL = 'https://grandorder.wiki/'

# > Cog : Pokémon
PKM_REST_API = 'https://pokeapi.co/api/v2/'
PKM_WIKI_URL_DE = 'https://www.pokewiki.de/'
PKM_WIKI_URL_EN = 'https://www.pokemon.com/us/pokedex/'
