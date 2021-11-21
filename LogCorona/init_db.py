import os
from peewee import (PostgresqlDatabase, SqliteDatabase)
from config import ProductionConfig, TestingConfig


def get_db():
    if os.getenv('ENV') == 'ProductionConfig':
        return PostgresqlDatabase(
            ProductionConfig.DATABASE,
            host=ProductionConfig.HOST,
            user=ProductionConfig.USER,
            port=ProductionConfig.PORT,
            password=ProductionConfig.PASSWORD
        )
    else:
        return SqliteDatabase(TestingConfig.DATABASE)
