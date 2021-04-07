from flask import Flask, render_template, request, Response, flash, redirect
from flask_pymongo import PyMongo
from forms import LoginForm
from werkzeug.security import generate_password_hash
from bson.json_util import dumps
from bson import ObjectId
from forms import LoginForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['MONGO_URI']='mongodb://localhost:27017/bd_pymongo'
mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template('home.html')

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
        response = {
            'id': str(id),
            'username': username,
            'password': hashed_pass,
            'e-mail': email
        }
        return response
     
    return {'message': 'datos recibidos'}

@app.route("/users", methods=['GET'])
def list_users():
    cursor = mongo.db.users.find()
    message = dumps(cursor)
    return Response(message, mimetype='application/json')

@app.route("/users/<id>", methods=['GET'])
def usuario(id):
    user = mongo.db.users.find_one({'_id':ObjectId(id)})
    message = dumps(user)
    return Response(message, mimetype='application/json')  

@app.route("/users/<id>", methods=['DELETE'])
def borrar(id):
    user = mongo.db.users.delete_one({'_id':ObjectId(id)})
    message = '{"message":"user delete", "id":'+id+'}'
    return Response(message, mimetype='application/json')  

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
    message = dumps(user)   
    return Response(message, mimetype='application/json')

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
    app.run(host='0.0.0.0', port=3000, debug=True)
