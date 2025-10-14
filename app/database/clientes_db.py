from .connect_db import db_connect, db_close



class Clientes: 

    @staticmethod
    def find_client_by_dni(dni):
        conn = db_connect()

        if conn is None:
            return 'Error de conexion'
        
        cursor = conn.cursor(dictionary=True)

        query = "SELECT nombre, apellido, telefono, dni, email, fecha_nacimiento, direccion_ciudad, direccion_calle, fecha_creacion FROM clientes WHERE dni = %s"

        try:
            cursor.execute(query, (dni, ))
            user_data = cursor.fetchone()

            if user_data:
                return user_data
            else:
                return None
        except Exception as e:
            print(f'Error al buscar al cliente: ', e)
            return None
        finally:
            cursor.close()

    @staticmethod
    def find_client_by_range(fecha_inicial, fecha_final):
        conn = db_connect()

        if conn is None:
            return 'Error de conexion'
        
        cursor = conn.cursor(dictionary=True)

        query = "SELECT nombre, apellido, telefono, dni, email, fecha_nacimiento, direccion_ciudad, direccion_calle, fecha_creacion FROM clientes WHERE fecha_creacion BETWEEN %s and %s"

        try:
            cursor.execute(query, (fecha_inicial, fecha_final))
            user_data = cursor.fetchall()

            if user_data:
                return user_data
            else:
                return None
        except Exception as e:
            print(f'Error al buscar al cliente: ', e)
            return None
        finally:
            cursor.close()

    @staticmethod
    def create_client(usuario_id ,nombre, apellido, email, telefono, dni, fecha_nacimiento, direccion_ciudad, direccion_calle):
        conn = db_connect()
        if conn is None:
            return 'Error de conexion'
        
        cursor = conn.cursor()
        user_query = f'SET @usuario_id = {usuario_id}'
        query = "INSERT INTO clientes (nombre, apellido, email, telefono, dni, fecha_nacimiento, direccion_ciudad, direccion_calle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        try:
            cursor.execute(user_query)
            cursor.execute(query, (nombre, apellido, email, telefono, dni, fecha_nacimiento, direccion_ciudad, direccion_calle))
            conn.commit()
            print(f'El usuario fue registrado: ', {nombre, apellido, email, telefono, dni, fecha_nacimiento, direccion_ciudad, direccion_calle})
            return True
        except Exception as e:
            print(f'Error al registrar: {e}')
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def email_exists(email):
        conn = db_connect()
        if conn is None:
            return 'Error de conexion'
        cursor = conn.cursor()

        query = "SELECT email FROM clientes WHERE email = %s"
        cursor.execute(query, (email, ))
        exists = cursor.fetchone() is not None

        cursor.close()
        conn.close()
        return exists
    
    @staticmethod
    def dni_exists(dni):
        conn = db_connect()
        if conn is None:
            return 'Error de conexion'
        cursor = conn.cursor()

        query = "SELECT dni FROM clientes WHERE dni = %s"
        cursor.execute(query, (dni, ))
        exists = cursor.fetchone() is not None

        cursor.close()
        conn.close()
        return exists
    
    @staticmethod
    def delete_client(usuario_id ,dni):
        conn = db_connect()

        if conn is None:
            return 'Error de conexion'
        
        cursor = conn.cursor()
        user_query = f'SET @usuario_id = {usuario_id}'
        query = 'DELETE FROM clientes WHERE dni = %s'

        try:
            cursor.execute(user_query)
            cursor.execute(query, (dni, ))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Cliente con DNI {dni} eliminado, filas afectadas: {cursor.rowcount}")
                return True
            else:
                print(f'No se encontro el DNI: {dni}')
                return False
        except Exception as e:
            print(f'Error al eliminar: {e}')
            return False
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def update_client_db(usuario_id ,dni, updates):
        conn = db_connect()
        if conn is None:
            return 'Error de conexion'
        cursor = conn.cursor()

        dataKeys = []  
        dataValues = []

        for key, value in updates.items():
            dataKeys.append(f'{key} = %s')
            dataValues.append(value)

        dataValues.append(dni)

        dataKeys_string = ", ".join(dataKeys)

        user_query = f'SET @usuario_id = {usuario_id}'
        query = f"UPDATE clientes SET {dataKeys_string} WHERE dni = %s"

        try:
            cursor.execute(user_query)
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
    def get_clients_logs():
        conn = db_connect()

        if not conn:
            return 'Error de conexion'
        
        cursor = conn.cursor(dictionary=True)

        query = 'SELECT log_id ,usuarioemail, accion, clientenombre, clienteapellido, fecha_accion FROM clientes_log'

        try:
            cursor.execute(query)
            logs = cursor.fetchall()
            
            if not logs:
                return 'No hay logs que mostrar'
            return logs
        except Exception as e:
            print(f'Error: {e}')

clientes_db = Clientes()