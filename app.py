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

LOG_CHANNEL_ID = int(LOG_CHANNEL_ID) if LOG_CHANNEL_ID else None

# =========================
# TEMP DATABASE
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
        print(f"Sync Error: {e}")

# =========================
# LOG FUNCTION
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
    description="Give Premium Access"
)
@app_commands.describe(
    user="Select User",
    uid="Enter UID",
    days="Active Days"
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

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(name="🆔 UID", value=f"`{uid}`", inline=False)
    embed.add_field(name="👤 USER", value=user.mention, inline=False)
    embed.add_field(name="📅 DAYS", value=str(days), inline=False)
    embed.add_field(
        name="⏰ EXPIRES",
        value=expire_date.strftime("%d-%m-%Y %H:%M"),
        inline=False
    )

    embed.set_footer(text="AXB PREMIUM SECURITY")

    await interaction.response.send_message(embed=embed)
    await send_log(embed)

# =========================
# UID ADD COMMAND
# =========================
@bot.tree.command(
    name="uid_add",
    description="Add UID For 1 Day"
)
@app_commands.describe(uid="Enter UID")
async def uid_add(
    interaction: discord.Interaction,
    uid: str
):

    expire_date = datetime.now() + timedelta(days=1)

    vip_users[uid] = {
        "user": None,
        "days": 1,
        "expire": expire_date
    }

    embed = discord.Embed(
        title="✅ UID ADDED",
        color=0x00ff00
    )

    embed.add_field(name="🆔 UID", value=f"`{uid}`", inline=False)
    embed.add_field(name="🟢 STATUS", value="ACTIVE", inline=False)
    embed.add_field(name="📅 DAYS", value="1 DAY", inline=False)

    embed.set_footer(text="AXB PREMIUM SECURITY")

    await interaction.response.send_message(embed=embed)
    await send_log(embed)

# =========================
# STATUS COMMAND
# =========================
@bot.tree.command(
    name="status",
    description="Check UID Status"
)
@app_commands.describe(uid="Enter UID")
async def status(
    interaction: discord.Interaction,
    uid: str
):

    if uid not in vip_users:
        await interaction.response.send_message(
            f"❌ UID `{uid}` Not Found"
        )
        return

    data = vip_users[uid]

    embed = discord.Embed(
        title="🔍 UID STATUS",
        color=0x3498db
    )

    embed.add_field(name="🆔 UID", value=f"`{uid}`", inline=False)
    embed.add_field(name="🟢 STATUS", value="ACTIVE", inline=False)
    embed.add_field(
        name="⏰ EXPIRES",
        value=data["expire"].strftime("%d-%m-%Y %H:%M"),
        inline=False
    )

    embed.set_footer(text="AXB PREMIUM SECURITY")

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
        title="❌ VIP ACCESS REMOVED",
        description=f"UID `{uid}` Removed Successfully",
        color=0xff0000
    )

    embed.set_footer(text="AXB PREMIUM SECURITY")

    await interaction.response.send_message(embed=embed)
    await send_log(embed)

# =========================
# RUN BOT
# =========================
bot.run(TOKEN)
