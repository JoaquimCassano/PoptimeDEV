from tweety import Twitter
from tweety.filters import SearchFilters
from tweety.types.twDataTypes import Tweet
from ai import AiResponse

class Agent:
    def __init__(self, user:str, password:str) -> None:
        self.client:Twitter = Twitter("session")
        self.client.sign_in(user, password)
        self.old_notifications = []

    @property
    def notifications(self) -> list[Tweet]:
        allTweets = self.client.search(keyword='to:poptimedev -from:poptimedev', filter_=SearchFilters.Latest()).results
        nonRepliedTweets = []
        for tweet in allTweets:
            try:
                threads = [ConversationThread for ConversationThread in tweet.get_comments()]
                allReplies = [tweet.expand() for tweet in threads]
                if "poptimedev" not in [reply.author.username for item in allReplies for reply in item]:
                    nonRepliedTweets.append(tweet)
            except:
                pass
                
        nonRepliedTweets = [tweet for tweet in nonRepliedTweets if tweet not in self.old_notifications]
        self.old_notifications = nonRepliedTweets
        return nonRepliedTweets
    
    
if __name__ == '__main__':
    import json ; secrets = json.load(open('secrets.json'))
    agent = Agent(secrets['twitter']['login'], secrets['twitter']['passwd'])
    for tweet in agent.notifications:
        print(tweet.text, tweet.author.username, sep=' ---- ') #type: ignore