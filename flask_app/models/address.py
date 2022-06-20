from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
class Address:
    db = 'soloproject'
    def __init__ (self, data):
        self.id = data['id']
        self.street = data['street']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def new_address(cls, data):
        query = 'INSERT INTO addresses (street, city, state, zip, user_id) VALUES (%(street)s, %(city)s, %(state)s, %(zip)s, %(user_id)s)'
        connectToMySQL(Address.db).query_db(query, data)

    @staticmethod
    def validate_address(form):
        valid = True
        if len(form['street']) < 8:
            flash('Please enter a valid street address')
            valid = False
        if len(form['city']) < 3:
            flash('Please enter a valid city name')
            valid = False
        if len(form['state']) < 2:
            flash('Please enter valid state name')
            valid = False
        if len(form['zip']) < 5:
            flash('Please enter a valid zipcode number')
            valid = False
        return valid