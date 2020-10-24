''' ANIMALCROSSING.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil

ALIASES = ['ac', 'acnh']

# > ---------------------------------------------------------------------------
class AnimalCrossing(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.instant = {
            'art'   : self.instant_art(),
            'song'  : self.instant_songs(),
            'songs' : self.instant_songs(),
        }
        self.key = '1A1o0oesDUh5PCzu42UA47nYOfUaoFaRTNnEhnmsDdCw'
        self.sheets = ['AC - Art', 'AC - Bug', 'AC - Fish', 'AC - Fossils', 'AC - Sea creatures', 'AC - Songs', 'AC - Villagers']
        self.resource = None

        self.update()

    def help(self, footer):
        title = 'Help Info: {}animalcrossing'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        possibilities = ['`<art>` - Shows the difference between fake and real', '`<fish/bug/sea creature/fossil>` - Information about named critter', '`<month>` `(south)` - List critters of the month (leavin, arriving and currently catchable)', 
            '`all year` - List critters which are catchable all year long', '`<song>` - Short preview of the named song', '`songs` - List of all songs', '`<villager>` - Information about named villager']
        description = 'This command is connected to the game \'Animal Crossing : New Horizons\' and can show information regarding this game.\n\n{}**Usage: ** \n{}'.format(
            alias, '\n'.join(['`{}animalcrossing` {}'.format(constants.INVOKE, x) for x in possibilities]))
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def animalcrossing(self, ctx, *, param):
        param = param.lower().strip()
        
        await utils.embed_send(ctx, utils.embed_create(title='Ping : {}ms'.format(ceil(self.client.latency*1000))))

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


    async def instant_art(self):
        artworks = self.resource['AC - Art']
        title = 'Artworks ({})'.format(len(artworks))
        fields = []
        for i in range(0, len(artworks)):
            entry = artworks[i]
            if i % 2 == 0 and i > 0:
                fields.append([None, True])
            fields.append(['{} | {}'.format(entry['name'], entry['name_de']), constants.EMPTY_CHAR, True])
        return False

    async def instant_songs(self):
        return False



# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(AnimalCrossing(client))