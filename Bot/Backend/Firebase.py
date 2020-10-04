''' A google Firebase is used for dynamic purposes. Like XP gathering'''
# > ---------------------------------------------------------------------------
# > Imports
import Bot.Backend.constants as constants
import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, db

# > ---------------------------------------------------------------------------
class Firebase():

    def __init__(self, cred):
        _cred = credentials.Certificate(cred)
        firebase_admin.initialize_app(_cred, {
            'databaseURL' : constants.FIRE_URL
        })

    def update(self, path, value):
        ref = db.reference(path)
        ref.update(value)

    def setValue(self, path, value):
        ref = db.reference(path)
        ref.set(value)

    def delete(self, path):
        ref = db.reference(path)
        ref.delete()

    def get(self, path):
        ref = db.reference(path)
        return ref.get()