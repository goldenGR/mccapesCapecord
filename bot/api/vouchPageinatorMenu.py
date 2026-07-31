import math

import discord
from api.createVouchSelectorEmbed import createVouchSelectorEmbed
from api.vouchMenu import VouchView

def get_vouches_page(vouches: list, page: int, per_page: int = 25):
    if page < 1:
        raise ValueError("Page must be at least 1.")

    start = (page - 1) * per_page
    end = start + per_page

    return vouches[start:end]

class VouchPageinatorSelect(discord.ui.Select):
    def __init__(self, vouchData, bot):
        self.vouchData = vouchData
        self.bot = bot
        print(self.vouchData)
        options = []

        vouches_per_page = 25
        total_pages = math.ceil(len(self.vouchData) / vouches_per_page)

        options = []

        for page in range(1, total_pages + 1):
            start = (page - 1) * vouches_per_page + 1
            end = min(page * vouches_per_page, len(self.vouchData))

            options.append(
                discord.SelectOption(
                    label=f"Page #{page}",
                    description=f"Vouches {start}-{end}"
                )
            )

        super().__init__(
            placeholder="Select a vouch page...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        page_id = int(self.values[0].replace("Page #", ""))

        await interaction.response.send_message(
            embed=createVouchSelectorEmbed(self.vouchData, self.bot, page_id),
            view=VouchView(get_vouches_page(self.vouchData, page_id), self.bot),
            ephemeral=True
        )

class VouchPageinatorView(discord.ui.View):
    def __init__(self, vouchData, bot):
        super().__init__(timeout=300)

        self.add_item(
            VouchPageinatorSelect(vouchData, bot)
        )