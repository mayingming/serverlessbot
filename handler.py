import json
import tweepy
import config
import csv


def twitter(event, context):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth)

    messages = []
    with open(config.MESSAGE_FILE) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            messages.append(row[0])
    for i in range(1, len(messages)):
        api.update_status(messages[i])
        print(messages[i])
        time.sleep(60 * config.TIME_SLOT)

    body = {
        "message": "All handled",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
