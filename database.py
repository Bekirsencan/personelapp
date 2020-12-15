from encoder import JSONEncoder
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://bekirsencan:Turtoise@cluster0.vfdtl.mongodb.net/PersonelAPP?retryWrites=true&w=majority")
current_database = client['PersonelAPP']
profile_collection = current_database["Profile"]

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
        return result
    

def onlick_profile(objectid):
    for data in profile_collection.aggregate([{'$match':{'_id':ObjectId(objectid)}},
                                              {'$lookup':{'from':"Job_Info",'localField':"_id",'foreignField':"_id",'as':"Job_Info"}},
                                              {'$lookup':{'from':"Contact",'localField':"_id",'foreignField':"_id",'as':"Contact"}}]):
        result = JSONEncoder().encode(data)
        return result