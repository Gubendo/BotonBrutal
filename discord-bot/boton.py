import discord
from discord.ext import tasks
import pandas as pd
import cv2
import io
import datetime
import requests
import argparse

class BetonBot(discord.Client):
    def __init__(self, channel):
      self.last_post = datetime.datetime(2012, 3, 5, 23, 8, 15)
      self.channel = channel 

      intents = discord.Intents.all()
      intents.message_content = True
      super().__init__(intents=intents)
      
    
    async def on_ready(self):
       print("BOT READY")
       self.update_data.start()
       await self.user.edit(username="Breton Brutal")
       await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='du haut de ses 457m'))

    @tasks.loop(seconds = 10)
    async def update_data(self):
       channel = self.get_channel(self.channel)
       response = requests.get("http://gubendo.pythonanywhere.com/get_height/")
       data = response.json()
       df = pd.read_csv("data.csv")

       for player in data:
          user = player[0]
          height = player[1]
          new_max = player[2]

          for index, row in df.iterrows():
             if row["player"] == user:
                   current_height = row["current_height"]
                   max_height = row["max_height"]
                   user_index = index

          df.loc[user_index, "current_height"] = height
          if new_max > max_height + 10:
             df.loc[user_index, "max_height"] = new_max
             df.to_csv("data.csv", index=False)
             await channel.send("_ _ \n🚨 Nouveau record pour " + user + " 🚨 : " + str(new_max) + " mètres\n _ _")
             await self.display_performance(1)
         
          if height < current_height - 50:
             df.to_csv("data.csv", index=False)
             await channel.send("_ _ \n💀 Chute terrible de " + str(current_height - height) + " mètres pour " + user + " (" + str(current_height) + "m -> " + str(height) + "m) 💀\n _ _")
             await self.display_performance(1)
      
      
          df.to_csv("data.csv", index=False)

    async def display_performance(self, performance):
       channel = self.get_channel(self.channel)
       response = requests.get("http://gubendo.pythonanywhere.com/get_height/")
       data = response.json()
       info = "\n"
       heights = {}
       for i in range(len(data)):
          heights[i] = data[i][performance] 

       heights_sorted = dict(sorted(heights.items(), key=lambda item: item[1], reverse=True))
       counter = 0
       last_height = 0
       for key in heights_sorted:
          player = data[key]
          if counter == 0:
             name = "🏆 " + player[0]
          else:
             splits = int((last_height - player[performance]) / 20)
             info += "-\n"*splits
             if counter == 1:
               name = "🥈 " + player[0]
             elif counter == 2:
               name = "🥉 " + player[0]
             else:
               name = "💩 " + player[0]
          
          if performance == 1:
            info += name + " : " + str(player[1]) + "m (Max : " + str(player[2]) + "m)\n"
          elif performance == 2:
            info += name + " : Max : " + str(player[2]) + "m\n"

          counter +=1 
          last_height = player[performance]
       splits = int(last_height / 20)
       info += "-\n"*splits
       info += "\n🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨\n"
       await channel.send(info)


       
    async def on_message(self, message):
       if message.author.bot:
         return
       
       if "!beton" in message.content:
          await self.display_performance(1) #1 pour hauteur actuelle, #2 pour hauteur max
       elif "!maxeur" in message.content:
          await self.display_performance(2)
       else:
          return



parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true')
parser.add_argument('--token', default="")

args = parser.parse_args()

if args.dev:
   channel = 1100334635382227004
else:
   channel = 1100461581072085012

bb = BetonBot(channel)
bb.run(args.token)




