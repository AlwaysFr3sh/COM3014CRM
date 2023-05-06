from pymongo import MongoClient
from bson.objectid import ObjectId
# from flask_login import LoginManager
# from flask_mongoengine import MongoEngine
# from datetime import datetime

db_name="authdb"
# When local mongodb databse is connected:
# db_host=f"mongodb://localhost:27017/"
# client=MongoClient(db_host)
# when docker container is running:
client = MongoClient(host="test_mongo",port=27017,username="root",password="password",authSource="admin")
db=client[db_name]


class User:
    def __init__(self, email,firstName,lastName,password,secQuestion,answer,ccode):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.secQuestion= secQuestion
        self.answer=answer
        self.ccode=ccode

    def save(self):
        users = db.User
        user_data = {
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'password': self.password,
            'secQuestion': self.secQuestion,
            'answer':self.answer,
            'ccode':self.ccode
        }
        user_id = users.insert_one(user_data).inserted_id
        return user_id

    @staticmethod
    def find_by_email(email):
        users = db.User
        user_data = users.find_one({'email': email})
        if user_data:
            user = User(user_data['email'], user_data['firstName'], 
                        user_data['lastName'], user_data['password'], 
                        user_data['secQuestion'],user_data['answer'] ,user_data['ccode'])
            return user
        else:
            return None
    @staticmethod
    def upPass(email,new_password):
        users=db.User
        users.update_one({"email": email}, {"$set": {"password": new_password}})
class Company:
    def __init__(self, cname, ccode,cinfo):
        self.cname = cname
        self.ccode = ccode
        self.cinfo = cinfo
        

    def save(self):
        companies = db.Company
        company_data = {
            'cname': self.cname,
            'ccode': self.ccode,
            'cinfo': self.cinfo,
            
            
        }
        company_id = companies.insert_one(company_data).inserted_id
        return company_id

    @staticmethod
    def find_by_ccode(user_id):
        companies = db.Company
        company_data = companies.find_one({'ccode':user_id})
        if company_data:
            company = Company(company_data['cname'], company_data['ccode'], company_data['cinfo'])
            return company
        else:
            return None