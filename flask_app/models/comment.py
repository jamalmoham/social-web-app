from flask_app.config.mysqlconnection import connectToMySQL
class Comment:
    db = 'soloproject'
    def __init__ (self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def new_comment(cls, data):
        query = 'INSERT INTO comments (comment, user_id, post_id) VALUES (%(comment)s, %(user_id)s, %(post_id)s)'
        connectToMySQL(Comment.db).query_db(query, data)
    
