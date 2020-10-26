''' CHECKS.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
import Bot.Backend.constants as constants

# > ---------------------------------------------------------------------------
# > Admin
def check_rank(rank_num, rank):
    num = -1
    for (k,v) in constants.RANK_MAP.items():
        if v == rank:
            num = k
            break
    if num <= rank_num:
        return True
    return False

def check_is_rank(i, rank_string):
    data = constants.FIRE_CON.get('users/{}'.format(i))
    if data == None or not check_rank(data['rank'], rank_string):
        return False
    return True

def check_is_mod(ctx):
    return check_is_rank(ctx.message.author.id, 'Moderator')

def check_is_admin(ctx):
    return check_is_rank(ctx.message.author.id, 'Admin')

def check_is_owner(ctx):
    return check_is_rank(ctx.message.author.id, 'Owner')

# > Channel
def check_is_dm(ctx):
    return ctx.message.channel.type == discord.ChannelType.private

def check_is_guild(ctx):
    return (not check_is_dm(ctx)) # Because Bots can't join private groups only DMs and Guilds are possible

# > Secret
def check_is_secret(cog):
    try:
        return cog.isSecret()
    except:
        return False