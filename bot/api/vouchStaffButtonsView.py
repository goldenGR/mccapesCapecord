from __future__ import annotations

import asyncio
import logging
import re

import discord

from api.approveVouch import approveVouchById
from api.deleteVouch import deleteVouchById
from api.getVouch import getVoucheByID

log = logging.getLogger(__name__)

async def dm_user(interaction: discord.Interaction, user_id: int, text: str) -> bool:
    """Try to DM a user. Returns True on success, False if it couldn't be sent."""
    try:
        user = interaction.guild.get_member(user_id) if interaction.guild else None
        user = user or await interaction.client.fetch_user(user_id)
        await user.send(text)
        return True
    except (discord.Forbidden, discord.NotFound, discord.HTTPException):
        return False


def vouchStaffButtonsView(
    vouch_id: int,
    supabase,
    *,
    approve_disabled: bool = False,
    delete_disabled: bool = False,
) -> discord.ui.View:
    view = discord.ui.View(timeout=None)
    view.add_item(ApproveVouchButton(vouch_id, supabase, disabled=approve_disabled))
    view.add_item(DeleteVouchButton(vouch_id, supabase, disabled=delete_disabled))
    return view

class DeleteVouchModal(discord.ui.Modal, title="Delete Vouch"):
    reason = discord.ui.TextInput(
        label="Reason for deletion",
        style=discord.TextStyle.paragraph,
        placeholder="Why are you deleting this vouch?",
        required=True,
        max_length=300,
    )

    def __init__(self, vouch_id: int, supabase, message: discord.Message):
        super().__init__()
        self.vouch_id = vouch_id
        self.supabase = supabase
        self.message = message

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Fetch the vouch (blocking call -> thread)
        ok, result = await asyncio.to_thread(getVoucheByID, self.vouch_id, self.supabase)
        if not ok or not result.data:
            await interaction.followup.send(f"Couldn't fetch vouch: {result}", ephemeral=True)
            return

        vouch = result.data[0]
        vouchee_id = int(vouch["vouchee"])
        voucher_id = int(vouch["voucher"])
        staff = interaction.user.mention
        reason = self.reason.value

        # Notify both parties; a failed DM must never block the deletion
        sent_vouchee, sent_voucher = await asyncio.gather(
            dm_user(
                interaction, vouchee_id,
                f"A vouch you received from <@{voucher_id}> has been deleted by {staff}. Reason: {reason}",
            ),
            dm_user(
                interaction, voucher_id,
                f"Your vouch for <@{vouchee_id}> has been deleted by {staff}. Reason: {reason}",
            ),
        )

        await asyncio.to_thread(deleteVouchById, self.vouch_id, self.supabase)

        # Disable all buttons on the original staff message
        await self.message.edit(
            view=vouchStaffButtonsView(
                self.vouch_id, self.supabase, approve_disabled=True, delete_disabled=True
            )
        )

        msg = f"Vouch has been deleted. Reason: {reason}\nGood job admin >.<"
        if not (sent_vouchee and sent_voucher):
            msg += "\n(Couldn't DM one or both users.)"
        await interaction.followup.send(msg, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        log.exception("DeleteVouchModal failed", exc_info=error)
        send = interaction.followup.send if interaction.response.is_done() else interaction.response.send_message
        await send("Something went wrong.", ephemeral=True)

class ApproveVouchButton(
    discord.ui.DynamicItem[discord.ui.Button],
    template=r"vouch_approve:(?P<id>\d+)",
):
    def __init__(self, vouch_id: int, supabase, *, disabled: bool = False):
        self.vouch_id = vouch_id
        self.supabase = supabase
        super().__init__(
            discord.ui.Button(
                label="Approve Vouch",
                style=discord.ButtonStyle.blurple,
                emoji="✅",
                custom_id=f"vouch_approve:{vouch_id}",
                disabled=disabled,
            )
        )

    @classmethod
    async def from_custom_id(cls, interaction: discord.Interaction, item, match: re.Match, /):
        return cls(int(match["id"]), interaction.client.supabase)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await asyncio.to_thread(approveVouchById, self.vouch_id, self.supabase)

        await interaction.edit_original_response(
            view=vouchStaffButtonsView(self.vouch_id, self.supabase, approve_disabled=True)
        )
        await interaction.followup.send(
            "Voucher has been approved. Gn pookie admin <3", ephemeral=True
        )


class DeleteVouchButton(
    discord.ui.DynamicItem[discord.ui.Button],
    template=r"vouch_delete:(?P<id>\d+)",
):
    def __init__(self, vouch_id: int, supabase, *, disabled: bool = False):
        self.vouch_id = vouch_id
        self.supabase = supabase
        super().__init__(
            discord.ui.Button(
                label="Delete Vouch",
                style=discord.ButtonStyle.gray,
                emoji="❌",
                custom_id=f"vouch_delete:{vouch_id}",
                disabled=disabled,
            )
        )

    @classmethod
    async def from_custom_id(cls, interaction: discord.Interaction, item, match: re.Match, /):
        return cls(int(match["id"]), interaction.client.supabase)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            DeleteVouchModal(self.vouch_id, self.supabase, interaction.message)
        )