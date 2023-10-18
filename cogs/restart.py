import discord
from discord.ext import commands
from discord import app_commands
import time
from sources import infos
from sources.logger import CustomLogger, INFO, WARNING, ERROR
import subprocess
import os

logger = CustomLogger()

class Restart(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="restart", description="Restarts the Bot")
    async def restart_command(self, interaction: discord.Interaction):
        try:
            user_name = interaction.user.name
            embed = restart_embed(user_name) 

            await interaction.response.send_message(embed=embed)
            logger.log(f"Restart Command was registered by {user_name}", level=INFO)

            current_script_path = os.path.abspath(__file__)
            current_directory = os.path.dirname(current_script_path)
            stop_script_path = os.path.join(current_directory, "..", "stop.sh")
            

            start_scipt_path = os.path.join(current_directory,"..", "start.sh")
            logger.log("The restart is executed", level=WARNING)
            subprocess.call([start_scipt_path])
            subprocess.call([stop_script_path])  
        except Exception as e:
            logger.log(f"An error occurred during restart: {str(e)}", level=ERROR)

async def setup(client: commands.Bot):
    await client.add_cog(Restart(client))

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
