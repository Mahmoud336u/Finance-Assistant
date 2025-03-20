# KMS key for encryption
resource "aws_kms_key" "s3_kms_key" {
  description = "KMS key for S3 bucket encryption"
}

# WAF for API Gateway (basic rule set)
resource "aws_wafv2_web_acl" "api_gateway_waf" {
  name        = "${var.project_name}-waf"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 1

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesCommonRuleSet"
      sampled_requests_enabled   = true
    }
  }
}
