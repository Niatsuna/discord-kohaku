''' RELOAD.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil

# > ---------------------------------------------------------------------------
class Reload(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}reload'.format(constants.INVOKE)
        description = 'Reloads a command / module\nSending with the keyword `all` will reload all commands / modules.\n Can only be used by moderators or higher!\n\n**Usage: ** `{}reload` `<cmd/module>`'.format(constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True)
    async def reload(self, ctx, *, param):
        # TODO
        await utils.embed_send(ctx, utils.embed_create(title='Ping : {}ms'.format(ceil(self.client.latency*1000))))

    @reload.error
    async def reload(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSIM_PARAM)
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Reload(client))