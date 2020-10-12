''' EDIT-PROFILE.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil

ALIASES = ['edit', 'ep', 'profile-edit', 'pe']

# > ---------------------------------------------------------------------------
class EditProfile(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}edit-profile'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Edits your Kohaku-Profile.\nYou need to specify which aspect you want to edit. Sending only the aspect will clear this aspect for your profile.\nAspects currently are: `description`.\n**Note:** Separate multiple aspects with `|`\n\n{}**Usage: ** `{}edit-profile` `[<aspect> <input>]`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, name='edit-profile', aliases=ALIASES)
    async def editProfile(self, ctx, *, param):
        aspects = param.split('|')
        db_path = 'users/{}'.format(ctx.message.author.id)
        data = constants.FIRE_CON.get(db_path)
        if data == None:
            data = constants.EMPTY_USER
            constants.FIRE_CON.setValue(db_path, data)
        success = []
        failed = []
        for asp in aspects:
            sp = asp.strip().split(' ')
            aspect = sp[0].lower()
            if aspect in data.keys():
                if len(sp) == 1:
                    data[aspect] = '-'
                    success.append(aspect)
                else:
                    inp = ' '.join(sp[1:]).strip()
                    if len(inp) > 1024 or len(inp.split('\n')) > 20: # Field Value max 1024 chars + no more then 20 lines
                        failed.append(aspect)
                    else:
                        data[aspect] = inp
                        success.append(aspect)
            else:
                failed.append(aspect)
        constants.FIRE_CON.update(db_path, data)
        if len(failed) == 0:
            await utils.embed_send(ctx, utils.embed_create(title='Update profile : Success', description='{}\'s profile was updated successfully!'.format(ctx.message.author.mention)))
        else:
            await utils.embed_send(ctx, utils.embed_create(title='Update profile : Failed', description='{}\'s profile couldn\'t be updated for {} aspects ({} successful). These aspects were: \n{}'.format(
                ctx.message.author.mention, len(failed), len(success), ', '.join(['`{}`'.format(x) for x in failed]))))

    @editProfile.error
    async def editProfile_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return

# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(EditProfile(client))