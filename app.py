''' APP.PY - BOT'S CORE
    This is the core of Kohaku where all modules are loaded and initialized.
    On start Kohaku is given the discord token to login. Other things are loaded from code.
'''
# -----------------------------------------------------------------------------------------------
# >> Imports
from discord.ext import commands
import Bot.Backend.constants as constants
import sys
import Bot.Backend.utils as utils
import json
import gspread
from Bot.Backend.Firebase import Firebase

# -----------------------------------------------------------------------------------------------
# >> Variables
client = commands.Bot(command_prefix=constants.INVOKE)
client.remove_command('help') # Removes default help command
try:
    _credentials = json.loads(sys.argv[2])
    utils.json_store('fire_cred.json', _credentials)
except:
    _credentials = utils.json_load('fire_cred.json')
constants.FIRE_CON = Firebase(_credentials)
constants.GC_CON = gspread.service_account(filename='fire_cred.json')

@client.event
async def on_message(message):
    # Does nothing (Override deafult on_message)
    return

# -----------------------------------------------------------------------------------------------
# >> Extensions
extension_path = 'Bot.Cogs.'
for cog in constants.COGS:
    try:
        client.load_extension(extension_path + cog)
        utils.log('[Kohaku] Loaded extension \'{}\''.format(cog))
    except Exception as ex:
        exc = '{}: {}'.format(type(ex).__name__, ex)
        utils.warn('[Kohaku] Failed to load extension {}\n{}'.format(cog, exc))

# -----------------------------------------------------------------------------------------------
client.run(sys.argv[1])