from upState import upState
import discord
import os
import random


# TODO:
# implement choice in -say
# -edit option

client = discord.Client()

jalenChats = []

wisdom = []
name = []

helpMsg = """```jalenbot cmds
-say | talk to the esteemed jalen buffalo
-advice (question) | ask him for advice
-addLine | add jalen quote
-listLine | list jalen quotes
-delLine (list #)| remove jalen quote
-addAdvice | add advice
-listAdvice | list advice
-delAdvice (list #) | delete advice
-repeat (msg) | repeats a msg
-upload (file) | uploads a file (jpg, png, gif)
-pic | sends a random pic```"""

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def getQuotes(fn):
    f = open(fn, "r")
    quotes = f.readlines()

    for i in range(0, len(quotes)):
        quotes[i] = quotes[i].strip('\n')

    f.close()
    return quotes

def saveQuotes(arr,  fn):
    f = open(fn, "w")
    for x in arr:
        f.write(x+"\n")
    f.close()

def printQuotes(arr):
    arr = chunks(arr, 20)
    ct = 0
    msg = []
    final = []

    for x in arr:
        for y in x:
            msg.append( "{} {}".format(ct, y))
            ct += 1
        final.append("```" + "\n".join(msg) + "```")
        msg = []
             
    return final

@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.split(" ")
    jalenChats = getQuotes("lines.txt")
    wisdom = getQuotes("wisdom.txt")
    name = getQuotes("names.txt")

    #messages
    if message.content.startswith("-say"):
        if len(msg) == 1:
            await message.channel.send(random.choice(jalenChats))
        else:
            await message.channel.send(jalenChats[int(msg[1])])

    if message.content.startswith("-advice"):
        if len(msg) != 1:
            await message.channel.send(random.choice(wisdom))
        else:
            await message.channel.send("ask me a question wauaghh")

    #quotes options
    if message.content.startswith("-addLine"):
        jalenChats.append(" ".join(msg[1:]))
        saveQuotes(jalenChats, "lines.txt")
        for x in printQuotes(jalenChats):
            await message.channel.send(x)

    if message.content.startswith("-listLine"):
        for x in printQuotes(jalenChats):
            await message.channel.send(x)
    
    if message.content.startswith("-delLine"):
        try:
            del jalenChats[int(" ".join(msg[1:]))]
            saveQuotes(jalenChats, "lines.txt")
            for x in printQuotes(jalenChats):
                await message.channel.send(x)
        except:
            await message.channel.send("invalid input")  
    
    #advice options
    if message.content.startswith("-addAdvice"):
        wisdom.append(" ".join(msg[1:]))
        saveQuotes(wisdom, "wisdom.txt")
        for x in printQuotes(wisdom):
            await message.channel.send(x)

    if message.content.startswith("-listAdvice"):
        for x in printQuotes(wisdom):
            await message.channel.send(x)
    
    if message.content.startswith("-delAdvice"):
        try:
            del wisdom[int(" ".join(msg[1:]))]
            saveQuotes(wisdom, "wisdom.txt")
            for x in printQuotes(wisdom):
                await message.channel.send(x)
        except:
            await message.channel.send("invalid input")  
    
    if message.content.startswith("-help"):
        await message.channel.send(helpMsg)

    #repeat
    if message.content.startswith("-repeat"):
        await message.channel.send(" ".join(msg[1:]))

    #uploads
    if message.content.startswith("-upload"):
        types = ["png", "jpeg", "gif", "jpg"] 
        if len(message.attachments) == 0:
            await message.channel.send("no attachment provided")
        else:
            for x in message.attachments:
                if any(x.filename.lower().endswith(image) for image in types):
                    await x.save("./imgs/" + x.filename)
                    await message.channel.send("successfully uploaded")
    
    if message.content.startswith("-pic"):
        imgString = random.choice(os.listdir("./imgs/"))
        await message.channel.send(file=discord.File("./imgs/" + imgString))

    #nickname
        if message.content.startswith("-nick"):
            builder = ""
            for i in randrange(4):
                builder += name[i] + " "
            await message.channel.send(builder)
            

upState()
client.run(os.getenv('TOKEN'))