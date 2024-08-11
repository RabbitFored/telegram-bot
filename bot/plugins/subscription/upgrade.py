from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButtonBuy, InlineKeyboardMarkup, LabeledPrice

from bot import logger, strings
from bot.core import database as db
from bot.core.utils import generate_keyboard


@Client.on_message(filters.command(["premium", "subscribe"]))
async def premium(client, message):

    pre_text = strings.get("premium_txt")
    btn = strings.get("premium_btn")

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
        title="Subscribe | Monthly",
        description="Subscribe to mailable premium for a month",
        currency="XTR",
        prices=[LabeledPrice(label="Mailable Premium", amount=50)],
        start_parameter="start",
        reply_markup=(
            InlineKeyboardMarkup([[InlineKeyboardButtonBuy(text="Pay ⭐️50")]])
        ),
    )


@Client.on_message(filters.successful_payment)
async def successful_payment(client, message):
    user = await db.get_user(message.from_user.id)
    await user.upgrade("premium", message.successful_payment.telegram_payment_charge_id)
    await message.reply("**Thank you for purchasing premium!**")
    logger.info(f"User {user.ID} upgraded to premium")
