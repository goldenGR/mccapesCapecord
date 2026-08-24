import asyncio
import discord

from api.approveVouch import approveVouchById
from api.deleteVouch import deleteVouchById


class vouchStaffButtonsView(discord.ui.View):
    def __init__(self, vouchId, supabase):
        super().__init__(timeout=None)
        self.vouchId = vouchId
        self.supabase = supabase

    @discord.ui.button(
        label="Approve Vouch",
        style=discord.ButtonStyle.blurple,
        emoji="✅",
        custom_id="vouch_approve"
    )
    async def approveVouch(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        # Acknowledge immediately, well within the 3s window
        await interaction.response.defer()

        # Run the blocking Supabase call off the event loop
        await asyncio.to_thread(approveVouchById, self.vouchId, self.supabase)

        button.disabled = True
        await interaction.edit_original_response(view=self)

        await interaction.followup.send(
            "Voucher has been approved. Gn pookie admin <3",
            ephemeral=True
        )

    @discord.ui.button(
        label="Delete Vouch",
        style=discord.ButtonStyle.gray,
        emoji="❌",
        custom_id="vouch_delete"
    )
    async def deleteVouch(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.defer()

        await asyncio.to_thread(deleteVouchById, self.vouchId, self.supabase)

        button.disabled = True
        await interaction.edit_original_response(view=self)

        await interaction.followup.send(
            "Vouch has been deleted. Good job admin >.<",
            ephemeral=True
        )