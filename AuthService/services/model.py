from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

class User:
    def __init__(self, email, first_name, last_name, password, sec_question, answer):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.sec_question = sec_question
        self.answer = answer

    def save(self):
        users = db['users']
        user_data = {
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'password': self.password,
            'secQuestion': self.sec_question,
            'answer': self.answer
        }
        result = users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def get_user_by_email(email):
        users = db['users']
        user_data = users.find_one({'email': email})
        if user_data:
            return User(
                email=user_data['email'],
                first_name=user_data['firstName'],
                last_name=user_data['lastName'],
                password=user_data['password'],
                sec_question=user_data['secQuestion'],
                answer=user_data['answer']
            )
        return None