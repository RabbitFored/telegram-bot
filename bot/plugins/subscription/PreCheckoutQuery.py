from pyrogram import Client


@Client.on_pre_checkout_query()
async def PreCheckoutQuery(client, PreCheckoutQuery):
    await PreCheckoutQuery.answer(success=True)
