variable "naming_suffix" {
  default = "apps-test-dq"
}

variable "path_module" {
  default = "unset"
}

locals {
  naming_suffix = "${var.pipeline_name}-${var.naming_suffix}"
  path_module   = var.path_module != "unset" ? var.path_module : path.module
}

variable "namespace" {
  default = "test"
}

variable "pipeline_name" {
  default = "api-record-level-score"
}

variable "database_name" {
  default = "api_record_level_score"
}

variable "input_database_name" {
  default = "api_input"
}

variable "input_table_name" {
  default = "input_file_api"
}

variable "readonly_database_name_list" {
  default = [
    "reference_data",
    "acl",
    "consolidated_schedule",
    "api_input",
    "oag_transform",
  ]
}

variable "input_bucket" {
  default = "s3-dq-api-internal"
}

variable "output_bucket" {
  default = "s3-dq-api-record-level-scoring"
}

variable "readonly_bucket_list" {
  default = ["s3-dq-api-archive", "s3-dq-reference-data-internal", "s3-dq-consolidated-schedule"]
}

variable "kms_key_s3" {
  description = "The ARN of the KMS key that is used to encrypt S3 buckets"
  default     = "arn:aws:kms:eu-west-2:797728447925:key/ad7169c4-6d6a-4d21-84ee-a3b54f4bef87"
}

variable "kms_key_glue" {
  description = "The ARN of the KMS key that is used to encrypt the glue metadata catalog"
  default     = "arn:aws:kms:eu-west-2:797728447925:key/804f851d-439b-4d4b-9720-37a3f3739000"
}

variable "lambda_slack" {
  type        = list(string)
  description = "The ARN of the Lambda function that will produce the Slack alerts"
  default     = ["arn:aws:lambda:eu-west-2:797728447925:function:ops-test-slack"]
}

variable "pipeline_count" {
  default = 1
}

variable "environment" {
  default     = "notprod"
  description = "Switch between environments"
}

variable "athena_log_prefix" {
  default = "lambda-partition-cleanup-log"
}

variable "monitor_name" {
  default = "api-record-level-score-monitor"
}

variable "monitored_bucket" {
  default = "s3-dq-api-record-level-scoring"
}

variable "monitor_lambda_run" {
  default = "15"
}

variable "output_path" {
  default = ""
}
