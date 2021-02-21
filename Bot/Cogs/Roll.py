''' ROLL.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil
import random

ALIASES = ['r']

# > ---------------------------------------------------------------------------
class Roll(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}roll'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Rolls die for you.\n\n{}**Usage: ** `{}roll <amount>w<type>(*<amount>)`\n**Example: ** `{}roll 1w100*5` - rolls 1 dice from 1 to 100 and multiplies the result with 5'.format(alias, constants.INVOKE, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def roll(self, ctx, *, param):
        param = param.lower().replace(' ','').strip()
        if 'w' not in param:
            await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)
            return
        amount1 = param[:param.find('w')]
        if amount1 == '':
            amount1 = 1
        if '*' in param:
            _param = param[param.find('w') + 1:].split('*')
            dice_type = _param[0]
            amount2 = _param[1]
        else:
            dice_type = param[param.find('w') + 1:]
            amount2 = 1
        
        try:
            amount1 = int(amount1)
            dice_type = int(dice_type)
            amount2 = float(amount2)
        except:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return

        if amount1 < 1 or amount1 > 500 or dice_type < 2 or amount2 < 1:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return
        
        results = []
        total = 0
        for i in range(0, amount1):
            result = int(random.randint(1, dice_type + 1) * amount2)
            total += result
            results.append(result)
        title = '{} rolled {}w{}'.format(ctx.message.author.display_name, amount1, dice_type)
        if amount2 != 1:
            title += ' (multiplied by {})'.format(amount2)
        if amount1 == 1:
            description = '**Result** : {}'.format(results[0])
        else:
            description = '**Results** : {}\n**Total** : {}'.format(', '.join([str(x) for x in results]), total)
        await utils.embed_send(ctx, utils.embed_create(title=title, description=description))

    @roll.error
    async def roll_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Roll(client))