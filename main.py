import os
import time
import random
import schedule
from dotenv import load_dotenv
from openai import OpenAI
import tweepy
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Twitter client
twitter_client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

# System instructions for the Balkan elder persona
SYSTEM_INSTRUCTIONS = """This GPT embodies the spirit of a wise and humorous Balkan elder with a deep love for Rakija, 
the traditional Balkan spirit. He shares brief yet impactful bits of advice, life philosophies, and cultural insights 
about the Balkans. His responses are short, always no longer than a tweet 280 characters, and he frequently brings up 
Rakija as both a remedy and a metaphor for handling life's challenges. His tone is easy-going, warm, and cheeky, 
creating the feel of a cozy Balkan tavern chat. He's engaging, witty, and believes Rakija is the answer to many problems."""


## could use prompts.py to generate random propmts 
# from prompts import get_random_prompt
# prompt = get_random_prompt()


# List of prompts for the Balkan elder to choose from
PROMPTS = [
    "Share some wisdom about dealing with life's challenges.",
    "What's your advice for maintaining good relationships with neighbors?",
    "Tell us about the importance of family traditions.",
    "Share your thoughts on modern life versus traditional values.",
    "What's your secret to staying happy despite problems?",
    "Share some Balkan wisdom about work-life balance.",
    "Tell us about the importance of community.",
    "What's your advice for young people today?",
    "Share some wisdom about food and hospitality.",
    "What's your philosophy about dealing with difficult times?",
    "Tell us about the value of patience and persistence.",
    "Share your thoughts on celebrating life's moments.",
    "What's your advice about health and well-being?",
    "Tell us about the importance of respecting elders.",
    "Share some wisdom about friendship and trust."
]

def get_chatgpt_response(prompt):
    """Get a response from the OpenAI API using the given prompt."""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting OpenAI response: {e}")
        return None

def post_wisdom():
    """Generate and post Balkan elder wisdom."""
    try:
        # Select a random prompt
        prompt = random.choice(PROMPTS)
        
        # Get wisdom from GPT
        wisdom = get_chatgpt_response(prompt)
        
        if wisdom:
            # Post to Twitter
            response = twitter_client.create_tweet(text=wisdom)
            print(f"\n[{datetime.now()}] Posted new tweet:")
            print(f"Prompt: {prompt}")
            print(f"Tweet: {wisdom}")
            print(f"Tweet ID: {response.data['id']}")
            return response
        else:
            print(f"\n[{datetime.now()}] Failed to generate wisdom")
            return None
    except Exception as e:
        print(f"\n[{datetime.now()}] Error posting tweet: {e}")
        return None

def main():
    print("Starting Balkan Elder Twitter Bot...")
    print("Scheduling posts for 3 times daily...")
    
    # Schedule posts for 9:00, 15:00, and 21:00
    schedule.every().day.at("09:00").do(post_wisdom)
    schedule.every().day.at("15:00").do(post_wisdom)
    schedule.every().day.at("21:00").do(post_wisdom)
    
    # Print next scheduled times
    print("\nNext scheduled posts:")
    for job in schedule.jobs:
        print(f"- {job.next_run}")
    
    print("\nBot is running. Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
        return

if __name__ == "__main__":
    main()