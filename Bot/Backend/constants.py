''' CONSTANTS.py - Stores Bot Constants like Color, Invoke etc. '''
# > ---------------------------------------------------------------------------
# > Imports
from discord import Embed
from Bot.Backend.utils import json_load
from os import listdir
from os.path import isfile, join

# > ---------------------------------------------------------------------------
# > General
COGS = [f[:-3] for f in listdir('Bot/Cogs/') if isfile(join('Bot/Cogs/', f))]
COLOR = 0x1b6c8f
EMPTY_CHAR = '\u200b'
INVOKE = '-'
OWNER = json_load('Bot/Resources/json/admin.json')['owner']
EMOTES = json_load('Bot/Resources/json/emotes.json')
GIFS = json_load('Bot/Resources/json/gifs.json')

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
AC_ICON_URL = 'https://cdn.discordapp.com/attachments/270376999925579778/744274811559215165/Du_bist_so_ein_Jfif_nea_das_musste_mal_gesagt_werden.png' # Love ya, hon

# > Cog : Dead by Daylight
DBD_REST_API = 'https://dbd-stats.info/api/'
DBD_WIKI_URL = 'https://deadbydaylight.gamepedia.com/'
DBD_ICON_URL = 'https://cdn.discordapp.com/attachments/737974066362712094/739284880768237658/file.png'

# > Cog : Fate/Grand Order
FGO_REST_API = 'https://api.atlasacademy.io/nice/NA/'
FGO_WIKI_URL = 'https://grandorder.wiki/'
FGO_ICON_URL = 'https://cdn.discordapp.com/attachments/626462024913911818/750153394949193848/NeroIcon.png'

# > Cog : Never Have I Ever
NHIE_URL = 'http://www.neverhaveiever.org'
NHIE_ICON_URL = 'https://discordapp.com/assets/4e4a4ac66710b0aecf931cd72cd65d9e.svg'

# > Cog : Pokémon
PKM_REST_API = 'https://pokeapi.co/api/v2/'
PKM_WIKI_URL_DE = 'https://www.pokewiki.de/'
PKM_WIKI_URL_EN = 'https://www.pokemon.com/us/pokedex/'
PKM_ICON_URL = 'https://cdn.discordapp.com/emojis/741978619361886261.png?v=1'

# > Cog : Would you rather
WYR_URL = 'http://either.io/{}'
WYR_ICON_URL = 'https://discordapp.com/assets/2cc6266229c7e2ccfde10e81782e8b5c.svg'
