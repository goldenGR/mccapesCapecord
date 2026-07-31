import discord
from api.createVouchEmbed import createVouchEmbed

class VouchSelect(discord.ui.Select):
    def __init__(self, vouchData, bot):
        self.vouchData = vouchData
        self.bot = bot
        print(self.vouchData)
        options = []

        for vouch in self.vouchData[:24]:  # Discord limit
            options.append(
                discord.SelectOption(
                    label=f"#{vouch['id']}",
                    description=f"Voucher: {vouch['voucher']}"
                )
            )

        super().__init__(
            placeholder="Select a vouch...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_id = int(self.values[0].replace("#", ""))

        vouch = next(
            (v for v in self.vouchData if v["id"] == selected_id),
            None
        )

        if not vouch:
            await interaction.response.send_message(
                "Vouch not found.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            embed=createVouchEmbed(vouch, self.bot),
            ephemeral=True
        )

class VouchView(discord.ui.View):
    def __init__(self, vouchData, bot):
        super().__init__(timeout=300)

        self.add_item(
            VouchSelect(vouchData, bot)
        )