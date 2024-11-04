import os
from dotenv import load_dotenv
import tweepy

# Load environment variables from .env file
load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

try:
    # Replace the text with whatever you want to Tweet about
    response = client.create_tweet(text='Hello world! Testing Twitter API v2')
    print(response)
except Exception as e:
    print(f"Error: {e}")
    # Print the actual values being used (first few chars)
    print("\nDebug - Checking credentials:")
    print(f"Consumer Key: {os.getenv('TWITTER_CONSUMER_KEY')[:8]}...")
    print(f"Access Token: {os.getenv('TWITTER_ACCESS_TOKEN')[:8]}...")