''' CHECKS.py '''
# > ---------------------------------------------------------------------------
# > Imports
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


# > Secret
def check_is_secret(cog):
    try:
        return cog.isSecret()
    except:
        return False