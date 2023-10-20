from database.database_path import DBPath
from sources.logger import CustomLogger, INFO, ERROR, WARNING
import sqlite3
from sqlite3 import Error
import discord
import time
from sources.infos import bot_picture, def_picture, clock_picture
import os
from datetime import datetime


logger = CustomLogger()
current_directory = os.path.dirname(__file__)
path = os.path.join(current_directory, "wb_storing.db")


def create_connection(path):
    conn = None
    cursor = None
    
    try:
        conn = sqlite3.connect(path)
        logger.log("Successfully connected to: " + path, level=INFO)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS WB (id INTEGER, lehrer TEXT, datum TEXT, content TEXT, notes TEXT, kw INTEGER, nr INTEGER, fach TEXT)")
        logger.log(f"The database was created successfully", level=INFO)

    except Error as e:
        logger.log(f"An error occurred in create_connection: {str(e)}", level=ERROR)

    return conn, cursor

def create_wb_entry(lehrer_name, datum, inhalt, note, kw, nr, fach):
    
    conn, cursor = create_connection(path)

    try:
        cursor.execute('SELECT MAX(id) FROM WB')
        last_id = cursor.fetchone()[0]
        if last_id is None:
            last_id = 0

        new_id = last_id + 1    
        logger.log("id catch was succsesfully")
    except Error as e:
        logger.log(f"An error occurred in the database id (create_wb_entry): {str(e)}", level=ERROR)


    try:
        cursor.execute(f"INSERT INTO WB VALUES ('{new_id}','{lehrer_name}', '{datum}', '{inhalt}', '{note}', '{kw}', '{nr}','{fach}')")
        conn.commit()
        logger.log("An entry was transferred to the database", level=INFO)

    except Error as e:
        logger.log(f"An error occurred in the database connection (create_wb_entry): {str(e)}", level=ERROR)

    finally:
        if conn:
            conn.close()


def select_kw_from_database(kw, nr):
    conn, cursor = create_connection(path)

    try:
        query = "SELECT * FROM WB ORDER BY kw DESC LIMIT 1;"
        cursor.execute(query)
        last_row = cursor.fetchone()
        database_kw = last_row[4]
        logger.log("The last entry, sorted by kw, was selected from the database", level=INFO)

        if kw != database_kw:
            logger.log("The variable 'nr' + 1 was returned from select_kw_from_database", level=INFO)
            return nr + 1
        else:
            logger.log("The variable 'nr' was returned from select_kw_from_database", level=INFO)
            return nr





    except Error as e:
        logger.log(f"An error occurred in select_kw_from_database: {str(e)}", level=ERROR)

    finally:
        if conn:
            conn.close()    


def database_search(kalenderwoche):
    try:
        conn, cursor = create_connection(path)
        query = f"SELECT * FROM WB WHERE KW = '{kalenderwoche}'"
        cursor.execute(query)
        logger.log("The variable 'date' is compared with all entries 'kw' in the database.",level=INFO)
        results = cursor.fetchall()
        embeds = []
        for result in results:
            embed = discord.Embed( title="**WOCHENBERICHT EINTRAG GEFUNDEN**", description="", color=discord.Color.pink())
            embed.set_thumbnail(url=bot_picture)
            embed.set_author(name="Developed by Bitflux_",icon_url=def_picture,url="https://discordapp.com/users/266266567157874700")
            embed.add_field(name="Name des Lehrers", value=result[1])
            date = format_date(result[2])
            embed.add_field(name="Datum", value=date)
            embed.add_field(name="Fach", value=result[7])
            embed.add_field(name="Was wurde gemacht?", value=result[3])
            embed.add_field(name="Extra Infos", value=result[4])
            embed.add_field(name="Kalenderwoche", value=result[5])
            embed.add_field(name="Nr", value=result[6])
            embed.add_field(name="ID", value=result[0])
            embed.set_footer(text= "Nachricht wurde versendet um: " +time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(time.time())) , icon_url=clock_picture)
            logger.log("A match was found", level=INFO)
            embeds.append(embed)
        if not results:
            embed = discord.Embed( title="**KALENDERWOCHE NICHT GEFUNDEN**", description="", color=discord.Color.red())
            embed.set_thumbnail(url=bot_picture)
            embed.set_author(name="Developed by Bitflux_",icon_url=def_picture,url="https://discordapp.com/users/266266567157874700")
            embed.add_field(name=f"**Es wurden keine Einträge mit der Kalenderwoche '{kalenderwoche}' gefunden.**", value="")
            embed.set_footer(text= "Nachricht wurde versendet um: " +time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(time.time())) , icon_url=clock_picture)
            logger.log("No match was found", level=WARNING)
            return [embed]
        return embeds
    except Error as e:
        logger.log(f"An error occurred in database_search {str(e)}", level=ERROR)

    finally:
        if conn:
            conn.close()



