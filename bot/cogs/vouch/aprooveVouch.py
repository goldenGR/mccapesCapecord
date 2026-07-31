import discord
from discord.ext import commands
from discord import app_commands
from api.approveVouch import approveVouchById
import datetime
from cogs.groups import admin_group

class approveVouch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(
        name="approve-vouch",
        description="Approove/dissaproove a vouch by id",
    )

    @app_commands.checks.has_permissions(ban_members=True)
    async def approveVouch(self, interaction: discord.Interaction, id: int, aproove: bool = True):
        await interaction.response.defer()
        try:

            client = self.bot
            result = approveVouchById(id, client.supabase, aproove=aproove)

            if result[1].data == []:
                await interaction.followup.send("Couldn't find/approve a vouch with that ID.", ephemeral=True)
                return
            
            approved_text = "Approved" if aproove else "Dis-Approved"
            
            embed = discord.Embed(
                title=f"Vouch {approved_text} Succesfully",
                description=f"Dk what to say here have fun admin <3",
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
    
    @approveVouch.error
    async def approveVouch_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You cant approve/disapprove vouches pookie :< >.<",
                ephemeral=True
            )
        else:
            raise error  # Let discord.py handle unexpected errors

async def setup(bot):
    await bot.add_cog(approveVouch(bot))
    