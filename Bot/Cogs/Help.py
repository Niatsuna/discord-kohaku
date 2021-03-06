''' HELP.py - INFORMATION TOOL'''
# -----------------------------------------------------------------------------------------------
# >> Imports
import Bot.Backend.checks as checks
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils

ALIASES = ['h']

# -----------------------------------------------------------------------------------------------
class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cmds = {}
        self.footer = {'text' : 'v{} | Parameters : <...> | Optional Parameters : (<...>) | List of parameters : [<...>]'.format(constants.VERSION)}

    def help_default(self):
        return [utils.embed_create(title='**Under Construction**', description='Either Nia forgot this embed, this embed is still under construction or something went terribly wrong ewe.'), None]

    def help(self, footer):
        title='Kohaku'
        description = 'Wasshoi~!\n Type `{}help <command>` to see more details about  a particular command.'.format(constants.INVOKE)
        fields = [ [None, False],
            [':clipboard: General', '`help`,`status`, `server`, `ping`, `gif`, `edit`', False],
            [':scroll: Game Information', '`animalcrossing`', True],
            [':game_die: Games', '`magic8ball`, `neverhaveiever`, `wouldyourather`, `rockpaperscissors`, `love`, `roll`', True],
            [None, False],
            [':gear: Source', '[Spaghetti code]({}), [Upcoming Features]({})'.format(constants.GITHUB_URL_CODE, constants.GITHUB_URL_BOARD), False]
        ]
        return utils.embed_create(title=title, description=description, fields=fields, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, name='help', aliases=ALIASES)
    async def _help(self, ctx, *, param):
        param = param.lower()
        if self.cmds == {}:
            self.cmds = utils.load_cmd_meta(self.client)
        if param in self.cmds.keys():
            try:
                result = self.cmds[param].help(self.footer)
            except:
                result = self.help_default()
            if not isinstance(result, list):
                result = [result,  None]
            await utils.embed_send(ctx, result[0],file=result[1])
        else:
            await self._help(ctx, param='help')

    @_help.error
    async def error_help(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self._help(ctx, param='help')

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(Help(client))