import re
import logging

logger = logging.getLogger(__name__)

def find_and_convert_twitter_links(content):
    """
    Find X.com (Twitter) links in a message and convert them to FixupX.com links.
    
    Args:
        content (str): The message content to search for links
        
    Returns:
        list: A list of converted links, or an empty list if no links were found
    """
    # Define regex patterns for different Twitter URL formats
    # This pattern matches both x.com and twitter.com links
    patterns = [
        r'https?://(?:www\.)?x\.com/\S+',
        r'https?://(?:www\.)?twitter\.com/\S+'
    ]
    
    converted_links = []
    
    # Search for all patterns in the message content
    for pattern in patterns:
        links = re.findall(pattern, content)
        
        # Convert each found link
        for link in links:
            # Replace twitter.com with fixupx.com
            if 'twitter.com' in link:
                converted_link = link.replace('twitter.com', 'fixupx.com')
            else:
                converted_link = link.replace('x.com', 'fixupx.com')
            
            converted_links.append(converted_link)
    
    if converted_links:
        logger.debug(f"Found and converted {len(converted_links)} Twitter/X links")
    
    return converted_links
