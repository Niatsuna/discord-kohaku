''' APP.PY - BOT'S CORE
    This is the core of Kohaku where all modules are loaded and initialized.
    On start Kohaku is given the discord token to login. Other things are loaded from code.
'''
# -----------------------------------------------------------------------------------------------
# >> Imports
from discord import Intents
from discord.ext import commands
import Bot.Backend.constants as constants
import sys
import Bot.Backend.utils as utils
import json
from Bot.Backend.Firebase import Firebase

# -----------------------------------------------------------------------------------------------
# >> Variables
intents = Intents.all()
client = commands.Bot(command_prefix=constants.INVOKE, intents=intents)
client.remove_command('help') # Removes default help command
try:
    FIRE_PRIVATE_KEY_ID = sys.argv[2]
    FIRE_PRIVATE_KEY = sys.argv[3]
    FIRE_CLIENT_EMAIL = sys.argv[4]
    FIRE_CLIENT_ID = sys.argv[5]
    FIRE_CLIENT_CERT_URL = sys.argv[6]

    _credentials = {
    "type": "service_account",
    "project_id": "discord-kohaku",
    "private_key_id": FIRE_PRIVATE_KEY_ID,
    "private_key": FIRE_PRIVATE_KEY,
    "client_email": FIRE_CLIENT_EMAIL,
    "client_id": FIRE_CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": FIRE_CLIENT_CERT_URL
    }
    utils.json_store('fire_cred.json', _credentials)
except:
    _credentials = utils.json_load('fire_cred.json')
constants.FIRE_CON = Firebase(_credentials)

@client.event
async def on_message(message):
    # Override default on_message (get's filled in EventHandler)
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