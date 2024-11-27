data "archive_file" "lambda_athena_zip" {
  type        = "zip"
  source_dir  = "${local.path_module}/lambda/athena/code"
  output_path = "${local.path_module}/lambda/athena/package/lambda.zip"
  count       = var.pipeline_count
}

resource "aws_lambda_function" "lambda_athena" {
  filename         = "${path.module}/lambda/athena/package/lambda.zip"
  function_name    = "${var.pipeline_name}-${var.namespace}-lambda-athena"
  role             = aws_iam_role.lambda_role_athena[0].arn
  handler          = "function.lambda_handler"
  source_code_hash = data.archive_file.lambda_athena_zip[0].output_base64sha256
  runtime          = "python3.8"
  timeout          = "900"

  environment {
    variables = {
      output_bucket_name = "s3://${var.output_bucket}-${var.namespace}"
      glue_database      = aws_glue_catalog_database.aws_glue_catalog_database[0].name
      namespace          = var.namespace
    }
  }

  tags = {
    Name = "lambda-athena-${local.naming_suffix}"
  }

  # lifecycle {
  #   ignore_changes = [
  #     filename,
  #     last_modified,
  #     source_code_hash,
  #   ]
  # }

  count = var.pipeline_count
}

resource "aws_iam_policy" "lambda_policy_athena" {
  name = "${var.pipeline_name}-${var.namespace}-lambda-policy-athena"

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
        "arn:aws:s3:::${var.input_bucket}-${var.namespace}",
        "arn:aws:s3:::${var.input_bucket}-${var.namespace}/*"
      ]
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
                "s3:DeleteObject"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::${var.input_bucket}-${var.namespace}/*",
        "arn:aws:s3:::${var.output_bucket}-${var.namespace}/*"
      ]
    },
    {
      "Action": [
                "s3:GetBucketLocation",
                "s3:GetObject",
                "s3:ListBucket"
      ],
      "Effect": "Allow",
      "Resource": [
        "${join(
  "\",\"",
  formatlist(
    "arn:aws:s3:::%s-%s",
    var.readonly_bucket_list,
    var.namespace,
  ),
  )}",
        "${join(
  "\",\"",
  formatlist(
    "arn:aws:s3:::%s-%s/*",
    var.readonly_bucket_list,
    var.namespace,
  ),
  )}"
      ]
    },
    {
      "Action": [
        "glue:GetDatabase",
        "glue:CreateTable",
        "glue:DeleteTable",
        "glue:GetTable",
        "glue:UpdateTable",
        "glue:GetPartition",
        "glue:GetPartitions",
        "glue:BatchCreatePartition",
        "glue:BatchDeletePartition"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:catalog",
        "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:database/${var.database_name}_${var.namespace}",
        "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:table/${var.database_name}_${var.namespace}/*",
        "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:database/${var.input_database_name}_${var.namespace}",
        "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:table/${var.input_database_name}_${var.namespace}/*"
      ]
    },
    {
      "Action": [
        "glue:GetDatabase",
        "glue:GetTable",
        "glue:GetPartition",
        "glue:GetPartitions"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:database/default",
        "${join(
  "\",\"",
  formatlist(
    "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:database/%s_%s",
    var.readonly_database_name_list,
    var.namespace,
  ),
  )}",
        "${join(
  "\",\"",
  formatlist(
    "arn:aws:glue:eu-west-2:${data.aws_caller_identity.current.account_id}:table/%s_%s/*",
    var.readonly_database_name_list,
    var.namespace,
  ),
)}"
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


count = var.pipeline_count
}

resource "aws_iam_role_policy_attachment" "lambda_policy_athena" {
  role       = aws_iam_role.lambda_role_athena[0].id
  policy_arn = aws_iam_policy.lambda_policy_athena[0].arn
  count      = var.pipeline_count
}

resource "aws_iam_role" "lambda_role_athena" {
  name = "${var.pipeline_name}-${var.namespace}-lambda-role-athena"

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
    Name = "lambda-role-athena-${local.naming_suffix}"
  }

  count = var.pipeline_count
}

resource "aws_cloudwatch_log_group" "lambda_log_group_athena" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_athena[0].function_name}"
  retention_in_days = 60

  tags = {
    Name = "lambda-log-group-athena-${local.naming_suffix}"
  }

  count = var.pipeline_count
}

resource "aws_iam_policy" "lambda_logging_policy_athena" {
  name        = "${var.pipeline_name}-${var.namespace}-lambda-logging-policy-athena"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogStream",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:*:log-stream:*",
        "${aws_cloudwatch_log_group.lambda_log_group_athena[0].arn}",
        "${aws_cloudwatch_log_group.lambda_log_group_athena[0].arn}/*"
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

resource "aws_iam_role_policy_attachment" "lambda_logging_policy_attachment_athena" {
  role       = aws_iam_role.lambda_role_athena[0].name
  policy_arn = aws_iam_policy.lambda_logging_policy_athena[0].arn
  count      = var.pipeline_count
}
