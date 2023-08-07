from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import configparser
import pathlib

file_config = pathlib.Path(__file__).parent.joinpath("config.ini")

config = configparser.ConfigParser()
config.read(file_config)

username = config.get("DB", "user")
password = config.get("DB", "password")
domain = config.get("DB", "domain")
port = config.get("DB", "port")
db_name = config.get("DB", "db_name")

url = f"postgresql://{username}:{password}@{domain}:{port}/{db_name}"
Base = declarative_base()
engin = create_engine(url, echo=False)
DBSession = sessionmaker(bind=engin)
session = DBSession()