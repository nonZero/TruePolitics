import json

import tqdm
import tweepy
from tweepy import Tweet

import secrets

client = tweepy.Client(secrets.BEARER_TOKEN)


user_id = 2946300174

response = client.get_users_tweets(
    user_id,
    tweet_fields=("created_at",),
)

# for i, tweet in enumerate(response.data):  # type: int, Tweet
#     print(type(tweet))
#     print(tweet.data)
#     print(tweet.text)
#     print(tweet.date)
#     print(tweet.time)


with open("tweets.jsonl", "a") as f:
    for tweet in tqdm.tqdm(
        tweepy.Paginator(
            client.get_users_tweets,
            user_id,
            max_results=100,
            tweet_fields=("created_at",),
        ).flatten(limit=25_000)
    ):
        f.write(
            json.dumps(
                dict(
                    id=tweet.id,
                    text=tweet.text,
                    created_at=tweet.created_at.isoformat(),
                ),
                ensure_ascii=False,
            )
            + "\n"
        )
