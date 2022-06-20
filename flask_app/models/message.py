from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from datetime import datetime
import math
class Message:
    db = 'soloproject'
    def __init__ (self, data):
        self.id = data['id']
        self.message = data['message']
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_sender = None
        self.user_friend = None
    
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def new_message(cls, data):
        query = 'INSERT INTO messages (message, user_id, friend_id) VALUES (%(message)s, %(user_id)s, %(friend_id)s )'
        connectToMySQL(Message.db).query_db(query, data)

    @classmethod
    def inbox(cls, data):
        query = 'SELECT * FROM users LEFT JOIN messages ON users.id = messages.user_id LEFT JOIN users as users2 ON users2.id = messages.friend_id WHERE users2.id = %(id)s ORDER BY messages.created_at DESC;'
        results = connectToMySQL(Message.db).query_db(query, data)
        # print('results', results)
        all_messages = []
        for message in results:
            message_instance = cls(message)
            data = {
                'id' : message['id'],
                'firstname' : message['firstname'],
                'lastname' : message['lastname'],
                'email' : message['email'],
                'password' : message['password'],
                'phone' : message['phone'],
                'occupation': message['occupation'],
                'education' : message['education'],
                'profile_pic' : message['profile_pic'],
                'created_at': message['created_at'],
                'updated_at' : message['updated_at']
            }
            sender = user.User(data)
            message_instance.user_sender = sender
            all_messages.append(message_instance)
        return all_messages
