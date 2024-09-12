from . import bot, CONFIG, logger



if __name__ == "__main__":
    if True:
        from . import web
        logger.info("Starting web client and bot")
        bot.start()
        
        #set self
        CONFIG.me = bot.get_me()

        web.run("0.0.0.0", CONFIG.port, loop=bot.loop)
    else:
        logger.info("Starting bot")
        bot.run()
