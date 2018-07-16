from __future__ import print_function

import boto3
import json
import logging
import os

from urllib2 import Request, urlopen, URLError, HTTPError

HOOK_URL = os.environ['HookUrl']
# The Slack channel to send a message to stored in the slackChannel environment variable
SLACK_CHANNEL = os.environ['slackChannel']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    object_size = event['Records'][0]['s3']['object']['size']
    
    rekog = boto3.client('rekognition', 'us-east-1')
    logger.info(object_key)
    response = rekog.detect_labels(
        Image={
            'S3Object':{
                'Bucket':bucket_name,
                'Name': object_key
            }
        },
		MaxLabels=10,
		MinConfidence=90
    )

    result = ''
    for label in response['Labels']:
	    result += "{Name} - {Confidence}%\n".format(**label)

    
    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': "%s is posted in bucket %s.\n image analysis:\n %s" % (object_key, bucket_name, result)
    }

    req = Request(HOOK_URL, json.dumps(slack_message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
