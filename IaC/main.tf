# Configure AWS provider
provider "aws" {
  region = var.region
}

# S3 Bucket for data lake (Iceberg)
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake"

  tags = {
    Name = "${var.project_name}-data-lake"
  }
}

resource "aws_s3_bucket_acl" "data_lake_acl" {
  bucket = aws_s3_bucket.data_lake.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake_sse" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.s3_kms_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lake_lifecycle" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "intelligent-tiering"
    status = "Enabled"

    transition {
      storage_class = "INTELLIGENT_TIERING"
    }
  }
}

# Block all public access to the data lake bucket
resource "aws_s3_bucket_public_access_block" "data_lake_public_access" {
  bucket                  = aws_s3_bucket.data_lake.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lambda function for Plaid API integration (with VPC config)
resource "aws_lambda_function" "plaid_integration" {
  filename      = "lambda-plaid.zip"
  function_name = "${var.project_name}-plaid-integration"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "python3.12"

  environment {
    variables = {
      PLAID_SECRET_ARN = aws_secretsmanager_secret.plaid_credentials.arn
      S3_BUCKET        = aws_s3_bucket.data_lake.id
    }
  }

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }
}

# Kinesis Data Stream for real-time events
resource "aws_kinesis_stream" "payment_events" {
  name             = "${var.project_name}-payment-events"
  shard_count      = 1
  retention_period = 24
}

# SageMaker model & endpoint (simplified)
resource "aws_sagemaker_model" "finance_model" {
  name               = "${var.project_name}-model"
  execution_role_arn = aws_iam_role.lambda_role.arn

  primary_container {
    image          = "<YOUR_SAGEMAKER_IMAGE_URI>"
    model_data_url = "s3://${aws_s3_bucket.data_lake.id}/model/model.tar.gz"
  }
}

# ECS Fargate cluster for model hosting
resource "aws_ecs_cluster" "finance_cluster" {
  name = "${var.project_name}-cluster"
}

resource "aws_ecs_task_definition" "model_task" {
  family                   = "${var.project_name}-model"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_task_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([{
    name  = "model-container",
    image = "<YOUR_ECS_MODEL_IMAGE>",
    portMappings = [{
      containerPort = 8080,
      hostPort      = 8080
    }]
  }])
}

# API Gateway with Cognito auth
resource "aws_apigatewayv2_api" "finance_api" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.finance_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.plaid_integration.invoke_arn
}

# Cognito user pool
resource "aws_cognito_user_pool" "users" {
  name = "${var.project_name}-user-pool"
}

# ElastiCache Redis for caching (inside VPC with subnet group)
resource "aws_elasticache_subnet_group" "redis" {
  name       = "${var.project_name}-redis-subnet-group"
  subnet_ids = aws_subnet.private[*].id
}

resource "aws_elasticache_cluster" "prediction_cache" {
  cluster_id           = "${var.project_name}-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis6.x"
  subnet_group_name    = aws_elasticache_subnet_group.redis.name
  security_group_ids   = [aws_security_group.redis.id]
}

