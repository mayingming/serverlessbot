import json
import tweepy
import config
import csv
import os
import boto3
import botocore


# Send twitter every 5 minutes

def tweet(event, context):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth)

    # Post the first message and deleted it from message file
    # If no messsage left, send error

    s3 = boto3.resource("s3")
    s3_client = boto3.client('s3')
    bucket_name = "tbot-bucket"
    bucket = s3.Bucket(bucket_name)
    newname = '/tmp/'+config.TEMP_FILE_TO_DELETE

    try:
        s3_client.download_file(bucket_name, config.TEMP_FILE, newname)
        # The object does exist.
        with open(newname, 'r') as readfile, open('/tmp/'+config.TEMP_FILE, 'w') as writefile:
            reader = csv.reader(readfile)
            mlist = list(reader)
            writer = csv.writer(writefile)
            if len(mlist) > 1:
                writer = csv.writer(writefile)
                for i, row in enumerate(mlist):
                    if i == 1:
                        api.update_status(row[0])
                    else:
                        writer.writerow(row)
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
            readfile.close()
            writefile.close()
            bucket.upload_file('/tmp/'+config.TEMP_FILE, config.TEMP_FILE)

    except botocore.exceptions.ClientError as e:

        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            with open(config.MESSAGE_FILE, 'r') as readfile, open('/tmp/'+config.TEMP_FILE, 'w') as writefile:
                reader = csv.reader(readfile)
                mlist = list(reader)
                writer = csv.writer(writefile)
                for i, row in enumerate(mlist):
                    if i == 1:
                        api.update_status(row[0])
                    else:
                        writer.writerow(row)

                body = {
                    "message": "twitter posted",
                    "input": event
                }

                response = {
                    "statusCode": 200,
                    "body": json.dumps(body)
                }
                readfile.close()
                writefile.close()
                bucket.upload_file('/tmp/'+config.TEMP_FILE, config.TEMP_FILE)
        else:
            # Something else has gone wrong.
            raise

    return response
