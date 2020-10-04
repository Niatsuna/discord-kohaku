''' RELOAD.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil

ALIASES = ['r', 'rl']

# > ---------------------------------------------------------------------------
class Reload(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cmds = {}

    def help(self, footer):
        title = 'Help Info: {}reload'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Reloads a command / module\nSending with the keyword `all` will reload all commands / modules.\n Can only be used by moderators or higher!\n\n{}**Usage: ** `{}reload` `<cmd/module>`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def reload(self, ctx, *, param):
        await utils.embed_send(ctx, utils.embed_create(title='ree : {}ms'.format(ceil(self.client.latency*1000))))

    @reload.error
    async def reload_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return

    def load_cmd_meta(self):
        for cog in self.client.cogs.values():
            if (not checks.check_is_secret(cog)) and cog.get_commands != []:
                self.cmds[cog.get_commands()[0].name] = cog


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Reload(client))