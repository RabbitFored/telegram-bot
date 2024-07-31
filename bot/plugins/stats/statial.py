from pyrogram import Client, filters
from bot.core import utils
from bot.core import database as db
from bot.core import filters as fltr

'''  
def create_statistics_graph(stats):
           import matplotlib.pyplot as plt
       
           labels = 'Active Users', 'Inactive Users'
           sizes = [stats['active_users'], stats['total_users'] - stats['active_users']]
           colors = ['#ff9999','#66b3ff']
           explode = (0.1, 0)

           plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
           plt.axis('equal')
           plt.title('User Activity')
           plt.savefig('user_activity.png')
           plt.close()
          '''  
@Client.on_message(filters.command(["statial"])  & fltr.group("admin") )
async def statial(client, message):
       #stats = db.get_active_users()
       #create_statistics_graph(stats)
       
       stat = db.get_statial()
       
       users = db.bot_db["botdata"].count_documents({})
       text = "**Statial**\n\n"
       text += f"**Total Users:** {users}\n"                                
       for i in stat:
           if not i == "_id":
             text += f"**{i}:** {stat[i]}\n" 
       await message.reply_text(text)