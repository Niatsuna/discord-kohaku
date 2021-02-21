''' GENSHINIMPACT.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil

ALIASES = ['gi', 'genshin']

# > ---------------------------------------------------------------------------
class GenshinImpact(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        raise Exception('Not done yet owo!')

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def genshinimpact(self, ctx, *, param):
        await utils.embed_send(ctx, constants.ERROR_LOCKED)

    @genshinimpact.error
    async def genshinimpact_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return

    async def update(self):
        return



# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(GenshinImpact(client))