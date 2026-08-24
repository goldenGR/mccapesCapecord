import discord
from discord.ext import commands
from discord import app_commands
from api.deleteVouch import deleteVouchById
import datetime
import api.vouch

class removeCooldown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(
        name="remove-cooldown",
        description="Remove a users vouch cooldown (30mins)",
    )

    @app_commands.checks.has_permissions(ban_members=True)
    async def removeCooldownCommand(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()
        try:

            api.vouch.whoVouchedWhoWhen = {k: v for k, v in api.vouch.whoVouchedWhoWhen.items() if k[0] != user.id}

            embed = discord.Embed(
                title=f"Removed cooldown succesfully for <@{user.id}>",
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

    @removeCooldownCommand.error
    async def deleteVouch_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You cant remove the cooldown honey pie >.<",
                ephemeral=True
            )
        else:
            raise error
        

async def setup(bot):
    await bot.add_cog(removeCooldown(bot))
    