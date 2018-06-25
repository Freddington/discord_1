import discord
import random
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os

bot = commands.Bot('!')
client = discord.Client()
@bot.event
async def on_ready():
    print("Bot is ready")

@bot.command(pass_context = True)
async def commands():
    await bot.say("!ping")
    await bot.say("!coin")
    await bot.say("!dice")
    await bot.say("!eightball")
    await bot.say("!openpoll, !closepoll")
    
@bot.command(pass_context = True)
async def ping(ctx):
    await bot.say("pong")

#@bot.command(pass_context=True)
#async def info(ctx, user: discord.Member):
    #await bot.say("The users name is: {}".format(user.name))

@bot.command(pass_context = True)
async def coin(ctx):
    await bot.say(random.choice(["Heads","Tails"]))

@bot.command(pass_context = True)
async def dice(ctx):
    await bot.say(random.choice([1,2,3,4,5,6]))

@bot.command(pass_context = True)
async def embed(ctx):
    embed = discord.Embed()
    embed.set_footer()
    embed.set_author()
    embed.add_field()
    await bot.say(embed)

@bot.command(pass_context = True)
async def eightball(ctx):
    await bot.say(random.choice(["Yes", "Ask again later", "No"]))
    
@bot.command(pass_context = True)
async def openpoll(ctx, *, args):
    try:
        os.remove("poll.txt")
    except:
        pass
    await bot.say("What are your poll options?")
    await bot.say("Separate multiple options with '//'")
    options = await bot.wait_for_message(author = ctx.message.author, timeout = 30)
    options = options.clean_content.split("//")
    vote_txt = open("poll.txt", "w")
    vote_txt.write(str(len(options)) + "\n")
    vote_txt.write(ctx.message.author.id+'\n')
    vote_txt.write(args + '\n')
    for counter in range (len(options)):
        vote_txt.write(str(counter + 1) + ": " + options[counter] + "\n")
        await bot.say("Type: !vote " + str(counter + 1) + " for " + options[counter])
    vote_txt.close()

@bot.command(pass_context = True)
async def vote(ctx, *, args):
    try:
        vote_txt = open("poll.txt", "r")
        votes = vote_txt.readlines()
        vote_line = int(votes[0])
        vote_txt.close()
        vote_txt = open("poll.txt", "a")
        if int(args)<= vote_line and int(args) > 0: 
            vote_txt.write(args + ",")
        else:
            await bot.say("pick a real number faggot")
        vote_txt.close()
    except:
        await bot.say("There are no polls at this time")

@bot.command(pass_context = True)
async def closepoll(ctx):
    try:
        vote_txt = open("poll.txt", "r")
        votes = vote_txt.readlines()
        vote_txt.close()
        if ctx.message.author.id == votes[1].strip('\n'):
            vote_num = int(votes[0])
            vote_line = votes[-1][:-1].split(",")
            vote_line.sort()
            counter = 0
            lst = []
            for i in range(vote_num):
                lst.append(0)
            for element in vote_line:
                lst[int(element)-1] += 1
        
            for i in range(len(lst)):
                await bot.say(votes[i+3].strip('\n') + " count: " + str(lst[i]))
            os.remove("poll.txt")
    except: 
        await bot.say("There are no polls for this time")
        os.remove("poll.txt")
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id != bot.user.id and 'nigger' in message.content or message.author.id != bot.user.id and 'faggot' in message.content:
        await bot.delete_message(message)
        await bot.send_message(message.channel, "Hey, we dont say those words around here "+ message.author.name)
    if "im hungry" in message.content:
        await bot.send_message(message.channel, "Then why dont you cook some food, "+message.author.name)

bot.run("###")
