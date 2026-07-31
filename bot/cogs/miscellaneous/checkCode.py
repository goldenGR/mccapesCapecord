import discord
from discord.ext import commands
from discord import app_commands

async def verifyCode(code):
    pass


class CheckCode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="checkcode",
        description="Verify a code through discord!",
    )
    async def checkcode(self, interaction: discord.Interaction, code: str):
        await interaction.response.defer()

        await verifyCode(code)
        await interaction.followup.send("Checked code!")

async def setup(bot):
    await bot.add_cog(CheckCode(bot))