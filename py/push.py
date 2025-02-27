import boto3

def send_sns_message(topic_arn, message, subject=None):
    """
    Send a message to an SNS topic.

    :param topic_arn: The ARN of the SNS topic.
    :param message: The message to send.
    :param subject: The subject of the message (optional).
    """
    sns_client = boto3.client('sns')
    
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )
    
    return response