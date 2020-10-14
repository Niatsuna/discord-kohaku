''' MAGIC8BALL.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import hashlib
import random

ALIASES = ['8b']

# > ---------------------------------------------------------------------------
class Magic8Ball(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.answers = utils.json_load('Bot/Resources/json/magic8ball.json')

    def help(self, footer):
        title = 'Help Info: {}magic8ball'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Answers your \'yes/no\'-questions.\n\n{}**Usage: ** `{}magic8ball`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def magic8ball(self, ctx, *, param):
        for m in ctx.message.mentions:
            for r in ['<!@{}>'.format(m.id), '<@{}>'.format(m.id)]:
                param = param.replace(r, m.display_name)
        h_param = int(hashlib.sha1(param.lower().replace(' ', '').encode('utf-8')).hexdigest(), 16)
        a_range = self.answers[h_param % 2]
        description = '🎱 {}'.format(a_range[random.randint(0, len(a_range)-1)])
        await utils.embed_send(ctx, utils.embed_create(title='"{}"'.format(param), description=description))

    @magic8ball.error
    async def magic8ball_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Magic8Ball(client))