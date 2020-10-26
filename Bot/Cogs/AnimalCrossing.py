''' ANIMALCROSSING.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from concurrent.futures import ThreadPoolExecutor

ALIASES = ['ac', 'acnh']

# > ---------------------------------------------------------------------------
class AnimalCrossing(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.instant = {
            'art'       : lambda self, ctx : self.instant_art(ctx),
            'fossils'   : lambda self, ctx : self.instant_fossils(ctx),
            'songs'     : lambda self, ctx : self.instant_songs(ctx),
        }
        self.functions = [self.search_fossil]
        self.key = '1A1o0oesDUh5PCzu42UA47nYOfUaoFaRTNnEhnmsDdCw'
        self.sheets = ['AC - Art', 'AC - Bug', 'AC - Fish', 'AC - Fossils', 'AC - Sea creatures', 'AC - Songs', 'AC - Villagers']
        self.resource = utils.json_load('Bot/Resources/json/animal_crossing.json')

    def help(self, footer):
        title = 'Help Info: {}animalcrossing'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        possibilities = ['']
        description = 'This command is connected to the game \'Animal Crossing : New Horizons\' and can show information regarding this game.\n\n{}**Usage: ** \n{}'.format(
            alias, '\n'.join(['`{}animalcrossing` {}'.format(constants.INVOKE, x) for x in possibilities]))
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def animalcrossing(self, ctx, *, param):
        param = param.lower().strip()
        if self.resource == None:
            await self.update()
        if param in self.instant.keys():
            if not await self.instant[param](self, ctx):
                await utils.embed_send(ctx, constants.ERROR_WHOOPS)
        else:
            with ThreadPoolExecutor(max_workers=len(self.functions)) as executor:
                _bool = [await executor.submit(utils.map_function_async, [func, ctx, param]).result() for func in self.functions]
            if True not in _bool:
                await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)

    @animalcrossing.error
    async def animalcrossing_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return

    async def update(self):
        result = {}
        for sheet in self.sheets:
            result[sheet] = utils.spreadsheet_to_json(self.key, sheet)
        utils.json_store('Bot/Resources/json/animal_crossing.json', result)
        self.resource = result

    async def _instant_list(self, ctx, array, title):
        desc = 'There are currently {} {}.'.format(len(array), title.lower())
        fields = []
        for entry in array:
            fields.append([entry['name'], '**German:** {}'.format(entry['name_de']), True])
        await utils.embed_send(ctx, utils.embed_create(title=title, description=desc, fields=fields))

    async def instant_art(self, ctx):
        artworks = self.resource['AC - Art']
        try:
            await self._instant_list(ctx, artworks, 'Artworks')
            return True
        except:
            return False

    async def instant_songs(self, ctx):
        songs = self.resource['AC - Songs']
        try:
            await self._instant_list(ctx, songs, 'Songs')
            return True
        except:
            return False

    async def instant_fossils(self, ctx):
        fossils = self.resource['AC - Fossils']
        try:
            await self._instant_list(ctx, fossils, 'Fossils')
            return True
        except:
            return False

    async def search_fossil(self, ctx, name):
        return False



# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(AnimalCrossing(client))