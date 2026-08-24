import os
from dotenv import load_dotenv
from supabase import create_client, Client
import discord
from discord.ext import commands
from cachetools import TTLCache

from api.vouchStaffButtonsView import vouchStaffButtonsView

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
TOKEN = os.getenv("BOT_TOKEN")
supabase: Client = create_client(url, key)
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

client = commands.Bot(command_prefix="+", intents=intents)
tree = client.tree
member_cache = TTLCache(maxsize=1, ttl=300)

GUILD_ID = 1378519415565320212

@client.event
async def on_ready():

    await setUpViews()

    # await tree.sync()
    guild = discord.Object(id=GUILD_ID)
    tree.clear_commands(guild=guild)
    # tree.clear_commands(guild=None)

    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)

    print("READY")

async def setUpViews():
    client.add_view(vouchStaffButtonsView(vouchId=None, supabase=supabase))

async def load_extensions():
    # ======= Vouches ========
    await client.load_extension("cogs.vouch.vouch")
    await client.load_extension("cogs.vouch.vouches")
    await client.load_extension("cogs.vouch.getVouch")
        # ======= Admin ========
    await client.load_extension("cogs.vouch.aprooveVouch")
    await client.load_extension("cogs.vouch.deleteVouch")
    await client.load_extension("cogs.vouch.addVouch")

    # ======= miscellaneous ========
    await client.load_extension("cogs.miscellaneous.checkCode")
    await client.load_extension("cogs.miscellaneous.capeRoles")

    # ======= ticketManagement ========
    await client.load_extension("cogs.ticketManagement.sendTicketManuall")

    # ======= Groups ========
    # await client.load_extension("cogs.mitelenius.groups")
    
@client.event
async def setup_hook():
    client.supabase = supabase
    await load_extensions()
    
# print(f"Token: {TOKEN}")
client.run(TOKEN)