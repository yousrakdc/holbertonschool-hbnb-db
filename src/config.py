import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'hohohoitsasecret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'hohohoitsasecret')
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite://SQL/hbnb.db')

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///development.db')

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/hbnb_prod')

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'