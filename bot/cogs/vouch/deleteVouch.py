import discord
from discord.ext import commands
from discord import app_commands
from api.deleteVouch import deleteVouchById
import datetime
# from cogs.groups import admin_group

class deleteVouch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(
        name="delete-vouch",
        description="Delete a vouch by id",
    )

    @app_commands.checks.has_permissions(ban_members=True)
    async def deleteVouch(self, interaction: discord.Interaction, id: int):
        await interaction.response.defer()
        try:

            client = self.bot
            result = deleteVouchById(id, client.supabase,)

            if result[1].data == []:
                await interaction.followup.send(f"Couldn't delete vouch with ID of {id}", ephemeral=True)
                return
            
            embed = discord.Embed(
                title=f"Vouch Deleted Succesfully",
                description=f"Goodnight pookie admin <3",
                color=0x2ECC71,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Error executing command!",
                description=f"An error occured while trying to execute this command! Please try again later\n Error: ```{e}```",
                color=0xF39C12,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)

    @deleteVouch.error
    async def deleteVouch_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You cant delete vouches pookie :< >.<",
                ephemeral=True
            )
        else:
            raise error  # Let discord.py handle unexpected errors
        

async def setup(bot):
    await bot.add_cog(deleteVouch(bot))
    