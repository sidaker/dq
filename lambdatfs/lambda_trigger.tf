resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_trigger[0].arn
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${var.input_bucket}-${var.namespace}"
  count         = var.pipeline_count
}

data "archive_file" "lambda_trigger_zip" {
  type        = "zip"
  source_dir  = "${local.path_module}/lambda/trigger/code"
  output_path = "${local.path_module}/lambda/trigger/package/lambda.zip"
  count       = var.pipeline_count
}

resource "aws_lambda_function" "lambda_trigger" {
  filename         = "${path.module}/lambda/trigger/package/lambda.zip"
  function_name    = "${var.pipeline_name}-${var.namespace}-lambda-trigger"
  role             = aws_iam_role.lambda_role_trigger[0].arn
  handler          = "trigger.lambda_handler"
  source_code_hash = data.archive_file.lambda_trigger_zip[0].output_base64sha256
  runtime          = "python3.8"
  timeout          = "60"

  environment {
    variables = {
      circuit_breaker_parameter_name = aws_ssm_parameter.lambda_trigger_enabled[0].name
      state_machine_name             = aws_sfn_state_machine.sfn_state_machine[0].name
    }
  }

  tags = {
    Name = "lambda-trigger-${local.naming_suffix}"
  }

  lifecycle {
    ignore_changes = [
      filename,
      last_modified,
      source_code_hash,
    ]
  }

  count = var.pipeline_count
}

resource "aws_iam_policy" "lambda_policy_trigger" {
  name = "${var.pipeline_name}-${var.namespace}-lambda-policy-trigger"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "states:StartExecution"
      ],
      "Effect": "Allow",
      "Resource": "${aws_sfn_state_machine.sfn_state_machine[0].id}"
    },
    {
      "Action": [
        "ssm:GetParameter"
      ],
      "Effect": "Allow",
      "Resource": "${aws_ssm_parameter.lambda_trigger_enabled[0].arn}"
    },
    {
      "Action": [
        "ssm:GetParameter"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/slack_notification_webhook"
      ]
    }
  ]
}
EOF


  count = var.pipeline_count
}

resource "aws_iam_role_policy_attachment" "lambda_policy_trigger" {
  role       = aws_iam_role.lambda_role_trigger[0].id
  policy_arn = aws_iam_policy.lambda_policy_trigger[0].arn
  count      = var.pipeline_count
}

resource "aws_iam_role" "lambda_role_trigger" {
  name = "${var.pipeline_name}-${var.namespace}-lambda-role-trigger"

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
    Name = "iam-lambda-trigger-${local.naming_suffix}"
  }

  count = var.pipeline_count
}

resource "aws_cloudwatch_log_group" "lambda_log_group_trigger" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_trigger[0].function_name}"
  retention_in_days = 60

  tags = {
    Name = "lambda-log-group-trigger-${local.naming_suffix}"
  }

  count = var.pipeline_count
}

resource "aws_iam_policy" "lambda_logging_policy_trigger" {
  name        = "${var.pipeline_name}-${var.namespace}-lambda-logging-policy-trigger"
  path        = "/"
  description = "IAM policy for logging from a lambda"

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
        "${aws_cloudwatch_log_group.lambda_log_group_trigger[0].arn}",
        "${aws_cloudwatch_log_group.lambda_log_group_trigger[0].arn}/*"
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


  count = var.pipeline_count
}

resource "aws_iam_role_policy_attachment" "lambda_logging_policy_attachment_trigger" {
  role       = aws_iam_role.lambda_role_trigger[0].name
  policy_arn = aws_iam_policy.lambda_logging_policy_trigger[0].arn
  count      = var.pipeline_count
}
