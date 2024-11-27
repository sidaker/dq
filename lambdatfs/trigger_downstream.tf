resource "aws_s3_bucket_notification" "bucket_notification_downstream" {
  bucket = "${var.output_bucket}-${var.namespace}"

  lambda_function {
    lambda_function_arn = "arn:aws:lambda:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:function:api-cross-record-scored-${var.namespace}-lambda-trigger"
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "log-consolidator/20"
    filter_suffix       = ".csv"
  }

  count = var.pipeline_count
}

