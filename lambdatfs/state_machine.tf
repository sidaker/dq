resource "aws_sfn_state_machine" "sfn_state_machine" {
  name     = "${var.pipeline_name}-${var.namespace}-state-machine"
  role_arn = aws_iam_role.step_function_exec[0].arn

  definition = <<EOF
{
  "Comment": "Run just the athena lambda.",
  "StartAt": "RunAthena",
  "States": {
    "RunAthena": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.lambda_athena[0].arn}",
      "End": true,
      "Retry": [ {
        "ErrorEquals": [ "States.ALL"],
        "IntervalSeconds": 30,
        "MaxAttempts": 1
      } ],
      "Catch": [ {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.error-info",
        "Next": "SlackAlert"
      } ]
    },
    "SlackAlert": {
      "Type": "Task",
      "Resource": "${var.lambda_slack[0]}",
      "End": true
    }
  }
}
EOF


  tags = {
    Name = "sfn-state-machine-${local.naming_suffix}"
  }

  count = var.pipeline_count
}

