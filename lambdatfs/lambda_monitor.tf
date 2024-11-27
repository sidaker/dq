resource "aws_iam_role" "lambda_monitor" {
  name = "${var.monitor_name}-${var.namespace}-lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = {
    Name = "iam-${var.monitor_name}-lambda-${local.naming_suffix}"
  }
}

resource "aws_iam_policy" "lambda_monitor_policy" {
  name = "${var.monitor_name}-${var.namespace}-lambda-policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:PutObject",
        "s3:List*"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::${var.monitored_bucket}-${var.namespace}",
        "arn:aws:s3:::${var.monitored_bucket}-${var.namespace}/*"]
    },
    {
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:GenerateDataKey*",
        "kms:DescribeKey"
      ],
      "Effect": "Allow",
      "Resource": "${var.kms_key_s3}"
    },
    {
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/slack_notification_webhook"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_monitor_policy" {
  role       = aws_iam_role.lambda_monitor.id
  policy_arn = aws_iam_policy.lambda_monitor_policy.arn
}

data "archive_file" "lambda_monitor_zip" {
  type        = "zip"
  source_dir  = "${local.path_module}/lambda/monitor/code"
  output_path = "${local.path_module}/lambda/monitor/package/lambda_monitor.zip"
}

resource "aws_lambda_function" "lambda_monitor" {
  filename         = "${path.module}/lambda/monitor/package/lambda_monitor.zip"
  function_name    = "${var.monitor_name}-${var.namespace}-lambda"
  role             = aws_iam_role.lambda_monitor.arn
  handler          = "monitor.lambda_handler"
  source_code_hash = data.archive_file.lambda_monitor_zip.output_base64sha256
  runtime          = "python3.8"
  timeout          = "900"
  memory_size      = "2048"

  environment {
    variables = {
      bucket_name    = "${var.monitored_bucket}-${var.namespace}"
      origin_bucket  = "${var.input_bucket}-${var.namespace}"
      path_          = var.output_path
      threashold_min = var.monitor_lambda_run
    }
  }

  tags = {
    Name = "lambda-${var.monitor_name}-${local.naming_suffix}"
  }
}

resource "aws_cloudwatch_log_group" "lambda_monitor" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_monitor.function_name}"
  retention_in_days = 90

  tags = {
    Name = "log-lambda-${local.naming_suffix}"
  }
}

resource "aws_iam_policy" "lambda_monitor_logging" {
  name        = "${var.monitor_name}-${var.namespace}-lambda-logging"
  path        = "/"
  description = "IAM policy for monitor lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "${aws_cloudwatch_log_group.lambda_monitor.arn}",
        "${aws_cloudwatch_log_group.lambda_monitor.arn}/*"
      ],
      "Effect": "Allow"
    },
    {
       "Action": "logs:CreateLogGroup",
       "Resource": "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*",
       "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_monitor_logs" {
  role       = aws_iam_role.lambda_monitor.name
  policy_arn = aws_iam_policy.lambda_monitor_logging.arn
}

resource "aws_cloudwatch_event_rule" "lambda_monitor_rule" {
  name                = "${var.monitor_name}-${var.namespace}-cw-event-rule"
  description         = "Fires every fifteen minutes"
  schedule_expression = "rate(${var.monitor_lambda_run} minutes)"
  is_enabled          = var.namespace == "prod" ? "true" : "true"
}

resource "aws_cloudwatch_event_target" "lambda_monitor_target" {
  rule = aws_cloudwatch_event_rule.lambda_monitor_rule.name
  arn  = aws_lambda_function.lambda_monitor.arn
}

resource "aws_lambda_permission" "monitor_cw_permission" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_monitor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_monitor_rule.arn
}
