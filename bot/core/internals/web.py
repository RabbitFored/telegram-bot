from quart import Quart, render_template
import os

# get the current working directory
current_working_directory = os.getcwd()


web = Quart(__name__, template_folder=f'{current_working_directory}/public')


@web.route('/')
async def index():
    return await render_template("index.html")