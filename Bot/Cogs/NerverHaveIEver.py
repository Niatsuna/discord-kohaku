''' NEVERHAVEIEVER.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import requests
from bs4 import BeautifulSoup

ALIASES = ['nhie']

# > ---------------------------------------------------------------------------
class Magic8Ball(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}neverhaveiever'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Selects a specific scenario.\n If you never did that, you pass ❌. But if you did do it at some point in your life: Drink! 🍹\n\n{}**Usage: ** `{}neverhaveiever`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def neverhaveiever(self, ctx, *, param):
        content = utils.json_load_url(constants.NHIE_URL)
        description = '... {}'.format(content['statement'][17:].strip())
        message = await utils.embed_send(ctx, utils.embed_create(title='Never have I ever ...', description=description))
        await message.add_reaction('🍹')
        await message.add_reaction('❌')

    @neverhaveiever.error
    async def neverhaveiever_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.neverhaveiever(ctx, param='NHIE')
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Magic8Ball(client))