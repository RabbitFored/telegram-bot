from pyrogram import Client, filters
from bot.core import filters as fltr

@Client.on_message(filters.command(["refund"]) & fltr.group("admin"))
async def refund(client, message):
  args = message.text.split(" ")
  user_id = args[1]
  charge_id = args[2]
  r = await client.refund_star_payment(user_id=user_id,
                                       telegram_payment_charge_id=charge_id)
  if r:
    await message.reply("success")
