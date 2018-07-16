# lambda-slack-demo
Lambda demo for AVPC meet

## Prerequisites
1. Slack account
2. Channel (public/private) on slack
3. incoming-web-hook created on that channel

## slack-alert.py
General event alert in slack. When any file is added in the target S3 bucket, Lambda will trigger an alert in the slack channel.

## slack-image-alert.py
When an image file is dropped in the target S3 bucket, Lambda will use Rekognition to identify objects in the image and send the object labels with high-confidence to slack channel.
