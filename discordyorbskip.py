# bot.py
import os
import cv2
import time
import numpy as np
import datetime
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def draw_cal():
    text ="__Calendar Commands__\nadd,[name],[racers],[date],[time],[host]\nedit,[Original date],[Original name],[racers],[date],[time],[host],[commentate]\ncommentate,[name],[date],[user]\n\n Dates are formated: Month Abbreviation XX. Ex: Jan 03\n\n"    
    x = datetime.datetime.now()
    datelist = [x]
    for i in range(6):
        datelist.append(x+ datetime.timedelta(days=(1 + i )))
    
    
    for i in range(7):
        text = text + "__**"+datelist[i].strftime("%b") + ' '+datelist[i].strftime("%d")+"**__ \n\n"
        f = open("datefile.txt", "r")
        for g in f:
            date = g.split("$")
            if(date[0] == (datelist[i].strftime("%b") + ' '+datelist[i].strftime("%d"))):
                text = text + "**"+ date[1] + "**   @ "+ date[3]+ "        "+ date[2] + "\nHost: "+date[4] + "    |   Commentators: "+date[5]+"\n"        

        f.close()   
    
    #print(text)
    return text




@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    for channel in guild.text_channels:
        if channel == client.get_channel(761004087369138177):
            #remove roles
            x = guild.members
            for i in x:
                if get(guild.roles, name='bot') in i.roles:
                    await i.remove_roles(get(guild.roles, name='bot'))

            
            response = draw_cal()
            message = await channel.fetch_message(761004454945226753)        
            await message.edit(content=response) 

            #time.sleep(10)
            #add roles
            x = datetime.datetime.now()
            f = open("datefile.txt", "r")
            for g in f:
                date = g.split("$") 
                if(date[0] == (x.strftime("%b") + ' '+x.strftime("%d")) or date[0]+datetime.timedelta(days=(1)) == (x.strftime("%b") + ' '+x.strftime("%d"))):    
                    com = date[6].split("&")
                    for y in com:
                        user = guild.get_member(int(y))                        
                        await user.add_roles(get(guild.roles, name='bot'))           
            
            
            
  
     
    
    
    
    
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "create2313":
        await message.delete()
        print(get(message.guild.roles, name='Commentator'))
    if message.content == "Yorb":
            await message.channel.send("Skip")     
          
    if client.get_channel(761004087369138177) == message.channel:
        mess = message.content.split(",")
        print(mess)
        # add [name] [racers] [date] [time] [host]
        if mess[0] == 'add' and len(mess) == 6 and (get(message.guild.roles, name='Admin') in message.author.roles or get(message.guild.roles, name='Organizer') in message.author.roles):
            
            f = open("datefile.txt", "a")
            f.write(mess[3].strip()+"$"+mess[1].strip()+"$"+mess[2].strip()+"$"+mess[4].strip()+"$"+mess[5].strip()+"$"+"None - Volunteer Now!$"+str(message.author.id)+"$\n")
            f.close()
            response = draw_cal()
            await message.delete()
            message = await message.channel.fetch_message(761004454945226753)        
            await message.edit(content=response) 
            #await message.channel.send(response)
        # commentate [name] [date] [user]
        elif mess[0] == 'commentate' and len(mess) == 4:
            text1 =""
            text2=""
            f = open("datefile.txt", "r")
            for g in f:
                date = g.split("$")
                com=""
                if date[5] == "None - Volunteer Now!":
                    com = mess[3].strip()
                else:
                    com= date[5] + ","+ mess[3].strip()
                if(date[0] == mess[2].strip() and date[1] == mess[1].strip()):
                    text1 = g
                    text2 = date[0]+"$"+date[1]+"$"+date[2]+"$"+date[3]+"$"+date[4]+"$"+com+"$"+date[6]+"&"+str(message.author.id)+"$\n"
            f.close()
            replace("datefile.txt",text1,text2)
            response = draw_cal()
            await message.delete()
            message = await message.channel.fetch_message(761004454945226753)        
            await message.edit(content=response)   

            x = datetime.datetime.now()
            f = open("datefile.txt", "r")
            for g in f:
                date = g.split("$") 
                if(date[0] == (x.strftime("%b") + ' '+x.strftime("%d")) or date[0]+datetime.timedelta(days=(1)) == (x.strftime("%b") + ' '+x.strftime("%d"))):    
                    com = date[6].split("&")
                    for y in com:
                        user = message.guild.get_member(int(y))                        
                        await user.add_roles(get(message.guild.roles, name='bot'))           




            
        # edit [Original date] [Original name] [racers] [date] [time] [host] [commentate]
        elif mess[0] == 'edit' and len(mess) == 8 and (get(message.guild.roles, name='Admin') in message.author.roles or get(message.guild.roles, name='Organizer') in message.author.roles):
            text1 =""
            text2=""
            f = open("datefile.txt", "r")
            for g in f:
                date = g.split("$")
                if(date[0] == mess[1].strip() and date[1] == mess[2].strip()):
                    text1 = g
                    text2 = mess[4].strip()+"$"+mess[2].strip()+"$"+mess[3].strip()+"$"+mess[5].strip()+"$"+mess[6].strip()+"$"+mess[7].strip()+"$"+date[6]+"$\n"
            f.close()
            replace("datefile.txt",text1,text2)
            response = draw_cal()
            await message.delete()
            message = await message.channel.fetch_message(761004454945226753)        
            await message.edit(content=response)
        
        
        else:            
            await message.delete()
    return

client.run(TOKEN)