import discord
from discord.ext import commands
from discord import app_commands
from database.database import database_view
from sources.logger import CustomLogger, INFO, ERROR

logger = CustomLogger()

class WBView(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="wb_view", description="Zeige dir die letzten X Einträge an.")
  async def WBView_command(self, interaction: discord.Interaction, anzahl: int):
    try:
        views = database_view(anzahl)
        await interaction.response.send_message(embeds=views, ephemeral=True)
        logger.log("Entrys message was sent successfully", level=INFO)
    except Exception as e:
        logger.log(f"An error occurred in database_view: {str(e)}", level=ERROR)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(WBView(client))






    




