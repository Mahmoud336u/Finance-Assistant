variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource tagging"
  default     = "ai-finance-assistant"
}

variable "plaid_secret_name" {
  description = "Name of the Secrets Manager secret for Plaid API keys"
  default     = "plaid_credentials"
}
