import discord
from discord.ext import commands
from discord import app_commands
from sources.logger import CustomLogger, INFO, WARNING, ERROR
from sources.infos import def_picture, bot_picture

logger = CustomLogger()


class ChannelMessage(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="channel_message", description="Sende die Command Nachricht")
  async def ChannelMessage(self, interaction: discord.Interaction):
    if interaction.user.id == 266266567157874700:
      await interaction.response.send_message(embed=embed_message)
    else:
      await interaction.response.send_message(embed=embed_no_permmision, ephemeral=True)


embed_no_permmision = discord.Embed( title="**Information zu den Commands**", description="", color=discord.Color.red())
embed_no_permmision.set_thumbnail(url=bot_picture)
embed_no_permmision.set_author(name="Developed by Bitflux_",icon_url=def_picture,url="https://discordapp.com/users/266266567157874700")
embed_no_permmision.add_field(name=f"**Dazu hast du keine Berechtigung!**", value="")
logger.log(f"Someone try to use /channel_message Command", level=WARNING)


embed_message = discord.Embed( title="**Information**", description="", color=discord.Color.orange())
embed_message.set_thumbnail(url=bot_picture)
embed_message.set_author(name="Developed by Bitflux_",icon_url=def_picture,url="https://discordapp.com/users/266266567157874700")
embed_message.add_field(name="**/help**", value="Zeigt dir wichtige Informationen an.")
embed_message.add_field(name="**/wb_new_entry**", value="Hiermit kannst du einen Eintrag erstellen.")
embed_message.add_field(name="**/wb_view**", value="Gebe die Anzahl an, an letzen Einträgen du sehen willst")
embed_message.add_field(name="**/wb_search**", value="Suche einen Eintrag nach einem Datum")
embed_message.add_field(name="**/restart**", value="Startet den Bot neu.")
embed_message.add_field(name="**/shutdown**", value="Stop den Bot.")
embed_message.add_field(name="**/wb_create_doc**", value="Aktuell noch in Arbeit!")
logger.log(f"The Command was succsesfully", level=INFO)


async def setup(client:commands.Bot) -> None:
  await client.add_cog(ChannelMessage(client))