import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import requests
import json

PATH = 'Bot/Resources/json/fategrandorder.json'
API = constants.FGO_REST_API

def update():
    return