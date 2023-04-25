import discord
from discord.ext import tasks
import pandas as pd
import cv2
import io
import datetime
import requests

class BetonBot(discord.Client):
    def __init__(self):
      self.last_post = datetime.datetime(2012, 3, 5, 23, 8, 15)

      intents = discord.Intents.all()
      intents.message_content = True
      super().__init__(intents=intents)
      
    
    async def on_ready(self):
       print("BOT READY")
       self.channel = self.get_channel(1100334635382227004)
       self.update_data.start()

    @tasks.loop(seconds = 10)
    async def update_data(self):
       channel = self.get_channel(1100334635382227004)
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
          if new_max > max_height:
             df.loc[user_index, "max_height"] = new_max
             df.to_csv("data.csv", index=False)
             await channel.send("_ _ \n🚨 Nouveau record pour " + user + " 🚨 : " + str(new_max) + " mètres\n _ _")
             await self.display_performance(1)
         
          if height < current_height - 50:
             df.to_csv("data.csv", index=False)
             await channel.send("_ _ \n💀 Chute terrible de " + str(current_height - height) + " mètres pour " + user + " 💀\n _ _")
             await self.display_performance(1)
      
      
          df.to_csv("data.csv", index=False)

    async def display_performance(self, performance):
       channel = self.get_channel(1100334635382227004)
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
               name = player[0]
          
          if performance == 1:
            info += name + " : " + str(player[1]) + "m (Max : " + str(player[2]) + "m)\n"
          elif performance == 2:
            info += name + " : Max : " + str(player[2]) + "m\n"

          counter +=1 
          last_height = player[performance]
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
       



bb = BetonBot()
bb.run("MTEwMDMzMjkyMTY4NjA3NzQ1MA.Gjl5oy.TmhI1vlC4QbPysH-BGC_SFSNPjwNNE8ZKmf1q4")


"""response = requests.get("http://localhost:5000/get_height/")
data = response.json()
info = "\n"
heights = {}
performance = 2 #1 pour hauteur actuelle, #2 pour hauteur max
for i in range(len(data)):
   heights[i] = data[i][performance] 

heights_sorted = dict(sorted(heights.items(), key=lambda item: item[1], reverse=True))
counter = 0
last_height = 0
for key in heights_sorted:
   player = data[key]
   if counter != 0:
      splits = int((last_height - player[performance]) / 20)
      info += "-\n"*splits
   info += player[0] + " : " + str(player[1]) + "m (Max : " + str(player[2]) + "m)\n"
   counter +=1 
   last_height = player[performance]
   

print(info)"""


