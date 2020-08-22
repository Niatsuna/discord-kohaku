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

# -----------------------------------------------------------------------------------------------
# >> Variables
client = commands.Bot(command_prefix=constants.INVOKE)
client.remove_command('help') # Removes default help command
discord_token = sys.argv[1]

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
client.run(discord_token)