resource "aws_lambda_function" "plaid_integration" {
  # ... existing config ...
  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }
}
