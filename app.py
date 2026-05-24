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
        except discord.Forbidden:
            print("❌ Bot has no permission to send messages in log channel")
        except Exception as e:
            print(f"❌ Log error: {e}")

# =========================
# SLASH COMMAND: OWNER
# =========================
@bot.tree.command(
    name="owner",
    description=" Premium Access"
)
@app_commands.describe(
    user="Select User",
    uid="Enter UID",
    days="Enter Active Days"
)
async def owner(interaction: discord.Interaction, user: discord.Member, uid: str, days: int):

    expire_date = datetime.now() + timedelta(days=days)
    formatted_expire = expire_date.strftime("%d-%m-%Y %H:%M")

    embed = discord.Embed(
        title="💎 VIP ACCESS ACTIVATED",
        description="A new premium user has been activated successfully.",
        color=0x8a2be2
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(name="🆔 UID", value=f"`{uid}`", inline=True)
    embed.add_field(name="🟢 STATUS", value="ACTIVE", inline=True)
    embed.add_field(name="👑 ACCESS", value="PREMIUM ", inline=True)

    embed.add_field(name="👤 USER", value=user.mention, inline=True)
    embed.add_field(name="📅 ACTIVE DAYS", value=f"{days} DAYS", inline=True)
    embed.add_field(name="⏰ EXPIRES ON", value=formatted_expire, inline=True)

    embed.set_footer(text="AXB PREMIUM SECURITY")

    await interaction.response.send_message(embed=embed)

    await send_log(embed)

# =========================
# SLASH COMMAND: REMOVE
# =========================
@bot.tree.command(
    name="owner_remove",
    description="Remove VIP Access from UID"
)
@app_commands.describe(uid="Enter UID to remove")
async def owner_remove(interaction: discord.Interaction, uid: str):

    embed = discord.Embed(
        title="❌ VIP ACCESS REMOVED",
        description=f"VIP Access for UID `{uid}` has been removed.",
        color=0xFF0000
    )

    embed.set_footer(text="AXB PREMIUM SECURITY")

    await interaction.response.send_message(embed=embed)

    await send_log(embed)

# =========================
# RUN BOT
# =========================
bot.run(TOKEN)
