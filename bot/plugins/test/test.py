from pyrogram import Client, filters
from bot.core import database as db
from bot.core.translation import Translator
from bot.core.utils import generate_keyboard
from bot import logger, CONFIG
from bot.core.utils import generate_keyboard, gen_rand_string
from datetime import datetime, timedelta
import time
from bot.core.database import MongoDB
'''
def read_and_modify_one_block_of_yaml_data(filename, key, value):
    with open(f'{filename}.yaml', 'r') as f:
        data = yaml.safe_load(f)
        data[f'{key}'] = f'{value}' 
        print(data) 
    with open(f'{filename}.yaml', 'w') as file:
      yaml.dump(data,file,sort_keys=False)
    print('done!')
    
@Client.on_message(filters.command(["test1"]))
async def test1(client, message):
    test_file = open("test.yaml", "r")
    t = yaml.safe_load(test_file)
    read_and_modify_one_block_of_yaml_data('test', key='Age', value=30)

    text = t

    await message.reply_text(text)


async def test_task(client, message):
    while True:
        await client.send_message(chat_id=message.chat.id, text="Test message")
        await asyncio.sleep(10) 
        
@Client.on_message(filters.command(["testc"]))
async def testc(client, message):
    process = ProcessManager.create_process("testc")
    await process.start(test_task(client, message))
    #await message.reply_text(text)
@Client.on_message(filters.command(["stop"]))
async def stop(client, message):
    process = ProcessManager.get_process(2)
    await process.stop()
    
@Client.on_message(filters.command(["test"]))
async def test(client, message):
    logger.info(message)
    processes = ProcessManager.list_processes()
    response = "Running processes:\n" + "\n".join([f"{p.process_id}: {p.name}" for p in processes])
    await message.reply(response)
    '''

@Client.on_message(filters.command(["test"]))
async def test(client, message):
    user = await db.get_user(message.from_user.id)
    await user.data.set({"jjdk": "kkf1"})
    await message.reply(f"t {str((await db.list_database()))}")
    
@Client.on_message(filters.command(["test2"]))
async def test2(client, message):
    user_language = "en"
    strings = Translator(lang=user_language)
    greeting_message = strings.get("greeting")
    btn = strings.get("start_btn")
    await message.reply(greeting_message, reply_markup=generate_keyboard(btn))