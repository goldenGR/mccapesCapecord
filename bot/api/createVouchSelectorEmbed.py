import discord
import datetime

def createVouchSelectorEmbed(vouches, bot, page):
    embed = discord.Embed(
        title=f"Vouches Page {page}",
        color=0x2ECC71,
        timestamp=datetime.datetime.now()
    )

    embed.set_footer(
        text='\u200b',icon_url=bot.get_user(vouches[0]['vouchee']).display_avatar.url
    )

    return embed