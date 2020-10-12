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
        self.key = '1sDTFrlxLNjLkLRHjIFK8HnKEbHtprsMHV8uHx7Csc1Y'
        self.sheets = ['GI - Characters', 'GI - Skills', 'GI - Constellations', 'GI - Regions']
        self.instant_map = {
            ''
        }

    def help(self, footer):
        title = 'Help Info: {}genshinimpact'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        params = [
            '`<character>` - Looks up a named character', '`character(s)` - Shows a list of all released characters',
            '`<skill>`  - Looks up a named skill', '`skill` `<character>` - Looks up all skills from a named character',
            '`<region>` - Looks up a region', '`<element>` - Looks up a element', '`elements` - Shows a graph with element reactions & effectiveness']
        description = 'This command is connected to the game \'Genshin Impact\' and can show information regarding this game.\n\n{}**Usage: **`{}genshinimpact` `parameter`\n**Parameters: **\n{}'.format(
            alias, constants.INVOKE, '\n'.join(params))
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def genshinimpact(self, ctx, *, param):
        param = param.lower().strip()

        await utils.embed_send(ctx, utils.embed_create(title='Ping : {}ms'.format(ceil(self.client.latency*1000))))

    @genshinimpact.error
    async def genshinimpact_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return

    async def update(self):
        result = {}
        for sheet in self.sheets:
            result[sheet] = utils.spreadsheet_to_json(self.key, sheet)
        utils.json_store('Bot/Resources/json/genshin_impact.json', result)



# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(GenshinImpact(client))