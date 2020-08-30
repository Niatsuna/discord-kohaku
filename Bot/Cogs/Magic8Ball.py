''' MAGIC8BALL.py - ANSWERS YOUR QUESTIONS
    This module represents a classic magic 8ball which can answer yes-no questions.
    These answers are stored in the Resources/magic8ball.json.
'''
# -----------------------------------------------------------------------------------------------
# >> Imports
from discord.ext import commands
import hashlib
import random
import Bot.Backend.utils as utils
import Bot.Backend.constants as constants

# -----------------------------------------------------------------------------------------------
class Magic8Ball(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.answers = utils.json_load('Bot/Resources/json/magic8ball.json')

    def shortDescription(self):
        return 'Magic 8Ball Module'

    def longDescription(self):
        title='Magic 8Ball'
        desc = 'Answers your \'yes/no\'-questions.\n\n**Invoke:** `{}8b <question>`'.format(constants.INVOKE)
        return [utils.embed_create(title=title, description=desc), None]

    def isSecret(self):
        return False

    @commands.command(pass_context=True, name='8b')
    async def magic8ball(self, ctx, *, param):
        for m in ctx.message.mentions:
            param = param.replace("<@!{}>".format(m.id), m.display_name).replace("<@{}>".format(m.id), m.display_name)
        h_param = int(hashlib.sha1(param.lower().replace(' ','').encode('utf-8')).hexdigest(), 16)
        if h_param % 2 == 0:
            answer_range = self.answers['yes']
        else:
            answer_range = self.answers['no']
        description='🎱 {}'.format(answer_range[random.randint(0,len(answer_range)-1)])
        await ctx.message.channel.send(embed=utils.embed_create(title='"{}"'.format(param), description=description))

    @magic8ball.error
    async def magic_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.channel.send(embed=constants.ERROR_MISSIM_PARAM)

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(Magic8Ball(client))