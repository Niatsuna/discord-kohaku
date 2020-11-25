''' LOVE.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from random import randint

ALIASES = ['<3', ':heart:']

# > ---------------------------------------------------------------------------
class Love(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}love'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Shows how much love is currently possible between you and a mentioned user.\n\n{}**Usage: ** `{}love` `<id/mention>`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def love(self, ctx, *, param):
        try:
            user = self.client.get_user(int(param.replace('<', '').replace('@', '').replace('!', '').replace('>', '')))
        except:
            user = None
        if user == None:
            await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)
            return
        description = ':heart: • There is a {}% chance of love between {} and {}'.format(randint(0,100), ctx.message.author.mention, user.mention)
        await utils.embed_send(ctx, utils.embed_create(description=description))

    @love.error
    async def love_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.ping(ctx, param=str(ctx.message.author.id))
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Love(client))