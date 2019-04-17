import discord
import watson
import asyncio
import configparser
import os
from discord.ext.commands import Bot

if (not os.path.isfile(os.path.join(os.path.dirname(__file__), "config.ini"))):
    print("No config file found, make sure you have one in the same directory as this python script\nexiting")
    quit()

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

TOKEN = config["DEFAULT"]["DISCORD_KEY"]
BOT_PREFIX = ("!", "$")

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name="memealyze",
        description="When uploading image include command \"!memealyze\" | \"!Memealyze\" | \"!MemeAlyze\" | \"!ma\" as a comment", 
        brief="Neural network put to good use",
        aliases=["Memealyze", "MemeAlyze", "ma"],
        pass_context=True)

async def GetMemeContents(context):
    await client.say("Sending image to the mothership, hold tight.")
    
    if(not context.message.attachments):
        await client.say(
                "Couldn't find image attachement. Make sure you include \"!memealyze\" or any of it's variants as a comment when submitting an image") 
        return

    imageUrl = str(context.message.attachments[0]["url"])
    messageContent = ""
    resultDict = watson.ReturnWatsonResults(imageUrl)
    
    for key,val in resultDict.items():
        messageContent += "{} : {}%\n".format(key, val)

    await client.say("Done, the boys at IBM said they found this:\n" + messageContent) 

async def servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Servers meme bot presides over")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(servers())
client.run(TOKEN)
