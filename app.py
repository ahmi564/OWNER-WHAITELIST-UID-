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
OWNER_GUILD_ID = os.getenv("OWNER_GUILD_ID")

if LOG_CHANNEL_ID:
    LOG_CHANNEL_ID = int(LOG_CHANNEL_ID)
else:
    LOG_CHANNEL_ID = None

if OWNER_GUILD_ID:
    OWNER_GUILD_ID = int(OWNER_GUILD_ID)
else:
    OWNER_GUILD_ID = None

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
# SECURITY CHECK FUNCTION
# =========================

async def security_check(interaction: discord.Interaction):
    # Sirf Mere Server Me Chلے
    if interaction.guild is None:
        return False

    if interaction.guild.id != OWNER_GUILD_ID:
        return False

    # Sirf Admin Use Kar Sake
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Only Administrators Can Use This Command.",
            ephemeral=True
        )
        return False

    return True

# =========================
# OWNER COMMAND
# =========================
@bot.tree.command(name="owner", description="Premium Access")
@app_commands.describe(user="Select User", uid="Enter UID", days="Enter Active Days")
async def owner(interaction: discord.Interaction, user: discord.Member, uid: str, days: int):

    if not await security_check(interaction):
        return

    expire_date = datetime.now() + timedelta(days=days)
    formatted_expire = expire_date.strftime("%d-%m-%Y %H:%M")

    vip_users[uid] = {
        "user": user.id,
        "days": days,
        "expire": expire_date
    }

    embed = discord.Embed(
        title="💎 VIP ACCESS ACTIVATED",
        description="A new premium user has been activated successfully.",
        color=0x8a2be2
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(name="🆔 UID", value=f"{uid}", inline=True)
    embed.add_field(name="🟢 STATUS", value="ACTIVE", inline=True)
    embed.add_field(name="👑 ACCESS", value="PREMIUM", inline=True)

    embed.add_field(name="👤 USER", value=user.mention, inline=True)
    embed.add_field(name="📅 ACTIVE DAYS", value=f"{days} DAYS", inline=True)
    embed.add_field(name="⏰ EXPIRES ON", value=formatted_expire, inline=True)

    embed.set_footer(text="AXB PREMIUM SECURITY")

    await interaction.response.send_message(embed=embed)
    await send_log(embed)

# =========================
# UID ADD COMMAND
# =========================
@bot.tree.command(name="uid_add", description="Add UID For 1 Day")
@app_commands.describe(uid="Enter UID")
async def uid_add(interaction: discord.Interaction, uid: str):

    if not await security_check(interaction):
        return

    expire_date = datetime.now() + timedelta(days=1)
    formatted_expire = expire_date.strftime("%d-%m-%Y %H:%M")

    vip_users[uid] = {
        "user": "AXB",
        "days": 1,
        "exp
