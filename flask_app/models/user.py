from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import address, message
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'soloproject'
    def __init__ (self, data):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.password = data['password']
        self.phone = data['phone']
        self.occupation = data['occupation']
        self.education = data['education']
        self.prifile_pic = data['profile_pic']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.address = None
        self.friend = None
        self.myrequests = None
        self.post = None
        self.chat = None
        self.chat_sender = None

    @classmethod
    def new_user(cls, data):
        query = 'INSERT INTO users (firstname, lastname, email, password) VALUES (%(firstname)s, %(lastname)s, %(email)s, %(password)s);'
        connectToMySQL(User.db).query_db(query, data)

    @classmethod
    def all_users(cls):
        query = 'select * from users'
        results = connectToMySQL(User.db).query_db(query)
        all_users = []
        for user in results:
            _user = cls(user)
            all_users.append(_user)
        return all_users

    @classmethod
    def update_user_info(cls, data):
        query = 'UPDATE users SET firstname =%(firstname)s, lastname =%(lastname)s, email = %(email)s, phone = %(phone)s, education = %(education)s, occupation = %(occupation)s WHERE users.id = %(id)s;'
        connectToMySQL(User.db).query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(User.db).query_db(query, data)
        if len(result) < 1:
            return None
        return cls(result[0])

    @classmethod
    def user_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(User.db).query_db(query, data)
        if len(result) < 1:
            return None
        user = cls(result[0])
        return user

    @classmethod
    def user_all_emails(cls):
        query = 'SELECT email FROM users;'
        results = connectToMySQL(User.db).query_db(query)
        all_emails = []
        for email in results:
            all_emails.append(email)
        return all_emails 
    
    @classmethod
    def user_profile(cls, data):
        query ='select * from users left join  addresses on users.id = addresses.user_id where users.id = %(id)s;'
        result = connectToMySQL(User.db).query_db(query, data)
        for user in result:
            user_instance = cls(user)
            data = {
                'id': user['addresses.id'],
                'street': user['street'],
                'city': user['city'],
                'state': user['state'],
                'zip': user['zip'],
                'user_id': user['user_id'],
                'created_at': user['addresses.created_at'],
                'updated_at': user['addresses.updated_at']
            }
            user_address = address.Address(data)
            user_instance.address = user_address
        return user_instance

    @classmethod
    def add_profile_pic(cls, data):
        query = 'UPDATE users SET profile_pic = %(profile_pic)s WHERE users.id = %(id)s'
        connectToMySQL(User.db).query_db(query, data)


    @classmethod
    def users_friend_list(cls, data):
        query = 'SELECT * FROM users LEFT JOIN friends ON users.id = friends.user_id LEFT JOIN users as users2 ON users2.id = friends.friend_id WHERE users2.id = %(id)s;'
        results = connectToMySQL(User.db).query_db(query, data)
        all_friends = []
        for friend in results:
            friend_instance = cls(friend)
            all_friends.append(friend_instance)
        return all_friends
    
    
    @classmethod
    def users_friend_requests(cls, data):
        query = 'SELECT * FROM users LEFT JOIN requests ON users.id = requests.user_id LEFT JOIN users as users2 ON users2.id = requests.friend_id WHERE users2.id = %(id)s;'
        results = connectToMySQL(User.db).query_db(query, data)
        
        all_requests = []
        for sender in results:
            request_sender_instance = cls(sender)
            all_requests.append(request_sender_instance)
        return all_requests

    @classmethod
    def user_chat(cls, data):
        query = 'select * from users left join messages on users.id = messages.user_id left join users as users2 on users2.id = messages.friend_id'
        results = connectToMySQL(User.db).query_db(query, data)
        my_chats = []
        for user in results:
            user_instance = cls(user)
            data = {
                'id' : user['users2.id'],
                'firstname' : user['users2.firstname'],
                'lastname' : user['users2.lastname'],
                'email' : user['users2.email'],
                'password' : user['users2.password'],
                'phone' : user['users2.phone'],
                'occupation': user['users2.occupation'],
                'education' : user['users2.education'],
                'profile_pic' : user['users2.profile_pic'],
                'created_at': user['users2.created_at'],
                'updated_at' : user['users2.updated_at']
            }

            dt = {
                'id' : user['messages.id'],
                'messsage' : user['messsage'],
                'user_id' : user['messages.user_id'],
                'friend_id' : user['friend_id'],
                'created_at' : user['messages.created_at'],
                'updated_at' : user['messages.updated_at'],
            }
            user_in_chat = User(data)
            user_instance.chat_sender = user_in_chat
            message_chat = message.Message(dt)
            user_instance.chat = message_chat
            my_chats.append(user_instance)
        return my_chats
    
        

    @classmethod
    def send_request(cls, data):
        query = 'insert into requests (user_id, friend_id) values (%(user_id)s, %(friend_id)s)'
        connectToMySQL(User.db).query_db(query, data)


    @classmethod
    def my_requests(cls, data):
        query = 'SELECT * FROM requests WHERE user_id = %(user_id)s and friend_id = %(friend_id)s;'
        results = connectToMySQL(User.db).query_db(query, data)
        requests = []
        for i in results:
            if len(requests)<0:
                return None
            requests.append(i['friend_id'])    
        return requests

    
    @classmethod
    def my_friends(cls, data):
        query = 'SELECT * FROM friends WHERE user_id = %(user_id)s and friend_id = %(friend_id)s;'
        results = connectToMySQL(User.db).query_db(query, data)
        friends = []
        for i in results:
            if len(friends)<0:
                return None
            friends.append(i['friend_id'])    
        return friends
    
    @classmethod
    def delete_request(cls, data):
        query = "DELETE FROM requests WHERE user_id = %(user_id)s AND friend_id = %(friend_id)s;"
        connectToMySQL(User.db).query_db(query, data)

    @classmethod
    def unfriend(cls, data):
        query = "DELETE FROM friends WHERE user_id = %(user_id)s AND friend_id = %(friend_id)s;"
        connectToMySQL(User.db).query_db(query, data)
    
    @classmethod
    def accept_request(cls, data):
        query = 'insert into friends (user_id, friend_id) values (%(user_id)s, %(friend_id)s)'
        connectToMySQL(User.db).query_db(query, data)

    @classmethod
    def search(cls, data):
        query = 'SELECT * FROM users WHERE firstname LIKE %(name)s OR lastname LIKE %(name)s OR concat(firstname and lastname) LIKE %(name)s;'
        results = connectToMySQL(User.db).query_db(query, data)
        print(results)
        search_results = []
        for user in results:
            _user = cls(user)
            search_results.append(_user)
        return search_results
        



    @staticmethod
    def user_validation(form):
        valid = True
        if len(form['firstname']) < 2:
            flash('Please enter a valid First Name', 'register')
            valid = False
        
        if len(form['lastname']) < 2:
            flash('Please enter a valid Last Name', 'register')
            valid = False
        
        if len(form['email']) < 1:
            flash('Email feild cannot be empty', 'register')
            valid = False
        
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid Email address', 'register')
            valid = False
        
        if len(form['password']) < 8 or len(form['password']) > 20:
            flash('Password must be 8 to 20 characters long', 'register')
            valid = False
        
        emailcheck = User.user_all_emails()
        emailcount = 0        
        for email in emailcheck:
            if form['email'] == email['email']:
                emailcount+=1
        if emailcount > 0:
            flash('Email is associated with an account already', 'register')
            valid = False
        
        if form['confirm-password'] != form['password']:
            flash('Passwords does not match', 'register')
            valid = False
        
        # checks for numbers in password
        numlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        numcount = 0
        for num in form['password']:
            for i in numlist:
                if i == num:
                    numcount+=1
        if numcount < 1:
            flash('Password must contain at least one number', 'register')
            valid = False
        #-----------ends here-----------

        # checks for upper case letters in password
        count = 0
        for i in form['password']:
            if i.isupper():
                count+=1
        if count < 1:
            flash('Password must contain at least one Upper case', 'register')
            valid = False
        return valid