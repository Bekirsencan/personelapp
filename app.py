from flask import Flask,request,jsonify
from flask_restful import Api,Resource
import database

app = Flask(__name__)
api = Api(app)

@app.route('/login_api/<string:username>', methods = ['GET'])
def login2(username):
     return database.checkUser_Username(username)

@app.route('/login_api/<string:username>/<string:password>', methods = ['GET'])
def login(username,password):
     return database.checkUser(username,password)

@app.route('/get_profile_api/<string:objectid>', methods = ['GET'])
def get_profile(objectid):
    return database.getProfile(objectid)

@app.route('/onclick_profile_api/<string:objectid>',methods = ['GET'])
def onclick_profile(objectid):
    return database.onlick_profile(objectid)
    
if __name__ == "__main__":
    app.run(debug = True)