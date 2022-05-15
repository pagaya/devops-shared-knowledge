import os
import boto3
from botocore.exceptions import ClientError
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


STS = boto3.client('sts')
S3 = boto3.client('s3')


def send_slack(message, print_log=True):
    slack_channel = os.environ["SLACK_CHANNEL_ID"]
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    client = WebClient(token=slack_token)
    if print_log:
        print(message)
    try:
        response = client.chat_postMessage(
            channel=slack_channel,
            text=message
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'


def get_bucket_ownership(bucket, account):
    query = S3.get_bucket_ownership_controls(
        Bucket=bucket,
        ExpectedBucketOwner=account
    )
    return query['OwnershipControls']['Rules'][0].get('ObjectOwnership')


def put_bucket_ownership(bucket, account):
    S3.put_bucket_ownership_controls(
        Bucket=bucket,
        ExpectedBucketOwner=account,
        OwnershipControls={
            'Rules': [
                {
                    'ObjectOwnership': 'BucketOwnerEnforced'
                },
            ]
        }
    )


def lambda_handler(event, context):
    account_id = STS.get_caller_identity()["Account"]
    all_buckets = S3.list_buckets()
    configured_buckets = 0

    for bucket in all_buckets['Buckets']:
        current_bucket = bucket["Name"]
        try:
            bucket_owner = get_bucket_ownership(current_bucket, account_id)
            if bucket_owner != "BucketOwnerEnforced":
                slack_message = f"Bucket `{current_bucket}`, is not configured with `BucketOwnerEnforced`." \
                                f" Check who created this bucket and why it was created misconfigured" \
                                f"\nAccount - *{account_id}*"
                send_slack(slack_message, print_log=False)
                try:
                    print(f"Configuring bucket `{current_bucket}` with `BucketOwnerEnforced`.")
                    put_bucket_ownership(current_bucket, account_id)
                    slack_message = f"Bucket `{current_bucket}` configured successfully with `BucketOwnerEnforced`"
                    send_slack(slack_message)
                    configured_buckets += 1
                except ClientError as e:
                    slack_message = f"Got a ClientError for bucket `{current_bucket}` \n ```{e}```"
                    send_slack(slack_message)
            elif bucket_owner == "BucketOwnerEnforced":
                print(f"Bucket `{current_bucket}` is already configured with `BucketOwnerEnforced`")
                configured_buckets += 1
            else:
                slack_message = f"Unknown issue with bucket `{current_bucket}`, please check manually" \
                                f"\nAccount - *{account_id}*"
                send_slack(slack_message)
        except ClientError as e:
            slack_message = f"Couldn't retrieve Bucket Ownership data for bucket `{current_bucket}`, please check manually." \
                            f"\nAccount ID - *{account_id}*" \
                            f"\nGot the following error: \n ```{e}```"
            send_slack(slack_message)

    if configured_buckets == len(all_buckets['Buckets']):
        slack_message = f"Account *{account_id}* is configured properly with `BucketOwnerEnforced` on all buckets"
        send_slack(slack_message)