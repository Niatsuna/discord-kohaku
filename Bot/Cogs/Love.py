''' LOVE.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from random import randint

ALIASES = ['<3']

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
        param = param.replace('<', '').replace('@', '').replace('!', '').replace('>', '')
        if param != 'everyone':
            try:
                user = self.client.get_user(int(param.replace('<', '').replace('@', '').replace('!', '').replace('>', '')))
            except:
                user = None
            if user == None:
                await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)
                return
            perc = randint(0,101)
            if perc == 101:
                description = ':heart: • The love between {} and {} is very strong! Their love is infinite!'.format(ctx.message.author.mention, user.mention)
            else:
                description = ':heart: • There is a {}% chance of love between {} and {}'.format(perc, ctx.message.author.mention, user.mention)
        else:
            description = ':heart: • {} loves everybody equally for at least {}%'.format(ctx.message.author.mention, randint(0,100))
        await utils.embed_send(ctx, utils.embed_create(description=description))

    @love.error
    async def love_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.love(ctx, param=str(ctx.message.author.id))
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Love(client))