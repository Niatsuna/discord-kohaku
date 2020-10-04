''' GIF.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import random

ALIASES = []

# > ---------------------------------------------------------------------------
class GIF(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}gif'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Search gifs (on tenor) with the given parameter and returns a random gif from this list.\n\n{}**Usage: ** `{}gif <parameter>`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def gif(self, ctx, *, param):
        gifs = utils.json_load_url(constants.GIF_URL.format(param))
        if gifs == None:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return
        if len(gifs['results']) == 0:
            await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)
            return
        i = random.randint(0,len(gifs['results'])-1)
        gif = gifs['results'][i]['media'][0]['gif']
        await utils.embed_send(ctx, utils.embed_create(image=gif['url']))

    @gif.error
    async def gif_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(GIF(client))