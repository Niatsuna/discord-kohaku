''' NEVERHAVEIEVER.py - NEVER HAVE OR DRINK!
    This module represents a classic never have i ever game.
'''
# -----------------------------------------------------------------------------------------------
# >> Imports
from bs4 import BeautifulSoup
from discord.ext import commands
import requests
import Bot.Backend.utils as utils
import Bot.Backend.constants as constants

# -----------------------------------------------------------------------------------------------
class NeverHaveIEver(commands.Cog):

    def __init__(self, client):
        self.client = client

    def shortDescription(self):
        return 'Play \'Never have I ever ... \''

    def longDescription(self):
        title = 'Never have I ever'
        description = 'Selects a specific scenario.\n If you never did that, you pass ❌. But if you did do it at some point in your life: Drink! 🍹\n\n **Invoke:** _`{}nhie`_'.format(constants.INVOKE)
        return [utils.embed_create(title=title, description=description, thumbnail=constants.NHIE_ICON_URL), None]

    def isSecret(self):
        return False

    @commands.command(pass_context=True)
    async def nhie(self, ctx, *param):
        try:
            response = requests.get(constants.NHIE_URL)
            page = BeautifulSoup(response.content, 'lxml')
        except Exception as ex:
            exc = '{}: {}'.format(type(ex).__name__, ex)
            utils.warn('> [Cmd:Nhie] Error during page scraping: {} |'.format(exc))
            await ctx.message.channel.send(embed=constants.ERROR_WHOOPS)
            return
        description = page.find('h1').parent['url'][1:].replace('-',' ')
        message = await ctx.message.channel.send(embed=utils.embed_create(title='Never have I ever ...', description=description))
        await message.add_reaction('🍹')
        await message.add_reaction('❌')

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(NeverHaveIEver(client))