''' LEAVE.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil
import random

ALIASES = ['l']

# > ---------------------------------------------------------------------------
class Leave(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}leave'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = '**Owner only:** Leaves specific Server.\n\n{}**Usage: ** `{}leave (<id>)`\n**Warning: ** No id results in leaving the server which the message origin from.'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.check(checks.check_is_owner and checks.check_is_guild)
    @commands.command(pass_context=True, aliases=ALIASES)
    async def leave(self, ctx, *, param):
        param = int(param.replace('<', '').replace('@', '').replace('!', '').replace('>', ''))
        g = self.client.get_guild(param)
        if g == None:
            await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)
        else:
            message = await utils.embed_send(ctx, utils.embed_create(description='Kohaku will be leaving \'{}\'. Are you sure?'.format(g.name)))
            await message.add_reaction('✔')
            await message.add_reaction('❌')

            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=lambda reaction, user : user == ctx.message.author and str(reaction.emoji) in ['✔', '❌'])
            except Exception:
                await message.edit(embed=constants.ERROR_TIMEOUT)
                return

            if str(reaction.emoji) == '✔':
                await message.edit(embed=utils.embed_create(description='Successfully left the guild \'{}\''.format(g.name)))
                await g.leave()
            elif str(reaction.emoji) == '❌':
                await message.edit(embed=utils.embed_create(description='No moving ? God damnit! I already packed my things q-q'))
            else:
                await message.edit(embed=constants.ERROR_WHOOPS)

    @leave.error
    async def leave_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.leave(ctx, param=str(ctx.message.guild.id))
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Leave(client))