import discord
from discord.ext import commands
import json

from algo_stack import algo

with open('./config/config.json') as json_file:
    json_data = json.load(json_file)

token = json_data["discord"]["token"]
client = commands.Bot(command_prefix = '>')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def select(ctx, context):
    await algo.crawling(context.split(","), ctx)

client.run(token)