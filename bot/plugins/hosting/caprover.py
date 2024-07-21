from caprover_api import caprover_api
import os
from pyrogram import Client, filters
from bot.core import filters as fltr

cap = caprover_api.CaproverAPI(
    dashboard_url= os.environ['cap_url'],
    password= os.environ['cap_password']
)

def redeploy_app_via_api(app_name):
    cap.deploy_app(app_name)
    print(f"App {app_name} redeployed successfully.")

# Usage


@Client.on_message(filters.command("deploy") & fltr.group("admin"))
async def set_log_level(client, message):
    print("redeploying")
    redeploy_app_via_api(os.environ['cap_app_name'])

