import discord
from discord.ext import commands
from discord import app_commands
from sources import infos
import time

class cog3(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="cog3", description="Sends hello!")
  async def cog3(self, interaction: discord.Interaction):
    await interaction.response.send_message(content="Hello!")

async def setup(client:commands.Bot) -> None:
  await client.add_cog(cog3(client))













def restart_embed(user_name):
    embed = discord.Embed(
        title="**BOT INFORMATION**",
        description="",
        color=discord.Color.red()
    )

    embed.set_thumbnail(url=infos.bot_picture)
    embed.add_field(name="Mitteilung", value=f"**Der Bot wird neugestartet von {user_name}!**", inline=False)


    embed.set_author(
        name="Developed by Bitflux_",
        icon_url=infos.def_picture,
        url="https://discordapp.com/users/266266567157874700"
    )

    embed.set_footer(text=time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(time.time())), icon_url=infos.clock_picture)
    return embed  