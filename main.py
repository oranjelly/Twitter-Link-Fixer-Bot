import discord
import re
import os
import logging
import time
import subprocess

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


def test_connection():
    logger.info("🚀 Testing Discord connection...")
    result = subprocess.run(["python3", "rate_limit_test.py"],
                            capture_output=True,
                            text=True)

    if "429 Too Many Requests" in result.stdout:
        logger.error(
            "⚠️ Rate limited by Discord. Waiting 15 minutes before retrying..."
        )
        time.sleep(900)  # Wait for 15 minutes
        return False

    logger.info("✅ Connection test passed. Starting bot.")
    return True


if __name__ == "__main__":
    if not TOKEN:
        logger.error(
            "🔐 No Discord token found. Please set the DISCORD_TOKEN environment variable."
        )
    else:
        while True:
            if test_connection():
                try:
                    client.run(TOKEN)
                except discord.errors.HTTPException as e:
                    if '429' in str(e):
                        logger.error(
                            "⚠️ Rate limited again. Waiting 15 minutes...")
                        time.sleep(900)  # Wait another 15 minutes
                    else:
                        logger.error(f"Unexpected Error: {e}")
                        break
