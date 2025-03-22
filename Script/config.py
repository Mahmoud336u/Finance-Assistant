import os

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_URL')
    SAGEMAKER_ENDPOINT = os.getenv('SAGEMAKER_ENDPOINT')
    KINESIS_STREAM_NAME = os.getenv('KINESIS_STREAM_NAME')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URL = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev.db')

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
