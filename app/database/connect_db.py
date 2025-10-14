import mysql.connector
from mysql.connector import errorcode
from .config import Config

db_connection = None

def db_connect():
    global db_connection
    if db_connection is None or not db_connection.is_connected():
        try:
            db_connection = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_DATABASE
            )
            print('Conexion exitosa con la base de datos')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"Error DB: La base de datos '{Config.DB_DATABASE}' no existe.")
            else:
                print(f"Error de conexión DB: {err}")
            db_connection = None
    return db_connection    
    

def db_close(exception=None):
    global db_connection
    if db_connection is not None and db_connection.is_connected():
        db_connection.close()
        db_connection = None
