import discord
import datetime

def createVouchEmbed(vouch, bot):
    embed = discord.Embed(
        title=f"Vouch #{vouch['id']}",
        color=0x2ECC71,
        timestamp=datetime.datetime.now()
    )

    embed.add_field(
        name="Voucher",
        value=f"<@{vouch['voucher']}>",
        inline=False
    )

    embed.add_field(
        name="Vouchee",
        value=f"<@{vouch['vouchee']}>",
        inline=False
    )

    embed.add_field(
        name="Message",
        value=f"```{vouch['message']}```",
        inline=False
    )

    embed.add_field(
        name="Verified?",
        value="True" if vouch["verified"] else "False",
        inline=False
    )

    embed.add_field(
        name="Negative?",
        value="True" if vouch["is_unvouch"] else "False",
        inline=False
    )

    embed.set_footer(
        text='\u200b',icon_url=bot.get_user(vouch['vouchee']).display_avatar.url
    )

    return embed