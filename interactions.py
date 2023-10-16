from tweety import Twitter
from tweety.filters import SearchFilters
from tweety.types.twDataTypes import Tweet
from ai import AiResponse

class ArvoreTweets:
    def __init__(self, parentTweet:Tweet) -> None:
        self.text = parentTweet.text
        self.author = parentTweet.author.username #type:ignore

        self.replies = []
    
    @property
    def asJson(self) -> str: #type:ignore
        tweetDict = {"text": self.text}
        if self.replies:
            tweetDict["replies"] = [reply.asJson for reply in self.replies]
        return json.dumps(tweetDict, indent=1)
        

class Agent: 
    def __init__(self, user:str='', password:str='') -> None:
        self.client:Twitter = Twitter("sessao")
        if user and password:
            self.client.sign_in(user, password)
        self.old_notifications = []

    @property
    def NewNotifications(self) -> list[Tweet]:
        """
        Returns a list of new notifications (tweets) that the bot received, but didnt reply.

        :return: A list of Tweet objects representing the new notifications.
        :rtype: list[Tweet]
        """
        allTweets = self.client.search(keyword='to:poptimedev -from:poptimedev', filter_=SearchFilters.Latest()).results
        nonRepliedTweets = []
        for tweet in allTweets:
            try:
                threads = [ConversationThread for ConversationThread in tweet.get_comments()]
                allReplies = [tweet.expand() for tweet in threads] #type: ignore
                if "poptimedev" not in [reply.author.username for item in allReplies for reply in item]:
                    nonRepliedTweets.append(tweet)
            except Exception as e:
                with open("error.txt", "w") as f:
                    f.write(str(e))
                
        nonRepliedTweets = [tweet for tweet in nonRepliedTweets if tweet not in self.old_notifications]
        self.old_notifications = nonRepliedTweets
        return nonRepliedTweets
    
    def GetContextOfReply(self, tweet:Tweet) -> ArvoreTweets|None:
        """
        Receives:
            - tweet (Tweet): The tweet to get the context from.
        Returns:
            - ArvoreTweets: A tree with the parents. Starts in the root of the conversation (the post) and ends in the reply (the tweet arg)
        """
        print('Called!')
        def build_tree(tweet: Tweet) -> ArvoreTweets:
            tree = ArvoreTweets(tweet)
            for reply in tweet.get_comments():
                tree.replies.append(build_tree(reply))
            return tree
        parentTweet = tweet.get_reply_to()  #type: ignore
        print(parentTweet)
        if parentTweet:
            print('Found parent tweet {}'.format(parentTweet))
            while parentTweet.get_reply_to(): #type: ignore
                parentTweet = parentTweet.get_reply_to() #type: ignore
            return build_tree(parentTweet) #type: ignore
        


        
    
if __name__ == '__main__':
    import json ; secrets = json.load(open('secrets.json', mode='r'))
    agent = Agent(secrets['twitter']['login'], secrets['twitter']['passwd'])
    #agent = Agent()
    notifications = agent.NewNotifications
    print(agent.GetContextOfReply(notifications[0]))