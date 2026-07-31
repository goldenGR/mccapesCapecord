import discord
from discord.ext import commands
from discord import app_commands
from api.createVouchEmbed import createVouchEmbed
from api.getVouch import getVoucheByID
import datetime

class getVouch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="get-vouch",
        description="Inquire a vouch by id!",
    )
    async def caperole(self, interaction: discord.Interaction, id: int):
        await interaction.response.defer()
        try:
            client = self.bot
            vouch = getVoucheByID(id, client.supabase)

            if vouch[1].data == []:
                embed = discord.Embed(
                    title="Vouch not found!",
                    description=f"Vouch with ID {id} was not found in the database.",
                    color=0xF39C12,
                    timestamp=datetime.datetime.now()
                )
                embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)
                return 
            
            vouch = vouch[1].data[0]
            
            await interaction.followup.send(
                embed=createVouchEmbed(vouch, client)
            )

            return

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
    await bot.add_cog(getVouch(bot))