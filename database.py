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
user_id = 2

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
                                              {'$lookup':{'from':"Job_Info",'localField':"_id",'foreignField':"_id",'as':"job_info"}},
                                              {'$project':{
                                                  'job_info._id':0
                                              }}]):
        result = JSONEncoder().encode(data)
        return Response(result,mimetype='application/json')
    
### When user click profile returns profile,job_info and contact from database
def onclick_profile(objectid):
    for data in profile_collection.aggregate([{'$match':{'_id':ObjectId(objectid)}},
                                              {'$lookup':{'from':"Job_Info",'localField':"_id",'foreignField':"_id",'as':"job_info"}},
                                              {'$unwind':'$job_info'},
                                              {'$lookup':{'from':"Contact",'localField':"_id",'foreignField':"_id",'as':"contact"}},
                                              {'$unwind':'$contact'}
                                              ]):
        result = JSONEncoder().encode(data)
        return Response(result,mimetype='application/json')


### POST REQUEST
### When users tries to register create database collections 
def insert_profile(user_id,profile_picture_url,username,password,name_surname,gender,job_info):
    profile_collection.insert(
        {'user_id':user_id,
         'profile_picture_url':profile_picture_url,
         'username':username,
         'password':password,
         'name_surname':name_surname,
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
        insert_contact(data["_id"])
        return "200"

def insert_job_info(_id,company_name,department_name,job,about):
    job_info_collection.insert(
        {'_id':_id,
         'company_name':company_name,
         'department_name':department_name,
         'job':job,'about':about}
        )
    return "200"
    

def insert_contact(objectid):
    contact_collection.insert(
        {
            '_id':objectid,
            'email':"",
            'number':""
        }  
    )
    return "200"

def insert_status(objectid):
    status_collection.insert(
        {'_id':objectid,
         'status_name':"çevrimiçi",
         'status_color_code':'#008000'}
        )
    return "200"


### UPDATE REQUEST

def update_status(objectid,data):
    status_collection.update({'_id':ObjectId(objectid)},{'$set':
        {'status_name':data["status_name"],
         'status_color_code':data["status_color_code"]
         }})
    return  "200"

def update_contact(objectid,data):
    contact_collection.update({'_id':ObjectId(objectid)},{'$set':
        {'email':data["email"],
         'number':data["number"]
         }})
    return "200"

def update_profile(objectid,data):
    profile_collection.update({'_id':ObjectId(objectid)},{'$set':
        {'username':data["username"],
         'password':data["password"],
         'name_surname':data["name_surname"],
         'profile_picture_url':data["profile_picture_url"],
         }})
    return  "200"

def update_job_info(objectid,data):
    job_info_collection.update({'_id':ObjectId(objectid)},{'$set':
        {'company_name':data["company_name"],
         'department_name':data["department_name"],
         'job':data["job"],
         'about':data["about"]
         }})
    return "200"


    


