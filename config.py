import os
import re
class Config:
   '''
   General configuration parent class
   '''
   UPLOADED_PHOTOS_DEST ='app/static/photos'#specifies the destination where we want to store our Images. 
   MAIL_SERVER = 'smtp.googlemail.com'
   MAIL_PORT = 587
   MAIL_USE_TLS = True  
   MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
   MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")   
   SECRET_KEY = os.environ.get('SECRET_KEY')
  #  # simple mde  configurations
   SIMPLEMDE_JS_IIFE = True
   SIMPLEMDE_USE_CDN = True
   pass
class ProdConfig(Config) :
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    #     SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    '''
    Production  configuration child class of ABOVE

    Args:
        Config: The parent configuration class MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  with General configuration settings
    '''
    pass
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mikeywalked:practice@localhost/pitcha_test' 
class DevConfig(Config):
    '''
    Development  configuration child class of Config

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mikeywalked:practice@localhost/pitcha'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}

