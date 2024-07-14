from pyrogram import Client, filters
from pyrogram.types import LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButtonBuy
from bot.core import database as db
from bot.core import filters as fltr
from bot.core.utils import generate_keyboard

@Client.on_message(filters.command(["premium", "subscribe"]))
async def premium(client, message):
  pre_text = '''
The bot offers a free limit to set 3 mails

**Need more?** Get a Premium subscription is for only 100stars/month

**The Premium subscription includes:**
__
 - Acquire upto 10 mail IDs.        
 - Set custom domains*
__ 
 
*domain not included
'''
  btn = "[Upgrade To Premium](data::cf_subscription.upgrade)"
  
  keyboard = generate_keyboard(btn)

  await message.reply_text(
      pre_text,
      disable_web_page_preview=True,
      reply_markup=keyboard,
      quote=True,
  )


@Client.on_message(filters.command(["upgrade"]))
async def upgrade(client, message):

  await client.send_invoice(
    message.chat.id,
    title="Premium",
    description="Subscribe to mailable premium for a month",
    currency="XTR",
    prices=[LabeledPrice(label="Mailable Premium", amount=100)],
    start_parameter="start",
    reply_markup=(InlineKeyboardMarkup(
      [[InlineKeyboardButtonBuy(text="Pay ⭐️100")]])))


@Client.on_message(filters.successful_payment)
async def successful_payment(client, message):
  db.user.upgrade(message.from_user.id, "premium")
  await message.reply("**Thank you for purchasing premium!**")
