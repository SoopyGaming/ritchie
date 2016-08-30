# RITchie
---
## RITchie is a stat tracking bot for the RIT eSports Discord server.

#### Games RITchie currently tracks

* Heroes of the Storm
* Overwatch

#### Games RITchie will soon be able to track (in order of development priority)

* Rocket League
* Counter Strike
* Dota 2
* League of Legends

#### Other features that will be added:
* Random match startup (picks maps/sides)
* Tournament mode (team building & automatic role/channel creation)

---
## How to Install

#### Hosted Version:
Adding RITchie to your server is easy as cake, just click the link below.

[Add RITchie to your Discord server](https://discordapp.com/oauth2/authorize?client_id=207294266681196544&scope=bot&permissions=0)

#### Self Hosted Version:
Want to mess around a bit more, or add your own branding to the bot? Instructions are below.
######Install
```
$ git clone http://www.github.com/evanextreme/ritchie.git
$ cd ritchie
$ pip install discord.py
```
######Run
```
$ python ritchie.py discord_bot_token
```
Depending on what versions of Python are installed, you might need to replace `python` for `python3`
