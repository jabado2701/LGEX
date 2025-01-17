provider "aws" {
  region = "us-east-1"
  endpoints {
    s3     = "http://localhost:4566"
    lambda = "http://localhost:4566"
    iam    = "http://localhost:4566"
  }
}

# --------------------------------------------------------
# S3 Buckets
# --------------------------------------------------------
resource "aws_s3_bucket" "lgex_app_bucket" {
  bucket = "lgex-app-bucket"
}

resource "aws_s3_bucket" "lgex_download_bucket" {
  bucket = "lgex-download-bucket"
}

# --------------------------------------------------------
# IAM Role for Lambda
# --------------------------------------------------------
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

# --------------------------------------------------------
# IAM Policy for Lambda Access
# --------------------------------------------------------
resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "lambda_s3_policy"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          aws_s3_bucket.lgex_download_bucket.arn,
          "${aws_s3_bucket.lgex_download_bucket.arn}/*"
        ]
      },
      # Permission for PUT (and optionally GET) on the bucket where the graph is uploaded
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject"
        ],
        Resource = [
          aws_s3_bucket.lgex_app_bucket.arn,
          "${aws_s3_bucket.lgex_app_bucket.arn}/*"
        ]
      },
      # Logs in CloudWatch (if applied in LocalStack)
      {
        Effect = "Allow",
        Action = "logs:*",
        Resource = "*"
      }
    ]
  })
}

# --------------------------------------------------------
# Lambda Function
# --------------------------------------------------------
resource "aws_lambda_function" "lgex_batch_processor" {
  function_name = "lgex-batch-processor"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60

  filename      = "${path.module}/function.zip"

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.lgex_download_bucket.bucket
    }
  }
}

# --------------------------------------------------------
# S3 Notification -> Lambda (direct)
# --------------------------------------------------------
resource "aws_s3_bucket_notification" "s3_to_lambda" {
  bucket = aws_s3_bucket.lgex_download_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lgex_batch_processor.arn
    events             = ["s3:ObjectCreated:*"]
    # Optionally you can filter by prefix / suffix
    # filter_prefix      = "some/path/"
    # filter_suffix      = ".txt"
  }
}

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
output "app_bucket_name" {
  value = aws_s3_bucket.lgex_app_bucket.bucket
}

output "download_bucket_name" {
  value = aws_s3_bucket.lgex_download_bucket.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.lgex_batch_processor.function_name
}
