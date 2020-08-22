''' HELP.py - INFORMATION TOOL
    Does what a help command should do. (duh.)
'''
# -----------------------------------------------------------------------------------------------
# >> Imports
import Bot.Backend.checks as checks
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils

# -----------------------------------------------------------------------------------------------
class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cmds = {}
        self.owner = utils.json_load('Bot/Resources/json/admin.json')['owner']

    def shortDescription_default(self):
        return '**Under Construction**'

    def longDescription_default(self):
        return [utils.embed_create(title='**Under Construction**', description='Either Nia forgot this embed, this embed is still under construction or something went terribly wrong ewe.'), None]

    def shortDescription(self):
        return 'Helps with commands and modules'

    def longDescription(self):
        title='Help'
        desc = 'I was written in {} by <@!{}>.\nLook at my [spaghetti code]({}) and [my upcoming features]({})!\n\n_For more infos regarding one module, use `{}help <module>`_\n\n_**Modules:**_'.format(
            utils.emote_load('python'), self.owner, constants.GITHUB_URL_CODE, constants.GITHUB_URL_BOARD, constants.INVOKE)
        modules = sorted(self.cmds.items(), key=(lambda  x: x[0]))
        fields = []
        for (cmd, cog) in modules:
            try:
                short = cog.shortDescription()
            except:
                short = self.shortDescription_default()
            fields.append(['`{}{}`'.format(constants.INVOKE, cmd), '_{}_'.format(short), False])
        return [utils.embed_create(title=title, description=desc, fields=fields), None]

    def isSecret(self):
        return False

    @commands.command(pass_context=True)
    async def help(self, ctx, *, param):
        param = param.lower()
        if self.cmds == {}:
            self.load_cmd_meta()
        if param in self.cmds.keys():
            try:
                result = self.cmds[param].longDescription()
            except:
                result = self.longDescription_default()
            if not isinstance(result, list):
                result = [result]
            await utils.embed_send(ctx, result[0],file=result[1])
        else:
            await self.help(ctx, param='help')

    @help.error
    async def error_help(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.help(ctx, param='help')

    def load_cmd_meta(self):
        for cog in self.client.cogs.values():
            if not checks.check_is_secret(cog) and cog.get_commands != []:
                self.cmds[cog.get_commands()[0].name] = cog

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(Help(client))