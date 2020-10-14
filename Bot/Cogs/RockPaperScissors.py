''' ROCKPAPERSCISSORS.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import random

ALIASES = ['rps', 'scheresteinpapier', 'ssp']

# > ---------------------------------------------------------------------------
class RockPaperScissors(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.emotes = {'✊' : 'Rock','✋' : 'Paper','✌️' : 'Scissors'}
        self.desc = '\n'.join(['{} - {}'.format(x, self.emotes[x]) for x in self.emotes.keys()])

    def help(self, footer):
        title = 'Help Info: {}rockpaperscissors'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Let\'s you play \'rock-paper-scissors\' with Kohaku.\n\n{}**Usage: ** `{}rockpaperscissors`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def rockpaperscissors(self, ctx, *, param):
        message = await utils.embed_send(ctx, utils.embed_create(title='Rock-Paper-Scissors!', description='{}, please react with your choice!\n{}'.format(ctx.message.author.mention, self.desc)))
        for emote in self.emotes.keys():
            await message.add_reaction(emote)
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reaction, user: user.id == ctx.message.author.id)
            reacted = True
        except:
            reacted = False
        if reacted == False or reaction.emoji not in self.emotes.keys():
            await message.edit(embed=utils.embed_create(title='Rock-Paper-Scissors : Timeout!', description='Match postponed!'))
        else:
            choice = list(self.emotes.keys())[random.randint(0, len(self.emotes.keys())-1)]
            result = self.match(self.emotes[choice], self.emotes[reaction.emoji])
            if result == 'DRAW':
                desc = 'Oh ehm .... it\'s a draw... yay ?'
            elif result == 'KOHAKU':
                desc = 'Hehe! I won!'
            else:
                desc = 'Congrats! You won! I know you could do it!'
            await message.edit(embed=utils.embed_create(title='Rock-Paper-Scissors : Results!', description='Kohaku: {}\n{} : {}\n\n{}'.format(choice, ctx.message.author.mention, reaction.emoji, desc)))


    @rockpaperscissors.error
    async def rockpaperscissors_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.rockpaperscissors(ctx, param='RPS')
            return

    def match(self, kohaku, player):
        if kohaku == player:
            return 'DRAW'
        elif (kohaku == 'Rock' and player == 'Paper') or (kohaku == 'Paper' and player == 'Scissors') or (kohaku == 'Scissors' and player == 'Rock'):
            return 'PLAYER'
        else:
            return 'KOHAKU'


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(RockPaperScissors(client))