import discord
from discord.ext import commands
import re
import datetime
from api.getVouches import getVouches
from api.vouchPageinatorMenu import VouchPageinatorView

def is_user_mention(text: str):
    return re.fullmatch(r"<@!?\d+>", text) is not None

async def sendDm(client, userId, msg="", embed=""):
    user = await client.fetch_user(userId)
    await user.send(msg, embed=embed)

def createEmbed(vouches, userId, targetUser):
    vouchData = vouches

    total_vouches = sum(
        1 for v in vouchData
        if not v.get("is_unvouch", False)
    ) - sum(
        1 for v in vouchData
        if v.get("is_unvouch", False)
    )

    total_approved = sum(
        1 for v in vouchData
        if v.get("verified", False) and not v.get("is_unvouch", False)
    ) - sum(
        1 for v in vouchData
        if v.get("verified", False) and v.get("is_unvouch", False)
    )

    embed = discord.Embed(
        title=f"Vouches for {targetUser.display_name}",
        color=0x2ECC71,
        timestamp=datetime.datetime.now()
    )

    embed.add_field(
        name="Username",
        value=targetUser.mention,
        inline=False
    )

    embed.add_field(
        name="Total Vouches",
        value=str(total_vouches),
        inline=True
    )

    embed.add_field(
        name="Total Approved",
        value=str(total_approved),
        inline=True
    )

    embed.set_thumbnail(
        url=targetUser.display_avatar.url
    )

    embed.set_footer(
        text="Select a vouch below to view details"
    )

    return embed

def buildNoVouchesEmbed(targetUser):
    embed = discord.Embed(
        title=f"No vouches found!",
        color=0x2ECC71,
        description=f"User {targetUser.id} has no vouches.",
        timestamp=datetime.datetime.now()
    )

    embed.set_thumbnail(
        url=targetUser.display_avatar.url
    )

    return embed

class Vouches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        client = self.bot
        if ctx.author.bot:
            return

        message = ctx.content
        senderId = ctx.author.id
        args = message.split(" ")

        if args[0] == "+vouches":
            print(f"Vouch listener fired: {ctx.id}")

            if len(args) == 1:
                vouches = getVouches(senderId, client.supabase)[1].data
                targetUser = await client.fetch_user(senderId)
                if vouches == []:
                    await ctx.reply(embed=buildNoVouchesEmbed(targetUser))
                    return
                await ctx.reply(
                    embed=createEmbed(
                        vouches,
                        senderId,
                        targetUser
                    ),
                    view=VouchPageinatorView(vouches, client)
                )

                return

            elif is_user_mention(args[1]):
                mentionId = int(args[1].replace("<","").replace("@","").replace("!","").replace(">",""))
                vouches = getVouches(mentionId, client.supabase)[1].data
                targetUser = await client.fetch_user(mentionId)
                if vouches == []:
                    await ctx.reply(embed=buildNoVouchesEmbed(targetUser))
                    return
                await ctx.reply(
                    embed=createEmbed(
                        vouches,
                        mentionId,
                        targetUser
                    ),
                    view=VouchPageinatorView(vouches, client)
                )

                return

            else:
                embed = discord.Embed(
                    title="Invalid User",
                    description="Please mention a valid user to get vouches",
                    color=0xE74C3C,
                    timestamp=datetime.datetime.now()
                )
                await ctx.reply(embed=embed)

                return


async def setup(bot):
    await bot.add_cog(Vouches(bot))