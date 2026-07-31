import discord
from discord.ext import commands
import time
import re
from api.vouchStaffButtonsView import vouchStaffButtonsView
import api.vouch as vouch
import datetime

VOUCH_APPROVE_CHANNEL_ID = 1527827736859775027

def is_user_mention(text: str):
    return re.fullmatch(r"<@!?\d+>", text) is not None

async def sendDm(client, userId, msg="", embed=""):
    user = await client.fetch_user(userId)
    await user.send(msg, embed=embed)

class Vouch(commands.Cog):
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

        if args[0] == "+vouch":
            print(f"Vouch listener fired: {ctx.id}")
            
            if (ctx.channel.id != 1428068846086127766 and ctx.channel.id != 1458858003666309261):
                embed = discord.Embed(
                    title="Incorect Channel",
                    description="Please Vouch a member in <#1428068846086127766>!",
                    color=0xE74C3C
                )
                await ctx.reply(embed=embed)

                return
            if len(args) == 1:
                embed = discord.Embed(
                    title="Missing Arguments",
                    description="Please provide a user mention to submit a vouch.",
                    color=0xE74C3C
                )
                await ctx.reply(embed=embed)

                return
            elif is_user_mention(args[1]):
                mentionId = int(args[1].replace("<","").replace("@","").replace("!","").replace(">",""))

                if mentionId == senderId:
                    await ctx.add_reaction("❌")
                    embed = discord.Embed(
                        title="Action Denied",
                        description="You cannot submit a vouch for yourself.",
                        color=0xE74C3C
                    )
                    await ctx.author.send(embed=embed)
                    return

                key = (senderId, mentionId)
                if key in vouch.whoVouchedWhoWhen:
                    if time.time() - vouch.whoVouchedWhoWhen[key] < 30 * 60:
                        await ctx.add_reaction("❌")
                        embed = discord.Embed(
                            title="Cooldown Active",
                            description="You may vouch this user again in 30 minutes.",
                            color=0xF39C12
                        )
                        await ctx.author.send(embed=embed)
                        return

                msg = ""
                if len(args) > 1:
                    for i in range(2, len(args)):
                        msg = " ".join(args[2:])

                print("Before submitVouch")

                submitedVouch = vouch.submitVouch(
                    senderId,
                    mentionId,
                    msg,
                    client.supabase
                )

                print("After submitVouch")

                # print(submitedVouch)

                if submitedVouch[0]:
                    await ctx.add_reaction("✅")
                    target_user = await client.fetch_user(mentionId)
                    created_at = datetime.datetime.fromisoformat(submitedVouch[1].data[0]['created_at'])

                    embed = discord.Embed(
                        title="Vouch Submitted Successfully",
                        description=f"You successfully vouched <@{mentionId}> (`{mentionId}`).",
                        color=0x2ECC71,
                        timestamp=created_at
                    )
                    embed.set_footer(text=f'Vouch ID: {submitedVouch[1].data[0]['id']}',icon_url=target_user.display_avatar.url)

                    await ctx.author.send(embed=embed)

                    

                    target_embed = discord.Embed(
                        title="You Received a Vouch",
                        description=f"You have been vouched by <@{senderId}> (`{senderId}`).",
                        color=0x3498DB,
                        timestamp=created_at
                    )
                    target_embed.set_footer(text=f'Vouch ID: {submitedVouch[1].data[0]['id']}',icon_url=ctx.author.display_avatar.url)

                    if target_user:
                        target_embed.set_author(
                            name=target_user.name,
                            icon_url=target_user.display_avatar.url
                        )

                    await sendDm(client, mentionId, embed=target_embed)

                    vouchChanellEmbed = discord.Embed(
                        title="New Vouch Submitted",
                        description=f"A new vouch has been submitted for <@{mentionId}> (`{mentionId}`).",
                        color=0x2ECC71
                    )
                    vouchChanellEmbed.add_field(
                        name="Vouch Details",
                        value=f"**Vouched User:** <@{mentionId}> (`{mentionId}`)\n**Vouched By:** <@{senderId}> (`{senderId}`)\n**Reason:** {msg}\n**Created At:** {created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                        inline=False
                    )
                    vouchChanellEmbed.set_footer(text=f'Vouch ID: {submitedVouch[1].data[0]['id']}',icon_url=ctx.author.display_avatar.url)

                    await client.get_channel(VOUCH_APPROVE_CHANNEL_ID).send(embed=vouchChanellEmbed, view=vouchStaffButtonsView(submitedVouch[1].data[0]['id'], client.supabase))

                else:
                    await ctx.add_reaction("❌")
                    embed = discord.Embed(
                        title="Vouch Failed",
                        description=f"An error occurred while submitting your vouch:\n```{submitedVouch[1]}```",
                        color=0xE74C3C
                    )
                    await ctx.author.send(embed=embed)

            else:
                await ctx.add_reaction("❌")
                embed = discord.Embed(
                    title="Invalid User",
                    description="Please mention a valid user to submit a vouch.",
                    color=0xE74C3C
                )
                await ctx.author.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Vouch(bot))