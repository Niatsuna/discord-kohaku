''' PING.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil

# > ---------------------------------------------------------------------------
class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}ping'.format(constants.INVOKE)
        description = 'Pings Kohaku and returns the ping in ms.\n\n**Usage: ** `{}ping`'.format(constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True)
    async def ping(self, ctx, *, param):
        await utils.embed_send(ctx, utils.embed_create(title='Ping : {}ms'.format(ceil(self.client.latency*1000))))

    @ping.error
    async def ping_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.ping(ctx, param=str(ctx.message.author.id))
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Ping(client))