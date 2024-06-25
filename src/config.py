import os

# Base configuration class with common settings
class Config:
    DEBUG = False  # Debug mode disabled by default
    TESTING = False  # Testing mode disabled by default

    # Default database URI, using SQLite if DATABASE_URL environment variable is not set
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hbnb_dev.db")

    # Disable SQLAlchemy modification tracking for improved performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost/hbnb_prod"
    )
