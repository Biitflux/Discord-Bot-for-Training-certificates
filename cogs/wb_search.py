import discord
from discord.ext import commands
from discord import app_commands
from database.database import database_search
from sources.logger import CustomLogger, INFO,ERROR

logger = CustomLogger()


class WBSearch(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="wb_search", description="Gebe dir die Einträge für die ganze KW aus")
  async def wbsearch_command(self, interaction: discord.Interaction, kalenderwoche: str):
    try:
      logger.log("Database is searched", level=INFO)
      search = database_search(kalenderwoche)

      await interaction.response.send_message(embeds=search, ephemeral=True)
      logger.log("Search message was sent successfully", level=INFO)

    except discord.DiscordException as e:
        logger.log(f"An error occurred in wbsearch_command: {str(e)}", level=ERROR)   

   
async def setup(client:commands.Bot) -> None:
  await client.add_cog(WBSearch(client))