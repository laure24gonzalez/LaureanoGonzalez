from flask import jsonify
from flask_restful import Resource
from sqlite3 import Error
from cnx import create_connection

class UserF(Resource):
    def __init__(self):
        self.conn = create_connection()

    def get_all(self):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM users')
                rows = cursor.fetchall()
                users = []
                for row in rows:
                    users.append({
                        'id': row[0],
                        'nombre': row[1],
                        'apellido': row[2],
                        'direccion': row[3],
                        'dni': row[4]
                    })
                return users, 200
            except Error as e:
                return {'error': str(e)}, 500
            finally:
                self.conn.close()
        return {'error': 'Error de conexión a la base de datos'}, 500

    def get(self, user_id=None, dni=None):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                if dni:
                    cursor.execute('SELECT * FROM users WHERE dni = ?', (dni,))
                if user_id:
                    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'nombre': row[1],
                        'apellido': row[2],
                        'direccion': row[3],
                        'dni': row[4]
                    }, 200
                return {'error': 'No se encontraron datos'}, 404
            except Error as e:
                return {'error': str(e)}, 500
            finally:
                self.conn.close()
        return {'error': 'Error de conexión a la base de datos'}, 500