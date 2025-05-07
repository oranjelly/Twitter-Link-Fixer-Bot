"""
Configuration file for the Discord bot and web application
Contains settings that can be modified
"""
import os

class Config:
    # Discord Bot Configuration
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    
    # Web Server Configuration
    UPTIME_PORT = 8080  # Port for the UptimeRobot web server
    FLASK_PORT = 5000   # Port for the main Flask web app
    
    # Link Conversion Settings
    ALTERNATIVE_FRONTEND = "fixupx.com"  # The alternative frontend to use for Twitter links
    
    # Logging Configuration
    LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL