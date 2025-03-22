output "api_gateway_url" {
  value = aws_apigatewayv2_api.finance_api.api_endpoint
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.users.id
}

output "s3_bucket_name" {
  value = aws_s3_bucket.data_lake.id
}
