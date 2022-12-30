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

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(command_prefix='!', intents=intents)

bot = discord.Bot()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# slash command to add a restaurant to the picker
@bot.slash_command(name="addrestaurant",
                   description="Adds a restaurant to be chosen from. Users can add as many restaurants as they want.")
async def first_slash(ctx):
    await ctx.respond("You executed the add restaurant command!")


# slash command to see how many wins a particular user has
@bot.slash_command(name="score",
                   description="Returns the number of times a user has chosen the restaurant the group goes to.")
async def first_slash(ctx):
    await ctx.respond("You have helped choose __ restaurants!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


# runs the bot
client.run(TOKEN)
