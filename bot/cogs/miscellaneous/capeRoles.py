import os

import discord
from discord.ext import commands
from discord import app_commands
import requests
import datetime

LOGINGCHANNEL = 1528767064356032533

capesRoles = {
    "2011":             1391249239664758836,
    "2012":             1391253576982204498,
    "2013":             1391253679465697361,
    "2015":             1391253679646179422,
    "2016":             1391253912945954976,
    "realms":           1402306795602710750,
    "mcexp":            1391254106005442742,
    "moonlighttrail":   1509547749551505430,
    "crafter":          1496964055963795708,
    "builder":          1510391668451578016,
    "mojangstudios":    1425854188734386237,
    "mojang":           1425853624000712754,
    "mojangold":        1425854345655746691,
    "mojira":           1425855021253132410
}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "API-Key": os.getenv("ANGELS_KEY")
}


class CapeRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="caperoles",
        description="Get yourself cape roles in the server!",
    )
    async def caperole(self, interaction: discord.Interaction, java_username: str):
        await interaction.response.defer(ephemeral=True)
        try:

            linkedResponse = requests.get(f"https://api.vlonk102.co.uk/linked?username={java_username}", headers=headers)
            linkedResponse = linkedResponse.json()["linked"]

            if linkedResponse == None:
                embed = discord.Embed(
                    title="Not discord found!",
                    description=f"It seems like this minecraft profile has no discord linked! \n Please link your discord by running ``,link`` in https://discord.com/channels/1378519415565320212/1385285209599250432! \n - If there is a mix up please open a ticket: https://discord.com/channels/1378519415565320212/1430045928060092456/1454906174766977065",
                    color=0xF39C12,
                    timestamp=datetime.datetime.now()
                )
                embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)

                await interaction.followup.send(embed=embed, ephemeral=True)

                return

            if linkedResponse != interaction.user.id:
                embed = discord.Embed(
                    title="Discord not matching with profile",
                    description=f"It seems like the username connected on this **Minecraft** profile isnt matching with your discord username! \n If there is a mix up please open a ticket: https://discord.com/channels/1378519415565320212/1430045928060092456/1454906174766977065",
                    color=0xF39C12,
                    timestamp=datetime.datetime.now()
                )
                embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed)

                return

            capesResponse = requests.get(f"https://api.vlonk102.co.uk/capes?username={java_username}", headers=headers)
            
            # THOSE NESTED IF STATEMENTS ARE KILLING ME :sob: GOTTA FIX TS :pray:
            # golden is handsome <3
            if capesResponse == None:
                embed = discord.Embed(
                    title="No minecraft profile found!",
                    description=f"It seems like there is not a minecraft profile with this username! \n Try rechecking if you enter the correct username! \n - If there is a mix up please open a ticket: https://discord.com/channels/1378519415565320212/1430045928060092456/1454906174766977065",
                    color=0xF39C12,
                    timestamp=datetime.datetime.now()
                )
                embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)

                return

            roles = []
            roles.append(interaction.guild.get_role(1531493585630007336))

            member = interaction.guild.get_member(interaction.user.id)
            for cape in capesResponse.json()["capes"]:
                if cape in capesRoles:
                    role = interaction.guild.get_role(capesRoles[cape])
                    roles.append(role)
                    
            roles = [r for r in roles if r is not None]
            await member.add_roles(*roles)


            embed = discord.Embed(
                title="Roles given succesfull",
                description=f"Enjoy your cape roles!",
                color=0x2ECC71,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)

            embed = discord.Embed(
                title="User used CapeRoles",
                description=f"{interaction.user.mention} has used the CapeRoles command! Username they used: {java_username}",
                color=0x2ECC71,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
            await self.bot.get_channel(LOGINGCHANNEL).send(embed=embed)
                    
        except Exception as e:
            embed = discord.Embed(
                title="Error executing command!",
                description=f"An error occured while trying to execute this command! Please try again later\n Error: ```{e}```",
                color=0xF39C12,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)
        

async def setup(bot):
    await bot.add_cog(CapeRoles(bot))