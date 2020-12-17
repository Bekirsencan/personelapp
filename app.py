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
    return database.check_user(username,password)

@app.route('/get_profile_api/<string:objectid>', methods = ['GET'])
def get_profile(objectid):
    return database.get_profile(objectid)

@app.route('/onclick_profile_api/<string:objectid>',methods = ['GET'])
def onclick_profile(objectid):
    return database.onlick_profile(objectid)

@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    return database.insert_profile(
        data['user_id'],
        data['profile_picture_url'],
        data['username'],
        data['password'],
        data['name'],
        data['surname'],
        data['gender'],
        data['Job_Info']
    )

@app.route('/update',methods=['POST'])
def udpate():
    data = request.get_json()
    search(data["update_name"],data)
    
def search(arg,data):
    print("search çalıştı")
    switcher = {
        'status':lambda:database.update_status(data["_id"],data),
        'contact':lambda:database.update_contact(data["_id"],data),
        'profile':lambda:database.update_profile(data["_id"],data),
        'job_info':lambda:database.update_job_info(data["_id"],data)
        }
    return switcher.get(arg,lambda:'Invalid')()


if __name__ == "__main__":
    app.run(debug = True)