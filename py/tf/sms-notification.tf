provider "aws" {
  region = "us-east-1"
}

resource "aws_sns_topic" "sms_topic" {
  name = "sms_notification_topic"
}

resource "aws_sns_topic_subscription" "sms_subscription" {
  topic_arn = aws_sns_topic.sms_topic.arn
  protocol  = "sms"
  endpoint  = "+5511996669707"
}

output "sns_topic_arn" {
  value = aws_sns_topic.sms_topic.arn
}