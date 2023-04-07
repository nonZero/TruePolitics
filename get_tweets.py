import datetime
import json

import tqdm
import tweepy
from tweepy import Tweet
from pprint import pp

import my_secrets # Add your Twitter API key here

client = tweepy.Client(my_secrets.BEARER_TOKEN)


user_id = 1552409123425337346 # Change to desired user ID

with open("output.jsonl", "a") as f:
    for tweet in tqdm.tqdm(
        tweepy.Paginator(
            client.get_users_tweets,
            user_id,
            max_results=100,
            tweet_fields="created_at,source",
            expansions="referenced_tweets.id",
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
