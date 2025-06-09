import os
from flask import Flask, request, render_template
from cnx import create_table, insert_test_data
from user import UserF
from task import Task

# Add rest full API
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        return {'message': 'POST request received'}


# Registrar recursos
api.add_resource(HelloWorld, '/api/hello')
api.add_resource(UserF, 
                '/api/users/<string:user_id>', 
                '/api/users/dni/<string:dni>',
                endpoint='user')
api.add_resource(Task, 
                '/api/tasks',
                '/api/tasks/<int:task_id>',
                '/api/users/<int:user_id>/tasks',
                endpoint='task')


# Verificar si la base de datos existe y crear tablas e insertar datos si es necesario
if not os.path.exists('database.db'):
    print("Creando base de datos y datos iniciales...")
    create_table()
    insert_test_data()
    print("Base de datos inicializada correctamente!")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return "<h1>POST hello world</h1>"
    else:
        name = 'alumno'
        return render_template("index.html", name=name)

@app.route("/tasks")
def list_tasks():
    status = request.args.get('status')
    task_instance = Task()
    result = task_instance.get()
    tasks = result[0].get('tasks', []) if isinstance(result, tuple) else []
    return render_template("tasks.html", tasks=tasks, status=status)

@app.route("/user_tasks", methods=["GET", "POST"])
def user_tasks():
    user_instance = UserF()
    # Obtener todos los usuarios para el dropdown
    all_users = user_instance.get_all()
    users = all_users[0] if isinstance(all_users, tuple) else []
    
    selected_user_id = request.args.get('user_id')
    tasks = []
    
    if selected_user_id:
        task_instance = Task()
        result = task_instance.get(user_id=int(selected_user_id))
        tasks = result[0].get('tasks', []) if isinstance(result, tuple) else []
    
    return render_template("user_tasks.html", users=users, tasks=tasks, selected_user_id=selected_user_id)

if __name__ == "__main__":
    app.run(debug=True)
