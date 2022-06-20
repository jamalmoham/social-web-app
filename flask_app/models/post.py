from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, comment
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

    @classmethod
    def new_post(cls, data):
        query = 'INSERT INTO posts (content, user_id, file) VALUES (%(content)s, %(user_id)s, %(file)s)'
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
            print(post_instance.user.prifile_pic)
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