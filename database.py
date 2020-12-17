from encoder import JSONEncoder
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Response

client = MongoClient("mongodb+srv://bekirsencan:Turtoise@cluster0.vfdtl.mongodb.net/PersonelAPP?retryWrites=true&w=majority")
current_database = client['PersonelAPP']
profile_collection = current_database["Profile"]
job_info_collection = current_database["Job_Info"]
status_collection = current_database["Status"]
contact_collection = current_database["Contact"]

def checkUser_Username(username):
    for data in profile_collection.find({'username':username}):
        result = JSONEncoder().encode(data)
        return Response(result,mimetype='application/json')

### GET REQUEST
### Check if username and password exist
def check_user(username,password):
    for data in profile_collection.find({'$and':[{'username':username},{'password':password}]},{'_id':1}):
        return  get_profile(data["_id"]) 

### After login return profile and job_info from database 
def get_profile(objectid):
    
    for data in profile_collection.aggregate([{'$match':{'_id':ObjectId(objectid)}},
                                              {'$lookup':{'from':"Job_Info",'localField':"_id",'foreignField':"_id",'as':"Job_Info"}}]):
        result = JSONEncoder().encode(data)
        return Response(result,mimetype='application/json')
    
### When user click profile returns profile,job_info and contact from database
def onlick_profile(objectid):
    for data in profile_collection.aggregate([{'$match':{'_id':ObjectId(objectid)}},
                                              {'$lookup':{'from':"Job_Info",'localField':"_id",'foreignField':"_id",'as':"Job_Info"}},
                                              {'$lookup':{'from':"Contact",'localField':"_id",'foreignField':"_id",'as':"Contact"}}]):
        result = JSONEncoder().encode(data)
        return Response(result,mimetype='application/json')


### POST REQUEST
### When users tries to register create database collections 
def insert_profile(userid,profile_picture_url,username,password,name,surname,gender,job_info):
    profile_collection.insert(
        {'User_id':userid,
         'profile_picture_url':profile_picture_url,
         'username':username,
         'password':password,
         'name':name,
         'surname':surname,
         'gender':gender}
        )
    for data in profile_collection.find({'$and':[{'username':username},{'password':password}]},{'_id':1}):
        insert_job_info(
            data["_id"],
            job_info[0]['company_name'],
            job_info[0]['department_name'],
            job_info[0]['job'],
            job_info[0]['about'])
        insert_status(data["_id"])
        return 'Başarılı'

def insert_job_info(_id,company_name,department_name,job,about):
    job_info_collection.insert(
        {'_id':_id,
         'company_name':company_name,
         'department_name':department_name,
         'job':job,'about':about}
        )

def insert_status(objectid):
    status_collection.insert(
        {'_id':objectid,
         'status_name':"çevrimiçi",
         'status_color_code':'#008000'}
        )

### UPDATE REQUEST

def update_status(objectid,data):
    status_collection.update({'_id':ObjectId(objectid)},{'$set':
        {'status_name':data["status_name"],
         'status_color_code':data["status_color_code"]
         }})

def update_contact(objectid,data):
    print("update çalıştı")
    contact_collection.update({'_id':ObjectId(objectid)},{'$set':
        {'email':data["email"],
         'number':data["number"]
         }})

def update_profile(objectid,data):
    profile_collection.update({'_id':ObjectId(objectid)},{'$set':
        {'user_id':data["user_id"],
         'username':data["username"],
         'password':data["password"],
         'name':data["name"],
         'surname':data["surname"],
         'gender':data["gender"]
         }})

def update_job_info(objectid,data):
    job_info_collection.update({'_id':ObjectId(objectid)},{'$set':
        {'company_name':data["company_name"],
         'department_name':data["department_name"],
         'job':data["job"],
         'about':data["about"]
         }})