import discord
from discord.ext import commands
from discord import app_commands
from sources.logger import CustomLogger, INFO, ERROR
import datetime
from database.database import select_kw_from_database, create_wb_entry
from sources.infos import bot_picture, def_picture


logger = CustomLogger()


class WBNewEntry(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="wb_new_entry", description="Erstelle einen neuen Wochenbericht")
  async def WBNewEntry_command(self, interaction: discord.Interaction):
    try:
        await interaction.response.send_modal(WBNewEntryModal(title="Wochenbericht erstellen"))
        logger.log("WBCreateModal was succesfully", level=INFO)
    except Exception as e:
        logger.log(f"An error occurred in WBNewEntry_command: {str(e)}", level=ERROR)
    

async def setup(client:commands.Bot) -> None:
  await client.add_cog(WBNewEntry(client))





class WBNewEntryModal(discord.ui.Modal):

    try:  
      def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.lehrer_name = self.add_item(discord.ui.TextInput(label="Name des Lehrers", placeholder="z.B. Herr Schmid", required=True, max_length=100, style=discord.TextStyle.short))
        self.datum = self.add_item(discord.ui.TextInput(label="Datum", placeholder="z.B. 23.08.2023", required=True, max_length=100, style=discord.TextStyle.short))
        self.fach = self.add_item(discord.ui.TextInput(label="Fach", placeholder="z.B. SAE-Berufsschule", required=True, max_length=100, style=discord.TextStyle.short))
        self.inhalt = self.add_item(discord.ui.TextInput(label="Was wurde gemacht?", placeholder="z.B. Wir haben Tetris gespielt", required=True, max_length=2000, style=discord.TextStyle.long))
        self.info = self.add_item(discord.ui.TextInput(label="Extra Infos ", placeholder="z.B. Herr Schmid war nicht da, hatte aber eine Aufgabe", required=False, max_length=2000, style=discord.TextStyle.long))


      async def on_submit(self, interaction: discord.Interaction):
        currend_date = datetime.datetime.now()
        kw = currend_date.isocalendar()[1]
        nr = kw + 14
        new_nr = select_kw_from_database(kw, nr)
        
        datum_value = self.children[1].value.replace(".", "")

        if self.children[4].value == '':
          info = "None"
          create_wb_entry(self.children[0].value, datum_value, self.children[3].value, info, kw, new_nr,self.children[2].value)
          message = WBNewEntryEmbed()
          await interaction.response.send_message(embed=message, ephemeral=True)

        else:
          message = WBNewEntryEmbed()
          create_wb_entry(self.children[0].value, datum_value, self.children[3].value, self.children[4].value, kw, new_nr, self.children[2].value)
          await interaction.response.send_message(embed=message, ephemeral=True)
            
    except discord.DiscordException as e:
        logger.log(f"An error occurred in WBNewEntryModal: {str(e)}", level=ERROR)
        
     

def WBNewEntryEmbed():
  embed = discord.Embed( title="**WOCHENBERICHT EINTRAG**", description="", color=discord.Color.green())
  embed.set_thumbnail(url=bot_picture)
  embed.set_author(name="Developed by Bitflux_",icon_url=def_picture,url="https://discordapp.com/users/266266567157874700")
  embed.add_field(name="Der Eintrag wurde erfolgreich der Datenbank übergeben.", value="")
  return embed

