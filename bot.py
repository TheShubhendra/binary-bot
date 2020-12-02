from telegram.ext import Updater, MessageHandler, CommandHandler,Filters
import pickle
import datetime 
import csv
from decouple import config
from coffeehouse import LydiaAI
TOKEN=config("TOKEN")
KEY=config("KEY")
lydia=LydiaAI(KEY)
try:
  with open("sessions","rb") as f:
    sessions = pickle.load(f)
except:
  sessions = {}
def think(inp,session):
  return session.think_thought(inp)
def chat(update,context):
  
  text = update.message.text
  chat_id = update.message.chat_id
  user_id = update.message.from_user.id
  if user_id in sessions:
    session=sessions[user_id]
  else:
    session=lydia.create_session()
    sessions[user_id]=session
    with open("sessions","wb") as f:
      pickle.dump(sessions,f)
  reply  = think(text,session)
  time=str(datetime.datetime.now())
  data=[time,chat_id,user_id,text,reply]
  print(data)
  with open("data.csv","a") as f:
    writer=csv.writer(f)
    writer.writerow(data)
  update.message.reply_text(reply)
def main():
  global session
  updater = Updater(TOKEN,use_context=True)
  dispatcher = updater.dispatcher
  dispatcher.add_handler(MessageHandler(Filters.text,chat))
  updater.start_polling()
  
if __name__=='__main__':
  main()