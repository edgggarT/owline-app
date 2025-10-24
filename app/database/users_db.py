from .connect_db import db_connect, db_close


class Users:
    def find_user(self, email: str, password: str) -> dict | None:

        conn = db_connect()

        if conn is None:
            return 'Error de conexion'

        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, email, password, name FROM users WHERE email = %s AND password = %s"

        try: 
            cursor.execute(query, (email, password))
            user_data = cursor.fetchone()

            if user_data:
                return user_data
            else:
                return None
        except Exception as e:
            print(f'Error al buscar usuario: {e}')
            return None
        finally:
            cursor.close()

    @staticmethod
    def find_user_by_id(id):
        conn = db_connect()
        if conn is None:
            return 'Error de conexion'
        
        cursor = conn.cursor(dictionary=True)
        query = 'SELECT id, email, password, name FROM users WHERE id = %s'
        try :
            cursor.execute(query, (id, ))
            user_data = cursor.fetchone()
            if user_data:
                return user_data
            else:
                return None
        except Exception as e:
            print(f'Error al buscar usuario: {e}')
            return None
        finally: 
            cursor.close()

    @staticmethod
    def update_user_db(id, updates):
        conn = db_connect()
        if conn is None:
            return 'Error de conexion'
        cursor = conn.cursor()

        dataKeys = []  
        dataValues = []

        for key, value in updates.items():
            dataKeys.append(f'{key} = %s')
            dataValues.append(value)

        dataValues.append(id)

        dataKeys_string = ", ".join(dataKeys)

        query = f"UPDATE users SET {dataKeys_string} WHERE id = %s"

        try:
            cursor.execute(query, tuple(dataValues))
            conn.commit()
            success = True
        except Exception as e:
            print(f'Error al actualizar: {e}')
            conn.rollback()
            success = False
        finally: 
            cursor.close()
            conn.close()

        return success

    @staticmethod
    def email_exists(email, current_user_id):
        conn = db_connect()
        if conn is None:
            return 'Error de conexion'
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id FROM users WHERE email = %s AND id != %s"
        cursor.execute(query, (email, current_user_id))
        exists = cursor.fetchone() is not None

        cursor.close()
        conn.close()
        return exists
    
    @staticmethod
    def email_exists_register(email):
        conn = db_connect()
        if conn is None:
            return 'Error de conexion'
        cursor = conn.cursor()

        query = "SELECT email FROM users WHERE email = %s"
        cursor.execute(query, (email, ))
        exists = cursor.fetchone() is None

        cursor.close()
        conn.close()
        return exists
    

    @staticmethod
    def user_register(name, email, password):
        conn = db_connect()
        if conn is None:
            return 'Error de conexion'
        
        cursor = conn.cursor()
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"

        try: 
            cursor.execute(query, (name, email, password))
            conn.commit()
            print(f'El usuario fue registrado: ', {name, email, password})
            return True
        except Exception as e:
            print(f'Error al registrar: {e}')
            conn.rollback()
            return False
        finally: 
            cursor.close()
            conn.close()

users_db = Users() 
