from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, comment
from datetime import datetime
import math
class Post:
    db = 'soloproject'
    def __init__ (self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.file = data['file']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.comments = []
        self.likes = None
        self.num_comments = None

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
    def new_post(cls, data):
        query = 'INSERT INTO posts (content, user_id, file) VALUES (%(content)s, %(user_id)s, %(file)s)'
        connectToMySQL(Post.db).query_db(query, data)

    @classmethod
    def users_post(cls, data):
        query = 'SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE posts.id = %(id)s'
        results = connectToMySQL(Post.db).query_db(query, data)
        print(results)
        post_instance = cls(results[0])
        data = {
                'id' : results[0]['users.id'],
                'firstname' : results[0]['firstname'],
                'lastname' : results[0]['lastname'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'phone' : results[0]['phone'],
                'occupation': results[0]['occupation'],
                'education' : results[0]['education'],
                'profile_pic' : results[0]['profile_pic'],
                'created_at': results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
        }
        post_user = user.User(data)
        post_instance.user = post_user
        return post_instance

    @classmethod
    def update_post(cls, data):
        query = 'UPDATE posts SET content = %(content)s, file = %(file)s where posts.id = %(id)s'
        connectToMySQL(Post.db).query_db(query, data)

    @classmethod
    def like_a_post(cls, data):
        query = 'INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);'
        result = connectToMySQL(Post.db).query_db(query, data)
        return result

    @classmethod
    def post_like(cls, data):
        query = 'SELECT * FROM likes WHERE user_id = %(user_id)s and post_id = %(id)s;'
        results = connectToMySQL(Post.db).query_db(query, data)
        likes = []
        print(results)
        for i in results:
            if len(likes)<0:
                return None
            likes.append(i['post_id'])    
        return likes

    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND post_id = %(id)s;"
        connectToMySQL(Post.db).query_db(query, data)

    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE user_id = %(user_id)s AND posts.id = %(id)s;"
        connectToMySQL(Post.db).query_db(query, data)

    @classmethod
    def post_feed(cls):
        query = 'select * , count(likes.post_id) as likes, count(comment) as coms from posts left join likes on likes.post_id = posts.id left join  comments on posts.id = comments.post_id join users on users.id = posts.user_id group by posts.id order by posts.created_at desc'
        results = connectToMySQL(Post.db).query_db(query)
        all_posts = []
        for post in results:
            post_instance = cls(post)
            data = {
                'id' : post['users.id'],
                'firstname' : post['firstname'],
                'lastname' : post['lastname'],
                'email' : post['email'],
                'password' : post['password'],
                'phone' : post['phone'],
                'occupation': post['occupation'],
                'education' : post['education'],
                'profile_pic' : post['profile_pic'],
                'created_at': post['users.created_at'],
                'updated_at' : post['users.updated_at']
            }

            dt = {
                'id' : post['comments.id'],
                'comment' : post['comment'],
                'user_id' : post['comments.user_id'],
                'post_id' : post['post_id'],
                'created_at' : post['comments.created_at'],
                'updated_at' : post['comments.updated_at'],
            }
            
            post_instance.num_comments = post['coms']
            post_instance.likes = post['likes']
            the_user = user.User(data)
            post_instance.user = the_user
            the_comment = comment.Comment(dt)
            post_instance.comments.append(the_comment) 
            all_posts.append(post_instance)
        return all_posts

    @classmethod
    def post_likes(cls):
        query = 'SELECT *, count(likes.post_id) as likes from posts left join likes on likes.post_id = posts.id'
        results = connectToMySQL(Post.db).query_db(query)
        all_posts_and_likes = []
        for post in results:
            post_instance = cls(post)
            
            all_posts_and_likes.append(post_instance)
        return all_posts_and_likes