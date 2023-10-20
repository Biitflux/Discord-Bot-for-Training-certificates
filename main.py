import discord
from discord.ext import commands
from sources.logger import CustomLogger, INFO, ERROR
from sources.infos import BOT_TOKEN

from sources.infos import bot_version, bot_developer, discord_version, python_version, sqlite_version

logger = CustomLogger()

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=discord.Intents.all())

        self.cogslist = ["cogs.info", 
                         "cogs.shutdown",
                         "cogs.restart", 
                         "cogs.wb_new_entry", 
                         "cogs.wb_search", 
                         "cogs.wb_view",
                         "cogs.wb_delete", 
                         #"cogs.wb_create_doc",
                         "cogs.channel_message"]

    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)

    async def on_ready(self):
        try:

            messages = [
                "Logged in as " + self.user.name, 
                "Bot ID " + str(self.user.id),
                "Discord Version " + discord_version,
                "Python Version " + python_version,
                "SQLite3 Version: " + sqlite_version,
                "Bot Version: " + bot_version,
                "Entwickler: " + bot_developer
                ]

            for message in messages:   
                logger.log(message, level=INFO)


            game = discord.Game("SRH durch :)")
            await self.change_presence(activity=game)

            synced = await self.tree.sync()
            logger.log(f"Slash CMDs Synced {str(len(synced))} Commands", level=INFO)
            
            
        except discord.DiscordException as e:
            logger.log(f"An error occurred during startup: {str(e)}", level=ERROR)


def main():
    try:
        client = Client()
        client.run(BOT_TOKEN)
        
    except discord.DiscordException as e:
        logger.log(f"An error occurred during startup: {str(e)}", level=ERROR)

if __name__ == "__main__":
    main()
