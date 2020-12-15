from encoder import JSONEncoder
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify,json

client = MongoClient("mongodb+srv://bekirsencan:Turtoise@cluster0.vfdtl.mongodb.net/PersonelAPP?retryWrites=true&w=majority")
current_database = client['PersonelAPP']
profile_collection = current_database["Profile"]
job_info_collection = current_database["Job_Info"]

def checkUser_Username(username):
    for data in profile_collection.find({'Username':username}):
        result = JSONEncoder().encode(data)
        return result
def checkUser(username,password):
    for data in profile_collection.find({'$and':[{'Username':username},{'Password':password}]}):
        result = JSONEncoder().encode(data)
        return result

def getProfile(objectid):
    
    for data in profile_collection.aggregate([{'$match':{'_id':ObjectId(objectid)}},
                                              {'$lookup':{'from':"Job_Info",'localField':"_id",'foreignField':"_id",'as':"Job_Info"}}]):
        result = JSONEncoder().encode(data)
        return jsonify(result)
    

def onlick_profile(objectid):
    for data in profile_collection.aggregate([{'$match':{'_id':ObjectId(objectid)}},
                                              {'$lookup':{'from':"Job_Info",'localField':"_id",'foreignField':"_id",'as':"Job_Info"}},
                                              {'$lookup':{'from':"Contact",'localField':"_id",'foreignField':"_id",'as':"Contact"}}]):
        result = JSONEncoder().encode(data)
        return result

def insertProfile(userid,profile_picture_url,username,password,name,surname,gender,job_info):
    profile_collection.insert({'User_id':userid,'Profile_picture_url':profile_picture_url,'Username':username,'Password':password,'Name':name,'Surname':surname,'Gender':gender})
    for data in profile_collection.find({'$and':[{'Username':username},{'Password':password}]},{'_id':1}):
        insert_Job_Info(data["_id"],job_info[0]['company_name'],job_info[0]['department_name'],job_info[0]['job'],job_info[0]['about'])
        return 'Başarılı'

def insert_Job_Info(_id,company_name,department_name,job,about):
    job_info_collection.insert({'_id':_id,'company_name':company_name,'department_name':department_name,'job':job,'about':about})