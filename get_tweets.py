import datetime
import json

import tqdm
import tweepy
from tweepy import Tweet

import my_secrets

client = tweepy.Client(my_secrets.BEARER_TOKEN)


user_id = 1552075163545608198

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


with open("gold.jsonl", "a") as f:
    for tweet in tqdm.tqdm(
        tweepy.Paginator(
            client.get_users_tweets,
            user_id,
            # end_time=datetime.datetime(2021, 4, 9, 0, 0),
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
