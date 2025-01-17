#######################################################
# 1) AWS Provider (LocalStack Example)
#######################################################
provider "aws" {
  region = "us-east-1"
  endpoints {
    s3     = "http://localhost:4566"
    lambda = "http://localhost:4566"
    iam    = "http://localhost:4566"
    sqs    = "http://localhost:4566"
  }
}

#######################################################
# 2) S3 Buckets
#######################################################
resource "aws_s3_bucket" "lgex_app_bucket" {
  bucket = "lgex-app-bucket"
}

resource "aws_s3_bucket" "lgex_download_bucket" {
  bucket = "lgex-download-bucket"
}

#######################################################
# 3) SQS Queue
#######################################################
resource "aws_sqs_queue" "lgex_queue" {
  name = "lgex-queue"
}

# Policy to allow S3 to send messages to the queue
data "aws_iam_policy_document" "sqs_queue_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }
    actions = [
      "SQS:SendMessage"
    ]
    resources = [
      aws_sqs_queue.lgex_queue.arn
    ]
    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_s3_bucket.lgex_download_bucket.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "allow_s3" {
  queue_url = aws_sqs_queue.lgex_queue.id
  policy    = data.aws_iam_policy_document.sqs_queue_policy.json
}

#######################################################
# 4) S3 -> SQS Notification
#######################################################
resource "aws_s3_bucket_notification" "s3_to_sqs" {
  bucket = aws_s3_bucket.lgex_download_bucket.id

  queue {
    queue_arn = aws_sqs_queue.lgex_queue.arn
    events    = ["s3:ObjectCreated:*"]
  }
}

#######################################################
# 5) IAM Role for Lambda
#######################################################
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Effect = "Allow",
        Sid    = ""
      }
    ]
  })
}

#######################################################
# 6) IAM Policy for Lambda Access
#######################################################
resource "aws_iam_role_policy" "lambda_s3_sqs_policy" {
  name = "lambda_s3_sqs_policy"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # S3 Permissions
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject"
        ],
        Resource = [
          aws_s3_bucket.lgex_download_bucket.arn,
          "${aws_s3_bucket.lgex_download_bucket.arn}/*",
          aws_s3_bucket.lgex_app_bucket.arn,
          "${aws_s3_bucket.lgex_app_bucket.arn}/*"
        ]
      },
      # Logs in CloudWatch
      {
        Effect = "Allow",
        Action = "logs:*",
        Resource = "*"
      },
      # SQS Permissions (for event source mapping to poll SQS)
      {
        Effect = "Allow",
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:GetQueueUrl"
        ],
        Resource = [
          aws_sqs_queue.lgex_queue.arn
        ]
      }
    ]
  })
}

#######################################################
# 7) Lambda Function
#######################################################
resource "aws_lambda_function" "lgex_batch_processor" {
  function_name = "lgex-batch-processor"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60

  # Update this to point to your zip file if needed
  filename = "${path.module}/function.zip"

  # Provide environment variables if needed
  environment {
    variables = {
      DOWNLOAD_BUCKET = aws_s3_bucket.lgex_download_bucket.bucket
      APP_BUCKET      = aws_s3_bucket.lgex_app_bucket.bucket
    }
  }
}

#######################################################
# 8) Lambda Event Source Mapping (SQS -> Lambda)
#######################################################
resource "aws_lambda_event_source_mapping" "sqs_to_lambda" {
  event_source_arn = aws_sqs_queue.lgex_queue.arn
  function_name    = aws_lambda_function.lgex_batch_processor.arn

  batch_size = 3
  enabled    = true

}

#######################################################
# 9) Outputs
#######################################################
output "app_bucket_name" {
  value = aws_s3_bucket.lgex_app_bucket.bucket
}

output "download_bucket_name" {
  value = aws_s3_bucket.lgex_download_bucket.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.lgex_batch_processor.function_name
}

output "sqs_queue_url" {
  value = aws_sqs_queue.lgex_queue.url
}

output "sqs_queue_arn" {
  value = aws_sqs_queue.lgex_queue.arn
}
