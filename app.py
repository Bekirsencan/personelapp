from flask import Flask,request,jsonify
from flask_restful import Api,Resource
import database

app = Flask(__name__)
api = Api(app)
user_id = 1

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

@app.route('/query/<string:objectid>/<int:arg>',methods=['GET'])
def query(objectid,arg):
    query_by_arg(arg,objectid)


@app.route('/register',methods=['POST'])
def register():
    global user_id
    user_id +=1
    data = request.get_json()
    return database.insert_profile(
        user_id,
        data['profile_picture_url'],
        data['username'],
        data['password'],
        data['name_surname'],
        data['gender'],
        data['job_info']
    )
    

@app.route('/update/<string:update_name>/<string:objectid>',methods=['POST'])
def udpate(update_name,objectid):
    data = request.get_json()
    return update_by_arg(update_name,objectid,data)


def update_by_arg(update_name,objectid,data):
    print("search çalıştı")
    switcher = {
        'status':lambda:database.update_status(objectid,data),
        'contact':lambda:database.update_contact(objectid,data),
        'profile':lambda:database.update_profile(objectid,data),
        'job_info':lambda:database.update_job_info(objectid,data)
        }
    return switcher.get(update_name,lambda:'Invalid')()

def query_by_arg(arg,object_id):
    switcher = {
        '0':lambda:database.query_by_status(object_id),
        '1':lambda:database.query_by_department_name(object_id)
        }
    return switcher.get(arg,lambda:'Invalid')()


if __name__ == "__main__":
    app.run(debug = True)