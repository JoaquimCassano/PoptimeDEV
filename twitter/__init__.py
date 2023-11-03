from tweety import Twitter ; import os, requests, json

secrets = json.load(open('secrets.json'))


app:Twitter = Twitter("session")

app.sign_in(secrets["twitter"]["login"], secrets["twitter"]["passwd"])

def TimeLine():
    return app.get_home_timeline(pages=4).tweets


def MyTweets():
    return app.user(1).tweets # type:ignore

def Post(text:str, medias:list[str], quote:None|str = None) -> int|tuple[int, str]:
    """
    Posts a text and media files to the app.

    Args:
        text (str): The text to be posted.
        medias (list[str]): The list of media urls.

    Returns:
        int|tuple[int, str]: Returns 0 if the post is successful. If an exception occurs, returns a tuple containing an error code (1) and the error message.

    """
    try:
        media_files:list = []
        for i, media in enumerate(medias):
            media_bytes = requests.get(media).content
            with open(f'temp{i}.jpg', 'wb') as f:
                f.write(media_bytes)
            media_files.append(f'temp{i}.jpg')
        app.create_tweet(text=text, files=media_files, quote_of=quote) # type: ignore
        return 0
    except Exception as e:
        return 1, str(e)
    finally:
        for media_file in media_files: # type: ignore
            os.remove(media_file)

if __name__ == "__main__":
    print(Post("oi oi oi teste teste teste pra poptimedev dnv pq a api caiu", [], quote="https://twitter.com/onlyanerd2/status/1713997696540000723"))