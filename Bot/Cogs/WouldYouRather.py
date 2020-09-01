''' WOULDYOURATHER.py - A OR B ? YOU DECIDE
    This module represents a classic would you rather game.
'''
# -----------------------------------------------------------------------------------------------
# >> Imports
from bs4 import BeautifulSoup
from discord.ext import commands
import random
import requests
import Bot.Backend.utils as utils
import Bot.Backend.constants as constants

# -----------------------------------------------------------------------------------------------
class WouldYouRather(commands.Cog):

    def __init__(self, client):
        self.client = client

    def shortDescription(self):
        return 'Play \'Would you rather\''

    def longDescription(self):
        title='Would you rather'
        description = 'Asks you a specific \'A/B\'-question.\n\n**Invoke:** _`{}wyr`_'.format(constants.INVOKE)
        return [utils.embed_create(title=title, description=description, thumbnail=constants.WYR_ICON_URL), None]

    def isSecret(self):
        return False

    @commands.command(pass_context=True)
    async def wyr(self, ctx, *param):
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

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(WouldYouRather(client))