variable "REGION" {
  description = "Desired region"
  type = string
  default = "eu-west-2"
}

variable "LAMBDA_NAME1" {
    description = "Name of lambda used for pipeline 1"
    type = string
    default = "c16-trenet-pipeline1-lambda"
}

variable "LAMBDA_NAME2" {
    description = "Name of lambda used for pipeline 2"
    type = string
    default = "c16-trenet-pipeline2-lambda"
}

variable "PIPELINE1_SCHEDULE_NAME" {
    description = "EventBridge Schedule name for pipeline 1"
    type = string
    default = "c16-trenet-pipeline1_scheduled_event" 
}

variable "PIPELINE2_SCHEDULE_NAME" {
    description = "EventBridge Schedule name for pipeline 2"
    type = string
    default = "c16-trenet-pipeline2_scheduled_event"
}

variable "SCHEDULE1_TRIGGER_RATE" {
    description = "EventBridge Schedule trigger frequency for pipeline 1"
    type = string
    default = "rate(1 minute)"
}

variable "SCHEDULE2_TRIGGER_RATE" {
    description = "EventBridge Schedule trigger frequency for pipeline 2"
    type = string
    default = "rate(1 hour)"
}
