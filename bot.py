# bot.py
import os
import sys

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

Options = []

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# slash command to add a restaurant to the picker
@bot.slash_command(name="addrestaurant", guild_ids=[1032437764614012988],
                   description="Adds a restaurant to be chosen from. Users can add as many restaurants as they want.")
async def addRestaurant(interaction: discord.Interaction, restaurant):
    Options.append(restaurant)
    await interaction.response.send_message(f'{interaction.user} added {restaurant} to the choices!')


# slash command to see how many wins a particular user has
@bot.slash_command(name="score", guild_ids=[1032437764614012988],
                   description="Returns the number of times a user has chosen the restaurant the group goes to.")
async def score(interaction: discord.Interaction):
    await interaction.response.send_message(f'{interaction.user} has chosen the restaurant ___ times!')


@bot.slash_command(name="options", guild_ids=[1032437764614012988], description="Returns the valid options that users "
                                                                                "have submitted")
async def options(interaction: discord.Interaction):
    output: str = ' , '.join(Options)

    await interaction.response.send_message(f'The current options to choose from are: ' + output)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


# runs the bot
bot.run(TOKEN)
