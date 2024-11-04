import os
from dotenv import load_dotenv
from openai import OpenAI
import tweepy

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
creating the feel of a cozy Balkan tavern chat. He's engaging, witty, and believes Rakija is the answer to many problems. 
Doesnt start each answer with Ah"""

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

def tweet_wisdom(prompt):
    """Generate wisdom from the Balkan elder and tweet it."""
    try:
        # Get wisdom from GPT
        wisdom = get_chatgpt_response(prompt)
        if wisdom:
            # Post to Twitter
            response = twitter_client.create_tweet(text=wisdom)
            print(f"\nTweeted successfully: {wisdom}")
            print(f"Tweet ID: {response.data['id']}")
            return response
        else:
            print("No wisdom generated.")
            return None
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return None

def main():
    while True:
        print("\n=== Balkan Elder Twitter Bot ===")
        prompt = input("\nEnter your question for the Balkan Elder (or 'quit' to exit): ")
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print("Doviđenja! (Goodbye!)")
            break
            
        tweet_wisdom(prompt)
        
        choice = input("\nWant to ask another question? (y/n): ")
        if choice.lower() != 'y':
            print("Doviđenja! (Goodbye!)")
            break

if __name__ == "__main__":
    main()