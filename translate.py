from operator import concat
import os
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters 
import googletrans
from googletrans import Translator

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

translator = Translator()

user_preference = {}

# all_lang = googletrans.LANGUAGES
# langcodes = dict(map(reversed,all_lang.items()))
langcodes = googletrans.LANGUAGES

def start(update, context):
  message = "Welcome " + update.message.from_user.first_name
  context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def check_lang(update,context):
  user = update.message.from_user.username
  try:
    send_message = "Language is set to " + user_preference[user].upper()
    context.bot.send_message(chat_id = update.effective_chat.id, text = send_message)
  except:
    send_message = "No language has been set yet"
    context.bot.send_message(chat_id = update.effective_chat.id, text = send_message)

def set_preferences(update,context):
  user = update.message.from_user.username
  msg = update.message.text
  msg = msg.split(' ')[1:].strip()
  msg = msg.lower()
  if len(msg) == 0:
    context.bot.send_message(chat_id = update.effective_chat.id, text = "No valid placeholders. Please run the command again!!")
  elif msg not in langcodes.keys():
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Language code not supported by Google Translate")
  else:
    try:
      user_preference[user] = msg
    except:
      user_preference[user] = msg
    text_message = str(msg.upper()) + " set for " + update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text = text_message)

def translate(update,context):
  user = update.message.from_user.username
  try:
    translation_language = user_preference.get(user, "en")
  except:
    context.bot.send_message(chat_id=update.effective_chat.id, text = "You have not set a language for translation")
    return
  msg = update.message.text
  msg = ''.join(msg.split(' ')[1:])
  if len(msg) == 0:
    context.bot.send_message(chat_id = update.effective_chat.id, text = "No valid placeholders. Please run the command again!!")
  else:
    msg = msg.strip().lower()
    translated = translator.translate(msg,dest = translation_language)
    send_message = "T: " + str(translated.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text = send_message)

def translate_lang(update,context,lang):
  user = update.message.from_user.username
  translation_language = lang
  msg = update.message.text
  msg = ''.join(msg.split(' ')[1:])
  if len(msg) == 0:
    context.bot.send_message(chat_id = update.effective_chat.id, text = "No valid placeholders. Please run the command again!!")
  else:
    msg = msg.strip().lower()
    translated = translator.translate(msg,dest = translation_language)
    send_message = lang + ": " + str(translated.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text = send_message)

def translate_en(update,context):
  return translate_lang(update,context,"en")

def translate_th(update,context):
  return translate_lang(update,context,"th")

def translate_ru(update,context):
  return translate_lang(update,context,"ru")

def unknown(update, context):
  send_message = "Basic help: /t - transalte, /en - eng, /th - thai, /ru - ru. Example: /ru Hey"
  context.bot.send_message(chat_id=update.effective_chat.id, text=send_message)

def check_language(update,context):

    msg = update.message.text
    msg = ''.join(msg.split(' ')[1:])
    if len(msg) == 0:
      context.bot.send_message(chat_id = update.effective_chat.id, text = "No valid placeholders. Please run the command again!!")
    else:
      msg = msg.strip()
      language = translator.detect(msg)
      lang_text = all_lang[language.lang.lower()]
      send_message = "Detected language: " + str(lang_text.upper()) + " Confidence: " + str(language.confidence)
      context.bot.send_message(chat_id = update.effective_chat.id, text = send_message)

def main():
  bot_token = os.getenv('BOT_TOKEN')
  bot = telegram.Bot(token=bot_token)
  updater = Updater(token=bot_token, use_context = True)
  dispatcher = updater.dispatcher
  print('bot started')
  dispatcher.add_handler(CommandHandler("start", start, pass_args = True))
  dispatcher.add_handler(CommandHandler("translate", translate, pass_args = True))
  dispatcher.add_handler(CommandHandler("check", check_language, pass_args = True))
  dispatcher.add_handler(CommandHandler("lang", set_preferences, pass_args = True))
  dispatcher.add_handler(CommandHandler("checklang", check_lang, pass_args = True))
  dispatcher.add_handler(CommandHandler("help", unknown))

  # per language translator. TODO: make it better
  dispatcher.add_handler(CommandHandler("t", translate, pass_args = True))
  dispatcher.add_handler(CommandHandler("en", translate_en, pass_args = True))
  dispatcher.add_handler(CommandHandler("th", translate_th, pass_args = True))
  dispatcher.add_handler(CommandHandler("ru", translate_ru, pass_args = True))

  dispatcher.add_handler(MessageHandler(Filters.command, unknown))
  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()
