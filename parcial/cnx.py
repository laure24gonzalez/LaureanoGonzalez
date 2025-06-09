import sqlite3
from sqlite3 import Error
from faker import Faker
import random

# Inicializar Faker con localización en español
fake = Faker(['es_ES'])

# Función para crear la conexión con la base de datos
def create_connection():
    try:
        conn = sqlite3.connect('database.db')
        return conn
    except Error as e:
        print(e)
    return None

# Función para crear la tabla si no existe
def create_table():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    dni TEXT NOT NULL
                )
            ''')
            
            # Agregar la creación de la tabla tasks
            sql_create_tasks_table = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                user_id INTEGER,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
            cursor.execute(sql_create_tasks_table)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()
            
# Función para insertar datos de prueba
def insert_test_data():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Insertar 10 usuarios aleatorios
            for _ in range(10):
                cursor.execute('''
                    INSERT INTO users (nombre, apellido, direccion, dni)
                    VALUES (?, ?, ?, ?)
                ''', (
                    fake.first_name(),
                    fake.last_name(),
                    fake.street_address(),
                    fake.unique.random_number(digits=8, fix_len=True)
                ))
                user_id = cursor.lastrowid
                
                # Insertar 3 tareas aleatorias para cada usuario
                for _ in range(3):
                    cursor.execute('''
                        INSERT INTO tasks (title, description, user_id, status)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        fake.sentence(nb_words=4),
                        fake.text(max_nb_chars=200),
                        user_id,
                        random.choice(['pending', 'in_progress', 'completed'])
                    ))
            
            conn.commit()
            print("Datos de prueba insertados correctamente!")
        except Error as e:
            print(f"Error al insertar datos de prueba: {e}")
        finally:
            conn.close()