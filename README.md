# AI-Driven Personal Finance Assistant

An AI-powered financial assistant that helps users track expenses, categorize transactions, and receive smart budgeting suggestions.

## Overview

This project provides an AI-driven system to help individuals manage their budgets. It includes features such as:
- **Transaction Categorization:** Automatically categorize expenses (Food, Rent, Entertainment, etc.).
- **Expense Tracking & Visualizations:** Interactive dashboards to visualize spending.
- **AI-Powered Budgeting Suggestions:** Personalized recommendations to optimize budgeting.
- **Data Integration:** Supports both Plaid API integration and CSV upload.

## Tech Stack

### Primary Stack
- **Frontend:** React, AWS S3, CloudFront
- **Backend:** AWS Lambda, API Gateway, RDS (PostgreSQL)
- **ML Models:** Hugging Face / OpenAI (fine-tuned)
- **Deployment:** AWS (Terraform)

### Alternative Scenario
For those exploring different architectures, an alternative stack is also described:
- **Frontend:** AWS Amplify, AWS Cognito, AWS Lex, Amazon Kendra, Amazon Polly
- **Backend:** ECS Fargate, API Gateway
- **Data Integration:** AWS Lambda (Plaid API), Amazon SQS
- **Data Storage:** Amazon S3, Amazon Aurora Serverless, Amazon DynamoDB
- **Data Processing:** AWS Glue, Amazon Athena, Apache Airflow (MWAA)
- **Machine Learning:** AWS SageMaker Pipelines, SageMaker Endpoints, Amazon Personalize (optional)
- **Streaming:** Amazon Kinesis, AWS Lambda
- **Security:** AWS IAM, AWS KMS, TLS/SSL
- **Monitoring:** Amazon CloudWatch, AWS X-Ray
- **Cost Optimization:** Auto-scaling, Spot Instances, S3 Intelligent-Tiering, VPC Endpoints, AWS Budgets, Cost Anomaly Detection
- **High Availability:** Route 53, S3 Cross-Region Replication, DynamoDB Global Tables
- **IaC:** AWS CDK or Terraform

> **Note:** Please refer to the [IaC README](IaC/README.md) for detailed instructions on provisioning the infrastructure.

## Getting Started

### Prerequisites

- **Git:** To clone the repository.
- **Python:** Ensure you have Python installed for running tests and scripts.
- **AWS CLI:** For deployment and infrastructure management (if using the AWS-based deployment).
- **Docker:** To build and run containerized environments.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Mahmoud336u/finance-assistant.git
   cd finance-assistant
