import discord
from discord.ext import commands
import time
from api.vouchStaffButtonsView import vouchStaffButtonsView
import api.vouch as vouch
import datetime
from api.mitelanius import is_user_id, is_user_mention, sendDm

VOUCH_APPROVE_CHANNEL_ID = 1527827736859775027
#VOUCH_APPROVE_CHANNEL_ID = 1458858003666309261

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

        if args[0] != "+vouch" and args[0] != "-vouch":
            return

        if args[0].startswith("+"):
            vU = False
            vouchType = "Vouch"
        elif args[0].startswith("-"):
            vU = True
            vouchType = "Unvouch"

        if (ctx.channel.id != 1428068846086127766 and ctx.channel.id != 1458858003666309261):
            embed = discord.Embed(
                title="Incorect Channel",
                description=f"Please {vouchType.lower()} a member in <#1428068846086127766>!",
                color=0xE74C3C
            )
            await ctx.reply(embed=embed)

            return
        
        if len(args) == 1:
            embed = discord.Embed(
                title="Missing Arguments",
                description=f"Please provide a user mention to submit a {vouchType.lower()}.",
                color=0xE74C3C
            )
            await ctx.reply(embed=embed)

            return
        
        if not is_user_mention(args[1]) and not is_user_id(args[1]):
            
            await ctx.add_reaction("❌")
            embed = discord.Embed(
                title="Invalid User",
                description=f"Please mention a valid user to submit a {vouchType.lower()}.",
                color=0xE74C3C
            )
            await ctx.author.send(embed=embed)

            return
        if is_user_mention(args[1]):
            mentionId = int(args[1].replace("<","").replace("@","").replace("!","").replace(">",""))
        else: 
            mentionId = int(args[1])

        if mentionId == senderId:
            await ctx.add_reaction("❌")
            embed = discord.Embed(
                title="Action Denied",
                description=f"You cannot submit a {vouchType.lower()} for yourself.",
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
                    description=f"You may {vouchType.lower()} this user again in 30 minutes.",
                    color=0xF39C12
                )
                await ctx.author.send(embed=embed)
                return

        msg = ""
        if len(args) > 1:
            for i in range(2, len(args)):
                msg = " ".join(args[2:])

        submitedVouch = vouch.submitVouch(
            senderId,
            mentionId,
            msg,
            client.supabase,
            vU
        )

        if not submitedVouch[0] or submitedVouch[1] == []:
            await ctx.add_reaction("❌")
            embed = discord.Embed(
                title=f"{vouchType} Failed",
                description=f"An error occurred while submitting your {vouchType.lower()}:\n```{submitedVouch[1]}```",
                color=0xE74C3C
            )
            await ctx.author.send(embed=embed)

            return
        
        await ctx.add_reaction("✅")
        target_user = await client.fetch_user(mentionId)
        created_at = datetime.datetime.fromisoformat(submitedVouch[1].data[0]['created_at'])

        embed = discord.Embed(
            title=f"{vouchType} Submitted Successfully",
            description=f"You successfully {vouchType.lower()} <@{mentionId}> (`{mentionId}`).",
            color=0x2ECC71,
            timestamp=created_at
        )
        embed.set_footer(text=f'{vouchType} ID: {submitedVouch[1].data[0]['id']}',icon_url=target_user.display_avatar.url)

        await ctx.author.send(embed=embed)

        target_embed = discord.Embed(
            title=f"You Received a {vouchType}",
            description=f"You have been {vouchType.lower()} by <@{senderId}> (`{senderId}`).",
            color=0x3498DB,
            timestamp=created_at
        )
        target_embed.set_footer(text=f'{vouchType} ID: {submitedVouch[1].data[0]['id']}',icon_url=ctx.author.display_avatar.url)

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

async def setup(bot):
    await bot.add_cog(Vouch(bot))