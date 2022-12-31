# bot.py
import os
import sys
import random

import discord
from dotenv import load_dotenv

# gets the token from the .env file
load_dotenv()
TOKEN: str = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("Error, Token is not valid")
    sys.exit(1)

# creates a bot object
bot = discord.Bot()

Options = {}

Score = {}


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# slash command to add a restaurant to the picker
@bot.slash_command(name="addrestaurant", guild_ids=[1032437764614012988],
                   description="Adds a restaurant to be chosen from. Users can add as many restaurants as they want.")
async def addRestaurant(interaction: discord.Interaction, restaurant):
    if interaction.user.id not in Options:
        Options[interaction.user.id] = restaurant
    elif isinstance(Options[interaction.user.id], list):
        Options[interaction.user.id].append(restaurant)
    else:
        Options[interaction.user.id] = [Options[interaction.user.id], restaurant]

    await interaction.response.send_message(f'{interaction.user} added {restaurant} to the choices!')


@bot.slash_command(name="random", guild_ids=[1032437764614012988],
                   description="Have the bot randomly pick a restaurant from the list of options.")
async def randomChoice(interaction: discord.Interaction):

    outputMessage: str = ''

    if not Options:
        outputMessage = 'Hey! The bot can\'t pick a restaurant if there are no options to choose from!'
    else:

        # picks a random restaurant submitted by a user from the options dictionary
        restaurants = list(Options.values())
        randNum: int = random.randint(0, len(restaurants) - 1)
        name: str = restaurants[randNum]

        # if the value is a list, pick a random restaurant from the list
        if isinstance(restaurants[randNum], list):
            output: int = random.randint(0, len(restaurants[randNum]) - 1)
            name = restaurants[randNum][output]

        if interaction.user.id not in Score:
            Score[interaction.user.id] = 1
        else:
            Score[interaction.user.id] += 1

        outputMessage = 'The restaurant chosen is: ' + name

    await interaction.response.send_message(outputMessage)


# slash command to see how many wins a particular user has
@bot.slash_command(name="score", guild_ids=[1032437764614012988],
                   description="Returns the number of times a user has chosen the restaurant the group goes to.")
async def score(interaction: discord.Interaction):

    userScore: int = 0
    for key in Score:
        if interaction.user.id == key:
            userScore = Score[interaction.user.id]
            break
        else:
            userScore = 0

    if userScore == 1:
        grammar = 'time'
    else:
        grammar = 'times'
    await interaction.response.send_message(f'{interaction.user} has chosen the restaurant {userScore} {grammar}!')


@bot.slash_command(name="options", guild_ids=[1032437764614012988], description="Returns the valid options that users "
                                                                                "have submitted")
async def options(interaction: discord.Interaction):
    optionMessage: str = ''
    if not Options:
        optionMessage = 'Sorry, there are currently no restaurants being considered!'
    else:
        # need to add the code here to check for all the restaurants being considered, either in a list or singular
        optionMessage = 'Hello world'

    await interaction.response.send_message(optionMessage)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


# runs the bot
bot.run(TOKEN)
