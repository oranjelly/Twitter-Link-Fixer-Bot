import discord
import os
import logging
import asyncio

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


async def test_connection():
    try:
        logger.info("🚀 Testing Discord connection...")
        await client.login(TOKEN)
        await client.close()
        logger.info("✅ Successfully connected to Discord.")
    except discord.errors.HTTPException as e:
        logger.error(f"⚠️ HTTP Error: {e}")
    except discord.errors.LoginFailure:
        logger.error("❌ Invalid Discord token.")
    except Exception as e:
        logger.error(f"⚠️ Error: {e}")


if __name__ == "__main__":
    if not TOKEN:
        logger.error(
            "🔐 No Discord token found. Please set the DISCORD_TOKEN environment variable."
        )
    else:
        asyncio.run(test_connection())
