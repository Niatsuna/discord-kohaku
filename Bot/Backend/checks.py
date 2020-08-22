''' CHECKS.py - Stores Bot Checks like 'does a file exist for that use?', 'is this user an admin?' etc. '''
# > ---------------------------------------------------------------------------
# > Imports
from Bot.Backend.utils import json_load

# > Admin
def check_is_admin(ctx):
    author_id = ctx.message.author.id
    json = json_load('Bot/Resources/json/admin.json')
    return author_id == json['owner'] or author_id in json['admins']

# > Secret
def check_is_secret(cog):
    try:
        return cog.isSecret()
    except:
        return False
