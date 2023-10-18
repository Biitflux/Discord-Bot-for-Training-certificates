import discord
from discord.ext import commands
from discord import app_commands
import time
from sources import infos
from sources.logger import CustomLogger, WARNING, INFO, ERROR
import subprocess
import os

logger = CustomLogger()

class Shutdown(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="shutdown", description="Shuts down the Bot")
    async def shutdown_command(self, interaction: discord.Interaction):
        try:
            user_name = interaction.user.name
            embed = close_embed(user_name) 
            await interaction.response.send_message(embed=embed)
            logger.log(f"Shutdown Command was registered by {user_name}", level=INFO)

            await self.client.close()
            
            current_script_path = os.path.abspath(__file__)
            current_directory = os.path.dirname(current_script_path)
            logger.log("The shutdown is executed", level=WARNING)
            stop_script_path = os.path.join(current_directory, "..", "stop.sh")

            subprocess.call([stop_script_path], shell=True) 

            
        except discord.DiscordException as e:
            logger.log(f"An error occurred during shutdown: {str(e)}", level=ERROR)

async def setup(client: commands.Bot):
    await client.add_cog(Shutdown(client))

def close_embed(user_name):
    embed = discord.Embed(
        title="**BOT INFORMATION**",
        description="",
        color=discord.Color.red()
    )

    embed.set_thumbnail(url=infos.bot_picture)
    embed.add_field(name=f"**Der Bot wird heruntergefahren von {user_name}!**", value="", inline=False)

    embed.set_author(
        name="Developed by Bitflux_",
        icon_url=infos.def_picture,
        url="https://discordapp.com/users/266266567157874700"
    )

    embed.set_footer(text=time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(time.time())), icon_url=infos.clock_picture)
    return embed
