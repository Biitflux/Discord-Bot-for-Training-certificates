import discord
from discord.ext import commands
from discord import app_commands
import time
from sources import infos
from sources.logger import CustomLogger, INFO, ERROR

logger = CustomLogger()

class info(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="info", description="View informations.")
  async def info(self, interaction: discord.Interaction):
    try:
      embed = BotInformation()
      await interaction.response.send_message(embed=embed, ephemeral=True)
      logger.log("The info message was sent successfully", level=INFO)
    except discord.DiscordException as e:
        logger.log(f"An error occurred while sending the info message: {str(e)}", level=ERROR)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(info(client))


def BotInformation():    
    embed = discord.Embed(
        title="**Informations**",
        description="",
        color=discord.Color.yellow()
    )

    embed.set_thumbnail(url=infos.bot_picture)
    embed.add_field(name="", value="**Bot-Version: **" + infos.bot_version , inline=False)
    embed.add_field(name="", value="**Python-Version: **" + infos.python_version , inline=False)
    embed.add_field(name="", value="**Discord-Version: **" + infos.discord_version , inline=False)
    embed.add_field(name="", value="**Du brauchst mehr Hilfe? **" + "\nSende mir eine Nachricht: Bitflux_" , inline=False)
    embed.set_author(
        name="Developed by Bitflux_",
        icon_url=infos.def_picture,
        url="https://discordapp.com/users/266266567157874700"
    )

    embed.set_footer(text= time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(time.time())) , icon_url=infos.clock_picture)
    return embed  