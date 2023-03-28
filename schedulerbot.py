import discord
from discord.ext import commands, tasks
import os
from datetime import datetime, timedelta, date

#Imports function
from dotenv import load_dotenv

#Loads the .env file
load_dotenv()

#Gets api token from .env
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

#Gets the client object from discord.py. Client is synonomous with bot.
bot = discord.Client()

#Event listener for when the bot has switched from offline to online.
@bot.event
async def on_ready():
        #Creates a counter to keep track of how many guilds/servers the bot is connected to.
        guild_count = 0

        #Loops through all the guild/servers that the bot is associated with.
        for guild in bot.guilds:
                #Print the server's ID and name.
                print(f" - {guild.id} (name: {guild.name})")

                #Increments the guild counter.
                guild_count = guild_count + 1
        
        #Prints how many guilds/servers the bots is in.
        print("School Scheduler is in " + str(guild_count) + " guilds.")

@bot.event
async def on_message(message):
        #Checks if the message that was sent is equal to "hello".
        if "!assn" in message.content:
                #sends back a message to the channel.
                await message.channel.send("Added to assignments!")
                f = open("schedule.txt", "a")
                #f.write(message.content)
                str = message.content
                str = str.replace("!assn ", '')
                f.write(str + "\n")

        #command to output list of assignments/tests due
        if message.content == "!list":
                f = open("schedule.txt", "r")
                await message.channel.send(f.read())



@tasks.loop(hours=24)
async def notify():
        channel = bot.get_channel(974801881928958013)

        #Notifies guild members of any upcoming assignments/tests within 
        dateOne = date.today()
        dateTwo = date.today() + timedelta(days=1)
        dateThree = date.today() + timedelta(days=2)
        dateFour = date.today() + timedelta(days=3)

        dateOne = dateOne.strftime("%m/%d/%Y")
        dateTwo = dateTwo.strftime("%m/%d/%Y")
        dateThree = dateThree.strftime("%m/%d/%Y")
        dateFour = dateFour.strftime("%m/%d/%Y")

        with open("schedule.txt") as file:
                lines = file.readlines()

        first = True 

        for line in lines:
                if (dateOne in line or dateTwo in line or dateThree in line or dateFour in line):
                        if (first):
                                await channel.send("@everyone")
                                first = False
                        await channel.send(line)


        if (dateOne in lines[0]):
                del lines[0]

        file.close()
        file2 = open("schedule.txt", "w")
        file2.writelines(lines)

@notify.before_loop
async def before():
        await bot.wait_until_ready()
        print("Finished waiting")

notify.start()
#Executes the bot with the specified token.
bot.run(DISCORD_TOKEN)