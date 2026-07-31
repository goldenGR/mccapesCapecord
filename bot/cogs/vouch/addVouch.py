import discord
from discord.ext import commands
from discord import app_commands
import datetime

from api.createVouchEmbed import createVouchEmbed
from api.vouch import submitVouch

class addVouch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(
        name="add-vouch",
        description="Add a new vouch",
    )

    @app_commands.checks.has_permissions(ban_members=True)
    async def addVouch(self, interaction: discord.Interaction, vouchee: discord.User, message: str, voucher: discord.User = None, verified: bool = False, is_unvouch: bool = False):
        await interaction.response.defer()
        try:
            client = self.bot

            if voucher is None:
                voucher = interaction.user
            voucher = voucher.id
            vouchee = vouchee.id

            result = submitVouch(voucher, vouchee, message, client.supabase, is_unvouch, verified)

            if result[1].data == []:
                await interaction.followup.send(f"Couldn't add vouch for {vouchee.display_name}", ephemeral=True)
                return
            
            embed = discord.Embed(
                title=f"Vouch Added Succesfully",
                description=f"Have fun admin-chan (˶>⩊<˶)",
                color=0x2ECC71,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed)

            vouchEmbed = createVouchEmbed(result[1].data[0], client)
            await interaction.followup.send(embed=vouchEmbed)

        except Exception as e:
            embed = discord.Embed(
                title="Error executing command!",
                description=f"An error occured while trying to execute this command! Please try again later\n Error: ```{e}```",
                color=0xF39C12,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text='\u200b',icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)

    @addVouch.error
    async def addVouch_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You cant add vouches pookie >.< Why u triyng",
                ephemeral=True
            )
        else:
            raise error  # Let discord.py handle unexpected errors
        

async def setup(bot):
    await bot.add_cog(addVouch(bot))
    