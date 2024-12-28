import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Sorry I Dont have time i gonna work on counter only 

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set up for countdown target date (New Year's)
NEW_YEAR = datetime(2025, 1, 1, 0, 0, 0)
scheduler = AsyncIOScheduler()
channel = None
last_message = None

# Discord intents configuration
intents = discord.Intents.default()
intents.message_content = True  # To read message content
intents.guilds = True  # To listen to guild events (like bot joining servers)

# Prefix function - Multiple possible prefixes
def get_prefix(bot, message):
    return ["","!", "?", "="]

bot = commands.Bot(command_prefix=get_prefix, intents=intents)

# Bot ready event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Find the first available text channel in one of the joined servers and send the countdown message
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                # Call the countdown function by passing the context for this channel
                ctx = await bot.get_context(await channel.send(f"\n ```COUNTER TO NEW YEAR 2025 EVE: WITH [GOJOEVE] 🌒🎆``` \n"))
                await countdown(ctx)  # Call the countdown function here
                break

    # Start countdown updater scheduler
    scheduler.add_job(update_countdown, "interval", seconds=10)
    scheduler.start()
    await bot.change_presence(activity=discord.Game(name="Bot is active"))


# Event when the bot joins a server
@bot.event
async def on_guild_join(guild):
    try:
        # Try to get the first text channel that the bot has permission to send messages in
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                # Call the countdown function by passing the context for this channel
                ctx = await bot.get_context(await channel.send(f"\n ```COUNTER TO NEW YEAR 2025 EVE: WITH [GOJOEVE] 🌒🎆``` \n"))
                await countdown(ctx)  # Call the countdown function here
                break
    except Exception as e:
        print(f"Error sending introduction message: {e}")

# Responds to any command error
@bot.event
# async def on_command_error(ctx, error):
async def on_command_error(ctx):
    # await ctx.send(f"Error: {error}")
    await countdown(ctx)

# Command: echo
@bot.command()
async def echo(ctx, arg):
    global channel
    channel = ctx.channel
    await ctx.send(f"Echoing: {arg}")

# Command: countdown
@bot.command()
async def countdown(ctx):
    global channel
    channel = ctx.channel
    now = datetime.now()
    if now >= NEW_YEAR:
        await ctx.send(f"**Happy New Year!** 🌒")
        scheduler.shutdown()
    else:
        delta = NEW_YEAR - now
        days, hours, minutes, seconds = delta.days, delta.seconds // 3600, (delta.seconds // 60) % 60, delta.seconds % 60
        countdown_message = f"{create_banner()}\n" \
                            f"**Countdown to New Year** ⌛🌒 \n" \
                            f"**`{days}` days** : **`{hours}` hours** : **`{minutes}` minutes** : **`{seconds}` seconds**\n" \
                            f"{create_banner()}\n\n\n" 
        global last_message
        last_message = await channel.send(countdown_message)

# Function to create minimalist banner (simple separator)
def create_banner():
    """Create a minimal separator using elegant characters."""
    # return "" * 10  
    return "\n"  # for now

# Function to update the countdown (scheduled to run every 10 seconds)
async def update_countdown():
    global last_message
    global channel
    if channel is None:
        print("Channel is not set.")
        return
    
    now = datetime.now()
    if now >= NEW_YEAR:
        if last_message:
            await last_message.edit(content=f"**Happy New Year!** 🌒")
        scheduler.shutdown()  # Stop the scheduler after the event is met
    else:
        delta = NEW_YEAR - now
        days, hours, minutes, seconds = delta.days, delta.seconds // 3600, (delta.seconds // 60) % 60, delta.seconds % 60
        countdown_message = f"{create_banner()}\n" \
                            f"**Countdown to New Year** ⌛🌒 \n" \
                            f"**`{days}` days** : **`{hours}` hours** : **`{minutes}` minutes** : **`{seconds}` seconds**\n" \
                            f"{create_banner()}\n\n\n"
        
        if last_message:
            await last_message.edit(content=countdown_message)
        else:
            last_message = await channel.send(countdown_message)


bot.run(DISCORD_BOT_TOKEN)
