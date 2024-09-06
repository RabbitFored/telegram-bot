from ..shared import CONFIG
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient

if bool(CONFIG.settings["pyrogram"].get("use_mongodb_for_session", False)):
    mongo_session = dict(connection=AsyncIOMotorClient(CONFIG.mongouri),
                         remove_peers=False)
else:
    mongo_session = None

if CONFIG.settings["pyrogram"].get("client_name", None):
    client_name = CONFIG.settings["pyrogram"]["client_name"]
else:
    client_name = CONFIG.settings.get("app_name", "bot")
    
bot = Client(
    client_name,
    api_id=CONFIG.apiID,
    api_hash=CONFIG.apiHASH,
    bot_token=CONFIG.botTOKEN,
    session_string=CONFIG.session_string,
    plugins=dict(
        root=CONFIG.settings.get('plugins', {}).get("dir", "bot/plugins"),
        exclude=CONFIG.settings.get('plugins', {}).get("exclude", []),
    )
    
    
    ,
    alt_port=bool(CONFIG.settings.get('pyrogram').get("alt_port", False)),
    test_mode=bool(CONFIG.settings.get('pyrogram').get("test_mode", False)),
    in_memory=bool(
        CONFIG.settings.get('pyrogram').get("in_memory_session", False)),
    ipv6=bool(CONFIG.settings.get('pyrogram').get("use_ipv6", False)),
    mongodb=mongo_session,
    proxy=CONFIG.settings.get('pyrogram').get("proxy", {}))
