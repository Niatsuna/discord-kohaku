''' WOULDYOURATHER.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import random
import requests
from bs4 import BeautifulSoup

ALIASES = ['wyr']

# > ---------------------------------------------------------------------------
class WouldYouRather(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}wouldyourather'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Asks you a specific \'A/B\'-question.\n\n{}**Usage: ** `{}wouldyourather`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def wouldyourather(self, ctx, *, param):
        url = constants.WYR_URL.format(random.randint(3,99999))
        try:
            response = requests.get(url)
            page = BeautifulSoup(response.content, 'lxml')
        except Exception as ex:
            exc = '{}: {}'.format(type(ex).__name__, ex)
            utils.warn('> [Cmd:Wyr] Error during page scraping: {} |'.format(exc))
            await ctx.message.channel.send(embed=constants.ERROR_WHOOPS)
            return
        title = page.find('h3', class_='preface').text.strip()
        options = page.find_all('span', class_='option-text')[:2]
        A = options[0].text.strip()
        B = options[1].text.strip()
        description = '🅰️ {}\n🅱️ {}'.format(A,B)
        message = await ctx.message.channel.send(embed=utils.embed_create(title=title, description=description))
        await message.add_reaction('🅰️')
        await message.add_reaction('🅱️')

    @wouldyourather.error
    async def wouldyourather_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.wouldyourather(ctx, param='WYR')
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(WouldYouRather(client))