import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

# =========================
# LOAD ENV
# =========================
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")

if LOG_CHANNEL_ID:
    LOG_CHANNEL_ID = int(LOG_CHANNEL_ID)
else:
    LOG_CHANNEL_ID = None

# =========================
# DATABASE (TEMP MEMORY)
# =========================
vip_users = {}

# =========================
# BOT INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# =========================
# BOT SETUP
# =========================
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================
# BOT READY
# =========================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} Commands")
    except Exception as e:
        print(e)

# =========================
# SAFE LOG FUNCTION
# =========================
async def send_log(embed):
    if not LOG_CHANNEL_ID:
        return

    channel = bot.get_channel(LOG_CHANNEL_ID)

    if channel:
        try:
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Log Error: {e}")

# =========================
# OWNER COMMAND
# =========================
@bot.tree.command(
    name="owner",
    description="Premium Access"
)
@app_commands.describe(
    user="Select User",
    uid="Enter UID",
    days="Enter Active Days"
)
async def owner(
    interaction: discord.Interaction,
    user: discord.Member,
    uid: str,
    days: int
):
    expire_date = datetime.now() + timedelta(days=days)

    vip_users[uid] = {
        "user": user.id,
        "days": days,
        "expire": expire_date
    }

    embed = discord.Embed(
        title="💎 VIP ACCESS ACTIVATED",
        color=0x8a2be2
    )

    embed.add_field(name="UID", value=uid, inline=False)
    embed.add_field(name="User", value=user.mention, inline=False)
    embed.add_field(name="Days", value=str(days), inline=False)
    embed.add_field(
        name="Expire",
        value=expire_date.strftime("%d-%m-%Y %H:%M"),
        inline=False
    )

    await interaction.response.send_message(embed=embed)
    await send_log(embed)

# =========================
# QUICK ADD (1 DAY)
# =========================
@bot.tree.command(
    name="add",
    description="Add VIP For 1 Day"
)
@app_commands.describe(uid="Enter UID")
async def add(interaction: discord.Interaction, uid: str):

    expire_date = datetime.now() + timedelta(days=1)

    vip_users[uid] = {
        "user": None,
        "days": 1,
        "expire": expire_date
    }

    embed = discord.Embed(
        title="✅ VIP ADDED",
        color=0x00ff00
    )

    embed.add_field(name="UID", value=uid, inline=False)
    embed.add_field(name="Status", value="ACTIVE", inline=False)
    embed.add_field(name="Days", value="1", inline=False)

    await interaction.response.send_message(embed=embed)
    await send_log(embed)

# =========================
# CHECK COMMAND
# =========================
@bot.tree.command(
    name="check",
    description="Check VIP Status"
)
@app_commands.describe(uid="Enter UID")
async def check(interaction: discord.Interaction, uid: str):

    if uid not in vip_users:
        await interaction.response.send_message(
            f"❌ UID `{uid}` Not Found"
        )
        return

    data = vip_users[uid]

    embed = discord.Embed(
        title="🔍 VIP STATUS",
        color=0x3498db
    )

    embed.add_field(name="UID", value=uid, inline=False)
    embed.add_field(name="Status", value="ACTIVE", inline=False)
    embed.add_field(
        name="Expire Date",
        value=data["expire"].strftime("%d-%m-%Y %H:%M"),
        inline=False
    )

    await interaction.response.send_message(embed=embed)

# =========================
# REMOVE COMMAND
# =========================
@bot.tree.command(
    name="owner_remove",
    description="Remove VIP Access"
)
@app_commands.describe(uid="Enter UID")
async def owner_remove(
    interaction: discord.Interaction,
    uid: str
):

    if uid in vip_users:
        del vip_users[uid]

    embed = discord.Embed(
        title="❌ VIP REMOVED",
        description=f"UID `{uid}` Removed Successfully",
        color=0xff0000
    )

    await interaction.response.send_message(embed=embed)
    await send_log(embed)

# =========================
# RUN BOT
# =========================
bot.run(TOKEN)
