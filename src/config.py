import os
from abc import ABC

# Base configuration class with common settings
class Config:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')


# Development configuration inherits from Config
class DevelopmentConfig(Config):
    # Development-specific database URI, defaults to SQLite if not set
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///development.db")

    DEBUG = True  # Enable debug mode for development


# Testing configuration inherits from Config
class TestingConfig(Config):
    TESTING = True  # Enable testing mode

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Production configuration inherits from Config
class ProductionConfig(Config):
    # Production database URI, defaults to PostgreSQL if DATABASE_URL is set, otherwise local SQLite
    TESTING = False
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/hbnb_prod"
    )