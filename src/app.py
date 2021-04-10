from flask import Flask, render_template, request, Response, flash, redirect, jsonify
from flask_pymongo import PyMongo
from forms import LoginForm
from werkzeug.security import generate_password_hash
from bson.json_util import dumps
from bson import ObjectId
from forms import LoginForm
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
app.config['MONGO_URI']='mongodb://localhost:27017/bd_pymongo'
mongo = PyMongo(app)
CORS(app)

@app.route("/")
def home():
    return render_template('home.html')

# ruta para crear usuario nuevo

@app.route("/users", methods=['POST'])
def create_user():
    print(request.json)
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
   
    if username and password and email:
        hashed_pass= generate_password_hash(password)
        id = mongo.db.users.insert(
            {
                'username': username,
                'password': hashed_pass,
                'e-mail': email
            }
        )
        response = jsonify({
            '_id': str(id),
            'username': username,
            'password': hashed_pass,
            'email': email }
        )
        print(str(id))
        return response
    response = jsonify(message="Simple server is running") 
    return Response(response, mimetype='application/json')

# ruta para solicitar listado de usuarios
@app.route("/users", methods=['GET'])
def list_users():
    cursor = mongo.db.users.find()
    response = dumps(cursor)
    return Response(response, mimetype='application/json') 

# ruta para solicitar un usuario por id
@app.route("/users/<id>", methods=['GET'])
def usuario(id):
    user = mongo.db.users.find_one({'_id':ObjectId(id)})
    response = dumps(user)
    return Response(response, mimetype='application/json')  

# ruta para eliminar un usuario por id
@app.route("/users/<id>", methods=['DELETE'])
def borrar(id):
    response = mongo.db.users.find_one({'_id':ObjectId(id)})
    user = mongo.db.users.delete_one({'_id':ObjectId(id)})
    response = dumps(response)
    return Response(response, mimetype='application/json') 

# ruta para listar un usuario especifico por id
@app.route("/user/<id>", methods=['GET'])
def listarid(id):
    response = mongo.db.users.find_one({'_id':ObjectId(id)})
    response = dumps(response)
    return Response(response, mimetype='application/json')

# ruta para actualizar un usuario especifico por id
@app.route("/users/<id>", methods=['PUT'])
def actualizar(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    if username and password and email:
        hashed_pass= generate_password_hash(password)
        mongo.db.users.update_one({'_id':ObjectId(id)},{'$set':{
                'username': username,
                'password': hashed_pass,
                'e-mail': email}})
    user = mongo.db.users.find_one({'_id':ObjectId(id)})
    response = dumps(user)   
    return Response(response, mimetype='application/json')

# ruta para correr localmente un formulario de entrada de usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        username = form.username.data 
        password = form.password.data
        email = form.email.data
        if username and password and email:
            hashed_pass= generate_password_hash(password)
            id = mongo.db.users.insert(
                {
                    'username': username,
                    'password': hashed_pass,
                    'e-mail': email
                }
            )
            response = {
                'id': str(id),
                'username': username,
                'password': hashed_pass,
                'e-mail': email
            }
            #return response
   
        return redirect('/users')
    return render_template('login.html', title='Sign In', form=form)    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
