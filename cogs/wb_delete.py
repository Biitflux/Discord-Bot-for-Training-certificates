import discord
from discord.ext import commands
from discord import app_commands
from database.database import database_delete_on_id
from sources.logger import CustomLogger, INFO, ERROR
logger = CustomLogger()

class WBDelete(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="wb_delete", description="Lösche einen Eintrag anhand seiner ID")
  async def WBDelete_command(self, interaction: discord.Interaction, entryid: int):
    delete_sucsess = database_delete_on_id(entryid)
    await interaction.response.send_message(embed=delete_sucsess,ephemeral=True)
    logger.log("Deleting the entry was successful", level=INFO)
 

async def setup(client:commands.Bot) -> None:
  await client.add_cog(WBDelete(client))