def database_view(anzahl):
    try:
        conn, cursor = create_connection(path)
        cursor.execute('SELECT * FROM WB ORDER BY id DESC LIMIT ?', (anzahl,))
        results = cursor.fetchall()
        embeds = []
        database_ids = []
        for result in results:
            embed = discord.Embed( title="**WOCHENBERICHT EINTRAG GEFUNDEN**", description="", color=discord.Color.pink())
            embed.set_thumbnail(url=bot_picture)
            embed.set_author(name="Developed by Bitflux_",icon_url=def_picture,url="https://discordapp.com/users/266266567157874700")
            embed.add_field(name="Name des Lehrers", value=result[1])
            date = format_date_dot(result[2])
            embed.add_field(name="Datum", value=date)
            embed.add_field(name="Fach", value=result[7])
            embed.add_field(name="Was wurde gemacht?", value=result[3])
            embed.add_field(name="Extra Infos", value=result[4])
            embed.add_field(name="Kalenderwoche", value=result[5])
            embed.add_field(name="Nr", value=result[6])
            embed.add_field(name="ID", value=result[0])
            logger.log("A match was found", level=INFO)
            embeds.append(embed)
            if os.path.exists('database_ids.txt'):
                os.remove('database_ids.txt')

            
            database_ids.append(result[0])
            with open('database_ids.txt', 'w') as f:
                for id in database_ids:
                    f.write(f'{id}\n')

        if not results:
            embed = discord.Embed( title="**Wochenbericht**", description="", color=discord.Color.red())
            embed.set_thumbnail(url=bot_picture)
            embed.set_author(name="Developed by Bitflux_",icon_url=def_picture,url="https://discordapp.com/users/266266567157874700")
            embed.add_field(name="**Es wurde kein Eintrag in der Datenbank gefunden, überprüfe bitte deine Eingabe.**", value="")
            logger.log("No match was found in the database", level=WARNING)
            return [embed]
        return embeds

    except Error as e:
        logger.log(f"An error occurred in database_view: {str(e)}", level=ERROR)

    finally:
        if conn:
            conn.close()



def database_delete_on_id(EntryID):
    try:
        conn, cursor = create_connection(path)
        cursor.execute(f"DELETE FROM WB WHERE id=?", (EntryID,))
        conn.commit()
        embed = discord.Embed( title="**WOCHENBERICHT EINTRAG GELÖSCHT**", description="", color=discord.Color.red())
        embed.set_thumbnail(url=bot_picture)
        embed.set_author(name="Developed by Bitflux_",icon_url=def_picture,url="https://discordapp.com/users/266266567157874700")
        embed.add_field(name=f"**Der Wochenbericht mit der ID {EntryID} wurde erfolgreich gelöscht!**", value="")
        logger.log(f"Entry with ID: {EntryID} was deleted.", level=WARNING)
        return embed

    except Error as e:
        logger.log(f"An error occurred in database_delete_on_id: {str(e)}", level=ERROR)

    finally:
        if conn:
            conn.close()


def format_date(date_str):
    try:
        day = date_str[:2]
        month = date_str[2:4]
        year = date_str[4:]
        formatted_date = f"{day}.{month}.{year}"
        return formatted_date
    except Exception as e:
        logger.log(f"An error occurred in format_date: {str(e)}", level=ERROR)


def format_date_dot(date_string: str) -> str:
    try:
        if date_string != "None":
            if len(date_string) == 6:
                my_date = datetime.strptime(date_string, '%d%m%Y')
                formatted_date = my_date.strftime('%#d.%#m.%Y')
                return formatted_date
            else:
                my_date = datetime.strptime(date_string, '%d%m%Y')
                formatted_date = my_date.strftime('%#d.%#m.%Y')
                return formatted_date
        else:
            return date_string  
    except Exception as e:
        logger.log(f"An error occurred in format_date_dot: {str(e)}", level=ERROR)



def get_kw_data(week: int):
    conn, cursor = create_connection(path)
    query = "SELECT lehrer, datum, kw FROM WB WHERE kw = ?"
    cursor.execute(query, (week,))
    results = cursor.fetchall()
    conn.close()
    return results        