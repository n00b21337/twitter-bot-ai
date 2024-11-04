import os
from dotenv import load_dotenv
import tweepy

# Load environment variables from .env file
load_dotenv()

# Initialize Twitter client with bearer token
client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

def search_tweets(username=None, query=None, max_results=100):
    """
    Search for tweets with given parameters.
    Either username or custom query must be provided.
    """
    try:
        # Construct query
        if username:
            search_query = f'from:{username} -is:retweet'
        else:
            search_query = query if query else 'from:suhemparack -is:retweet'

        # Perform search
        tweets = client.search_recent_tweets(
            query=search_query,
            tweet_fields=['context_annotations', 'created_at', 'author_id'],
            max_results=max_results
        )

        # Print results
        if tweets.data is not None:
            print(f"\nFound {len(tweets.data)} tweets:")
            print("=" * 50)
            for tweet in tweets.data:
                print(f"\nTweet text: {tweet.text}")
                print(f"Created at: {tweet.created_at}")
                if hasattr(tweet, 'context_annotations') and tweet.context_annotations:
                    print("\nContext Annotations:")
                    for annotation in tweet.context_annotations:
                        print(f"- {annotation}")
                print("-" * 50)
        else:
            print("No tweets found.")

    except Exception as e:
        print(f"Error searching tweets: {e}")

def main():
    while True:
        print("\n=== Twitter Search Tool ===")
        print("1. Search by username")
        print("2. Custom search query")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            username = input("Enter Twitter username (without @): ")
            max_results = input("Enter maximum number of results (10-100): ")
            try:
                max_results = int(max_results)
                max_results = min(100, max(10, max_results))  # Ensure between 10 and 100
                search_tweets(username=username, max_results=max_results)
            except ValueError:
                print("Invalid number, using default 100 results")
                search_tweets(username=username)
                
        elif choice == '2':
            query = input("Enter your search query: ")
            max_results = input("Enter maximum number of results (10-100): ")
            try:
                max_results = int(max_results)
                max_results = min(100, max(10, max_results))  # Ensure between 10 and 100
                search_tweets(query=query, max_results=max_results)
            except ValueError:
                print("Invalid number, using default 100 results")
                search_tweets(query=query)
                
        elif choice == '3':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()