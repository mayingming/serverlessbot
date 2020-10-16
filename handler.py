import json
import tweepy
import config
import csv
import os


# Send twitter every 10 minutes

def twitter(event, context):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth)

    # Post the first message and deleted it from message file
    # If no messsage left, send error
    with open(config.MESSAGE_FILE, 'r') as readfile, open(config.TEMP_FILE, 'w') as writefile:
        reader = csv.reader(readfile)
        mlist = list(reader)
        if len(mlist) > 1:
            writer = csv.writer(writefile)
            for i, row in enumerate(mlist):
                if i == 1:
                    api.update_status(row[0])
                else:
                    writer.writerow(row)

            os.remove(config.MESSAGE_FILE)
            os.rename(config.TEMP_FILE, config.MESSAGE_FILE)

            body = {
                "message": "twitter posted",
                "input": event
            }

            response = {
                "statusCode": 200,
                "body": json.dumps(body)
            }
        else:
            error = {
                "message": "No message left, twitter post failed.",
                "input": event
            }

            response = {
                "statusCode": 400,
                "error": json.dumps(error)
            }

    return response
