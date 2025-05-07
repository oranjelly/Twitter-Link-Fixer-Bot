import discord
import re
import os
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the token from environment variables
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up intents (permissions)
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content

# Initialize the Discord client
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info(f"✅ Bot is ready and logged in as {client.user}")
    logger.info(f"Connected to {len(client.guilds)} servers")
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="for X.com links"))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    twitter_links = re.findall(r'https?://(?:www\.)?twitter\.com\S+',
                               message.content)
    x_links = re.findall(r'https?://(?:www\.)?x\.com\S+', message.content)

    all_links = twitter_links + x_links
    if not all_links:
        return

    fixed_links = [
        link.replace('twitter.com',
                     'fixupx.com').replace('x.com', 'fixupx.com')
        for link in all_links
    ]

    try:
        await message.delete()
    except discord.Forbidden:
        logger.warning(
            f"Bot lacks permission to delete messages in {message.channel}")
        return
    except discord.HTTPException as e:
        logger.warning(f"Failed to delete message: {e}")
        return

    reply = f"{message.author.mention} 🔁 Fixed link:\n" + "\n".join(
        fixed_links)
    await message.channel.send(reply)


async def run_bot():
    try:
        logger.info("🚀 Starting the Discord bot...")
        await client.start(TOKEN)
    except discord.errors.HTTPException as e:
        if e.status == 429:
            logger.error(
                "⚠️ Rate limited. Waiting for 15 minutes before retrying...")
            await asyncio.sleep(900)
            await run_bot()
        else:
            logger.error(f"❌ Error: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    if not TOKEN:
        logger.error(
            "🔐 No Discord token found. Please set the DISCORD_TOKEN environment variable."
        )
    else:
        import asyncio
        asyncio.run(run_bot())
