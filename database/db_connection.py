import sys

sys.dont_write_bytecode = True


import pymysql
import psycopg2
from config.db_config import DB_CONFIGS

def get_db_connection(db_key):
    config = DB_CONFIGS[db_key]
    try:
        if config["type"] == "postgresql":
            return psycopg2.connect(
                host=config["host"],user=config["user"],
                password=config["password"], dbname=config["database"],
                port=config["port"]
                
            )
        else:
            raise ValueError("Unsupported database type")
    except Exception as e:
        raise Exception(f"Error connecting to {db_key}: {e}")
    
    



