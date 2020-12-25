from flask.json import jsonify
from encoder import JSONEncoder
from pymongo import MongoClient, cursor
from bson.objectid import ObjectId
from flask import Response


client = MongoClient("mongodb+srv://bekirsencan:Turtoise@cluster0.vfdtl.mongodb.net/PersonelAPP?retryWrites=true&w=majority")
current_database = client['PersonelAPP']

def checkUser_Username(username):
    for data in current_database["Profile"].find({'username':username}):
        result = JSONEncoder().encode(data)
        return Response(result,mimetype='application/json')

### GET REQUEST
def check_user(username,password):
    for data in current_database["Profile"].find({'$and':[{'username':username},{'password':password}]},{'_id':1}):
        return  get_profile(data["_id"]) 

def get_profile(objectid):
    for data in current_database["Profile"].aggregate([{'$match':{'_id':ObjectId(objectid)}},
                                              {'$lookup':{'from':"Job_Info",'localField':"_id",'foreignField':"_id",'as':"job_info"}},
                                              {'$lookup':{'from':"Contact",'localField':"_id",'foreignField':"_id",'as':"contact"}},
                                              {'$lookup':{'from':"Status",'localField':"_id",'foreignField':"_id",'as':"status"}},
                                              {'$lookup':{'from':"Social",'localField':"_id",'foreignField':"_id",'as':"social"}},
                                              {'$project':{'social._id':0}}]):
        result = JSONEncoder().encode(data)
        return Response(result,mimetype='application/json')
    
def onclick_profile(objectid):
    for data in current_database["Profile"].aggregate([{'$match':{'_id':ObjectId(objectid)}},
                                              {'$lookup':{'from':"Job_Info",'localField':"_id",'foreignField':"_id",'as':"job_info"}},
                                              {'$unwind':'$job_info'},
                                              {'$lookup':{'from':"Contact",'localField':"_id",'foreignField':"_id",'as':"contact"}},
                                              {'$unwind':'$contact'}
                                              ]):
        result = JSONEncoder().encode(data)
        return Response(result,mimetype='application/json')

def get_social(objectid):
    result = []
    for data in current_database["Social"].find({'_id':ObjectId(objectid)},{'_id':0}):
        result.append(data['social'][0])
        result.append(data['social'][1])
    return jsonify(result)


### POST REQUEST
def insert_profile(user_id,profile_picture_url,username,password,name_surname,gender,job_info,contact):
    current_database["Profile"].insert(
        {'user_id':user_id,
         'profile_picture_url':profile_picture_url,
         'username':username,
         'password':password,
         'name_surname':name_surname,
         'gender':gender}
        )
    for data in current_database["Profile"].find({'$and':[{'username':username},{'password':password}]},{'_id':1}):
        insert_job_info(
            data["_id"],
            job_info[0]['company_name'],
            job_info[0]['department_name'],
            job_info[0]['job'],
            job_info[0]['about'])
        insert_status(data["_id"])
        insert_social(data["_id"])
        insert_contact(
            data["_id"],
            contact[0]['email'],
            contact[0]['number']
            )
        return "200"

def insert_job_info(_id,company_name,department_name,job,about):
    current_database["Job_Info"].insert(
        {'_id':_id,
         'company_name':company_name,
         'department_name':department_name,
         'job':job,'about':about}
        )
    return "200"
    

def insert_contact(objectid,email,number):
    current_database["Contact"].insert(
        {
            '_id':objectid,
            'email':email,
            'number':number
        }  
    )
    return "200"

def insert_status(objectid):
    current_database["Status"].insert(
        {'_id':objectid,
         'status_name':"çevrimiçi",
         'status_color_code':'#008000'}
        )
    return "200"

def insert_social(objectid):
    current_database["Social"].insert(
        {
            '_id':objectid,
            'social':[
                {
                    'name':"twitter",
                    'site_url':"",
                    'image_url':""
                },
                {
                    'name':"linkedin",
                    "site_url":"",
                    'image_url':""
                }
            ]
        }
    )
    


### UPDATE REQUEST

def update_status(objectid,data):
    current_database["Status"].update({'_id':ObjectId(objectid)},{'$set':
        {'status_name':data["status_name"],
         'status_color_code':data["status_color_code"]
         }})
    return  "200"

def update_profile(objectid,data):
    current_database["Profile"].update({'_id':ObjectId(objectid)},{'$set':
        {'username':data["username"],
         'password':data["password"],
         'name_surname':data["name_surname"],
         'profile_picture_url':data["profile_picture_url"],
         }})
    current_database["Contact"].update({'_id':ObjectId(objectid)},{'$set':
        {'email':data["contact"][0]['email'],
         'number':data["contact"][0]['number']
         }})
    return  "200"

def update_job_info(objectid,data):
    current_database["Job_Info"].update({'_id':ObjectId(objectid)},{'$set':
        {'company_name':data["company_name"],
         'department_name':data["department_name"],
         'job':data["job"],
         'about':data["about"]
         }})
    return "200"

def update_social(objectid,data):
    current_database["Social"].update({'_id':ObjectId(objectid),'social.name':'twitter'},{
        '$set':{
            'social.$.site_url':data['social'][0]['site_url'],
            'social.$.image_url':data['social'][0]['image_url']
        }
    })
    current_database["Social"].update({'_id':ObjectId(objectid),'social.name':'linkedin'},{
        '$set':{
            'social.$.site_url':data['social'][1]['site_url'],
            'social.$.image_url':data['social'][1]['image_url']
        }
    })
    return "200"

### QUERY REQUEST
def query_by_department_name(department_name):
    cursor = current_database["Job_Info"].aggregate([{'$match':{'department_name':department_name}},
        {'$lookup':{'from':"Profile",'localField':"_id",'foreignField':"_id",'as':"profile"}},
        {'$unwind':'$profile'},
        {'$lookup':{'from':"Contact",'localField':"_id",'foreignField':"_id",'as':"contact"}},
        {'$unwind':'$contact'},
        {'$lookup':{'from':"Status",'localField':"_id",'foreignField':"_id",'as':"status"}},
        {'$unwind':'$status'}
        ])
    result = []
    for document in cursor:
        result.append(document)
    return Response(JSONEncoder().encode(result),mimetype='application/json')    


