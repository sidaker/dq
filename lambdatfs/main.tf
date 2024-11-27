data "aws_caller_identity" "current" {
}

resource "aws_ssm_parameter" "lambda_trigger_enabled" {
  name  = "${var.pipeline_name}-${var.namespace}-lambda-trigger-enabled"
  type  = "String"
  value = "y"

  tags = {
    Name = "ssm-lambda-trigger-enabled-${local.naming_suffix}"
  }

  count = var.pipeline_count
}

resource "aws_iam_role" "step_function_exec" {
  name = "${var.pipeline_name}-${var.namespace}-step-function-exec"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF


  count = var.pipeline_count
}

resource "aws_iam_policy" "step_function_exec_policy" {
  name = "${var.pipeline_name}-${var.namespace}-step-function-exec-policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "${aws_lambda_function.lambda_athena[0].arn}",
                "${var.lambda_slack[0]}"
            ]
        }
    ]
}
EOF


  count = var.pipeline_count
}

resource "aws_iam_role_policy_attachment" "step_function_exec_policy" {
  role       = aws_iam_role.step_function_exec[0].id
  policy_arn = aws_iam_policy.step_function_exec_policy[0].arn
  count      = var.pipeline_count
}


resource "aws_glue_catalog_database" "aws_glue_catalog_database" {
  name  = "${var.database_name}_${var.namespace}"
  count = var.pipeline_count
}
