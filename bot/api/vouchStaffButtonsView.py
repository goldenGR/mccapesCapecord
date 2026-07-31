import discord

from api.approveVouch import approveVouchById
from api.deleteVouch import deleteVouchById


class vouchStaffButtonsView(discord.ui.View):
    def __init__(self, vouchId, supabase):
        super().__init__(timeout=300)
        self.vouchId = vouchId
        self.supabase = supabase

    @discord.ui.button(
        label="Approve Vouch",
        style=discord.ButtonStyle.blurple,
        emoji="✅"
    )
    async def approveVouch(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        
        approveVouchById(self.vouchId, self.supabase)

        button.disabled = True

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
        "Voucher has been approved. Gn pookie admin <3",
        ephemeral=True
    )


    @discord.ui.button(
        label="Delete Vouch",
        style=discord.ButtonStyle.gray,
        emoji="❌"
    )
    async def deleteVouch(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        
        deleteVouchById(self.vouchId, self.supabase)

        button.disabled = True
        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            "Voucher has been deleted. Good job admin >.<",
            ephemeral=True
        )
        