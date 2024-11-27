data "archive_file" "lambda_partition_cleanup" {
  type        = "zip"
  source_dir  = "${local.path_module}/lambda/partition_cleanup/code"
  output_path = "${local.path_module}/lambda/partition_cleanup/package/lambda.zip"
}

resource "aws_lambda_function" "lambda_partition_cleanup" {
  filename         = "${path.module}/lambda/partition_cleanup/package/lambda.zip"
  function_name    = "${var.pipeline_name}-${var.namespace}-lambda-partition-cleanup"
  role             = aws_iam_role.lambda_role_partition_cleanup.arn
  handler          = "function.lambda_handler"
  source_code_hash = data.archive_file.lambda_partition_cleanup.output_base64sha256
  runtime          = "python3.8"
  timeout          = "900"

  environment {
    variables = {
      athena_log        = "${var.output_bucket}-${var.namespace}"
      athena_log_prefix = var.athena_log_prefix
      database_name     = "${var.input_database_name}_${var.namespace}"
      table_name        = var.input_table_name
    }
  }

  tags = {
    Name = "lambda-partition-cleanup-${local.naming_suffix}"
  }

  # lifecycle {
  #   ignore_changes = [
  #     filename,
  #     last_modified,
  #     source_code_hash,
  #   ]
  # }
}

resource "aws_iam_policy" "lambda_policy_partition_cleanup" {
  name = "${var.pipeline_name}-${var.namespace}-lambda-policy-partition-cleanup"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryExecution",
        "athena:GetQueryResults"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Action": [
                "s3:GetBucketLocation",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
                "s3:ListMultipartUploadParts",
                "s3:AbortMultipartUpload",
                "s3:PutObject"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::${var.output_bucket}-${var.namespace}",
        "arn:aws:s3:::${var.output_bucket}-${var.namespace}/*"
      ]
    },
    {
      "Action": [
        "glue:GetDatabase",
        "glue:GetPartition",
        "glue:GetPartitions",
        "glue:GetTable",
        "glue:BatchDeletePartition",
        "glue:DeletePartition"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:catalog",
        "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:database/${var.input_database_name}_${var.namespace}",
        "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:table/${var.input_database_name}_${var.namespace}/*"
      ]
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
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:GenerateDataKey"
      ],
      "Effect": "Allow",
      "Resource": "${data.aws_kms_alias.glue.arn}"
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

}

resource "aws_iam_role_policy_attachment" "lambda_policy_partition_cleanup" {
  role       = aws_iam_role.lambda_role_partition_cleanup.id
  policy_arn = aws_iam_policy.lambda_policy_partition_cleanup.arn
}

resource "aws_iam_role" "lambda_role_partition_cleanup" {
  name = "${var.pipeline_name}-${var.namespace}-lambda-role-partition-cleanup"

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
    Name = "lambda-role-partition-cleanup-${local.naming_suffix}"
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group_partition_cleanup" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_partition_cleanup.function_name}"
  retention_in_days = 60

  tags = {
    Name = "lambda-log-group-partition-cleanup-${local.naming_suffix}"
  }
}

resource "aws_iam_policy" "lambda_logging_policy_partition_cleanup" {
  name        = "${var.pipeline_name}-${var.namespace}-lambda-logging-policy-partition_cleanup"
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
        "${aws_cloudwatch_log_group.lambda_log_group_partition_cleanup.arn}",
        "${aws_cloudwatch_log_group.lambda_log_group_partition_cleanup.arn}/*",
        "${aws_cloudwatch_log_group.lambda_log_group_partition_cleanup.arn}:*"
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

resource "aws_iam_role_policy_attachment" "lambda_logging_policy_attachment_partition_cleanup" {
  role       = aws_iam_role.lambda_role_partition_cleanup.name
  policy_arn = aws_iam_policy.lambda_logging_policy_partition_cleanup.arn
}

resource "aws_cloudwatch_event_rule" "partition_cleanup_daily" {
  name                = "${var.pipeline_name}-${var.namespace}-partition_cleanup"
  description         = "API input partitions cleanup once a day"
  schedule_expression = "cron(0 11 * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda_partition_cleanup_daily" {
  rule = aws_cloudwatch_event_rule.partition_cleanup_daily.name
  arn  = aws_lambda_function.lambda_partition_cleanup.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda_cleanup_daily" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_partition_cleanup.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.partition_cleanup_daily.arn
}
