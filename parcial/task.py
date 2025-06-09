from flask import jsonify, request
from flask_restful import Resource, reqparse
from sqlite3 import Error
from cnx import create_connection

class Task(Resource):
    def __init__(self):
        self.conn = create_connection()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, required=True)
        self.parser.add_argument('description', type=str)
        self.parser.add_argument('user_id', type=int, required=True)
        self.parser.add_argument('status', type=str, default='pending')

    def get(self, task_id=None, user_id=None):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                status = request.args.get('status')  # Obtener el estado del query parameter
                
                if task_id:
                    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
                    row = cursor.fetchone()
                    if row:
                        return {
                            'id': row[0],
                            'title': row[1],
                            'description': row[2],
                            'user_id': row[3],
                            'status': row[4]
                        }, 200
                    return {'error': 'Tarea no encontrada'}, 404
                
                # Construir la consulta base
                query = 'SELECT * FROM tasks'
                params = []
                conditions = []
                
                # Agregar condición de usuario si existe
                if user_id:
                    conditions.append('user_id = ?')
                    params.append(user_id)
                
                # Agregar condición de estado si existe
                if status:
                    conditions.append('status = ?')
                    params.append(status)
                
                # Agregar las condiciones a la consulta
                if conditions:
                    query += ' WHERE ' + ' AND '.join(conditions)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                tasks = []
                for row in rows:
                    tasks.append({
                        'id': row[0],
                        'title': row[1],
                        'description': row[2],
                        'user_id': row[3],
                        'status': row[4]
                    })
                
                if not tasks and (user_id or status):
                    message = []
                    if user_id:
                        message.append('usuario')
                    if status:
                        message.append('estado')
                    return {'message': f'No se encontraron tareas para el {" y ".join(message)} especificado'}, 404
                
                return {'tasks': tasks}, 200
            except Error as e:
                return {'error': str(e)}, 500
            finally:
                self.conn.close()
        return {'error': 'Error de conexión a la base de datos'}, 500

    def post(self):
        args = self.parser.parse_args()
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO tasks (title, description, user_id, status)
                    VALUES (?, ?, ?, ?)
                ''', (args['title'], args['description'], args['user_id'], args['status']))
                self.conn.commit()
                return {'message': 'Tarea creada exitosamente', 'task_id': cursor.lastrowid}, 201
            except Error as e:
                return {'error': str(e)}, 500
            finally:
                self.conn.close()
        return {'error': 'Error de conexión a la base de datos'}, 500
