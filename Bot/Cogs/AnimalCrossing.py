''' ANIMALCROSSING.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil

ALIASES = ['ac', 'acnh']

# > ---------------------------------------------------------------------------
class AnimalCrossing(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}animalcrossing'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        possibilities = ['']
        description = 'This command is connected to the game \'Animal Crossing : New Horizons\' and can show information regarding this game.\n\n{}**Usage: ** \n{}'.format(
            alias, '\n'.join(['`{}animalcrossing` {}'.format(constants.INVOKE, x) for x in possibilities]))
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def animalcrossing(self, ctx, *, param):
        await utils.embed_send(ctx, utils.embed_create(title='Ping : {}ms'.format(ceil(self.client.latency*1000))))

    @animalcrossing.error
    async def animalcrossing_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(AnimalCrossing(client))