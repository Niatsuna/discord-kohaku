# Kohaku
<img width="150" height="150" align="left" style="float: left; margin: 0 10px 0 0;" alt="Kohaku" src="https://assets.gitlab-static.net/uploads/-/system/project/avatar/20396064/cdn_discordapp_com-e72850ba63a9815a37c06f6401f5fb1a.png?width=64">

Kohaku is a open source Discord bot coded in Python with [discord.py](https://discordpy.readthedocs.io/en/latest/) by Niatsuna
The bot is specified on certain games and is merely a hobby project.<br>
If you need help or want to share critique, please contact Niatsuna on Discord via: <br>✦ Niatsuna ✦#6787.
<br>
<br>
**Needed**:<br>
![](https://img.shields.io/badge/python-v3.7-brightgreen)
## Getting Started
### :exclamation: Requirements
To get Kohaku working you first and foremost need **at least** these modules.
Each and everyone can be installed using
```
pip install <module>
```
![](https://img.shields.io/badge/beautifulsoup4-v4.9.0-blue)
![](https://img.shields.io/badge/discord.py-v1.3.4-%237289DA)
![](https://img.shields.io/badge/Pillow-v7.1.2-blue)
![](https://img.shields.io/badge/requests-v2.23.0-blue)
![](https://img.shields.io/badge/lxml-v4.5.1-blue)
![](https://img.shields.io/badge/Unidecode-v1.1.1-blue)
<br>

All these requirements can also be found in the [requirements.txt](requirements.txt) file which is used to deploy Kohaku at the moment.<br>
This documentation should be updated on a regular basis but if something is missing check out the file instead.<br>
<br>**Note**: To see which versions you already installed use `pip freeze`

### :o: Running
Use
```
python app.py $DISCORD_TOKEN
```
to start Kohaku. After that Kohaku is loading, loggin into the bot account based on the token and informs you when it's ready. Have fun!
Thanks to @fwcd Docker Deployment is possible! (Thank you very much <3)

### Usage
**DISCLAIMER:** Because this is a hobby project and open-source you are free to use Kohaku as you like but it's your responsibility! This code is not bug-free or perfect. So if anything might happend and you didn't wanted that: Sorry bud, but that's on you. We are happy to help but i will not be your scapegoat. For anything else read the [GPU License](LICENSE.md).

<br><br>
The prefix for Kohaku is defined in `constants.py` in the Backend Folder. On default it is `-` but can be changed before running.
To use Kohaku type the prefix , the module and then other parameters.<br>
`-help` will show you a help message and goes into more detail. <br>
**Example:**<br>
<img align="right" alt="Example_Usage" src="https://i.gyazo.com/5f7683368f276f083f2e759fa7fe680e.png"> The Magic 8 Ball Module is callable with `8b`. With the default settings use<br>
`
-8b <question>
`<br>
to ask Kohaku and you will get a yes or no.
<br><br><br>
<br><br><br>
<br><br><br>

## Features
Kohaku is specialized for little discord games and information about third-party games.

Entries marked with an  :no_entry_sign: are currently not available but planned.

### Discord Games
* Would you rather - `wyr`
* Never have i ever - `nhie`
* Hangman - `hangman` :no_entry_sign:
* Magic 8Ball - `8b`

### Game Information
* Animal Crossing : New Horizons - `ac`
* Dead by Daylight - `dbd`
* Fate/Grand Order - `fgo` :no_entry_sign:
* Pokémon - `pkm`  :no_entry_sign:

### Other Features
* LaTex compiling - `latex`  :no_entry_sign:
* Math solver - `math` :no_entry_sign:

Other features which are not listed here are either hidden, admin tools or little gimmicks.

## Special Thanks
To these awesome people that are testing Kohaku for free:<br>
<img align="middle" alt="Thanks" src="https://thumbs.gfycat.com/BrownDependableDowitcher-size_restricted.gif">
<br>
<i align="center" style="font-size: .85em">Source: Anime "Anima Yell!"</i>

* Nariax3 (Stuff i was too lazy to do)
* Lirby
* fwcd (Docker Stuff)
* Awesome people from THE IT-Server
* Awesome people from the Johann25-Server °L° (Check JohannaBDK out! Awesome streams & Co :D)
* Many more !