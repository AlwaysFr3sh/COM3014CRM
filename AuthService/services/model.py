from pymongo import MongoClient
from bson.objectid import ObjectId
# from flask_login import LoginManager
# from flask_mongoengine import MongoEngine
# from datetime import datetime

db_name="authdb"
db_host=f"mongodb://localhost:27017/"
client = MongoClient(db_host)
db=client[db_name]

# class User(db.Document):
#     email = db.EmailField(required=True, unique=True)
#     password = db.StringField(required=True)
#     firstName = db.StringField(required=True)
#     secondName = db.StringField(required=True)
#     # secQuestion=db.StringField(required=True)
#     # created_at = db.DateTimeField(default=datetime.utcnow)

#     def to_json(self):
#         return {
#             "email":self.email,
#             "password":self.password,
#             "full_name":self.full_name,
#             # "secQuestion":self.secQuestion
#         }
        

# class Company(db.Document):
#     cname = db.StringField(required=True)
#     ccode = db.StringField(required=True,unique=True)
#     user_id = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)

#     def to_json(self):
#         return {
#             "cname":self.cname,
#             "ccode":self.ccode,
#             "user_id":self.user_id
#         }
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
                        user_data['secQuestion'], user_data['ccode'], 
                        user_data['answer'])
            return user
        else:
            return None

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