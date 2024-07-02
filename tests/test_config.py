import os
import unittest
from dotenv import load_dotenv

# Assuming the config file is named config.py and resides in the same directory
from src.config import Config, DevelopmentConfig, ProductionConfig, TestingConfig


class TestConfig(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(os.path.join(basedir, '../.env'))

    def test_default_config(self):
        # Unset DATABASE_URL to test default value
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
        config = Config()
        self.assertFalse(config.DEBUG)
        self.assertFalse(config.TESTING)
        self.assertFalse(config.SQLALCHEMY_TRACK_MODIFICATIONS)
        self.assertEqual(config.SECRET_KEY, os.getenv('SECRET_KEY', 'hohohoitsasecret'))
        self.assertEqual(config.JWT_SECRET_KEY, os.getenv('JWT_SECRET_KEY', 'hohohoitsasecret'))
        self.assertEqual(config.JWT_ACCESS_TOKEN_EXPIRES, 3600)
        self.assertEqual(config.DATABASE_URL, 'sqlite:///hbnb_dev.db')

    def test_development_config(self):
        # Unset DATABASE_URL to test default value
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
        config = DevelopmentConfig()
        self.assertTrue(config.DEBUG)
        self.assertEqual(config.DATABASE_URL, 'sqlite:///development.db')

    def test_production_config(self):
        # Unset DATABASE_URL to test default value
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
        config = ProductionConfig()
        self.assertFalse(config.DEBUG)
        self.assertEqual(config.DATABASE_URL, 'postgresql://user:password@localhost/hbnb_prod')

    def test_testing_config(self):
        # Unset DATABASE_URL to test default value
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
        config = TestingConfig()
        self.assertTrue(config.TESTING)
        self.assertEqual(config.DATABASE_URL, 'sqlite:///:memory:')

if __name__ == '__main__':
    unittest.main()
