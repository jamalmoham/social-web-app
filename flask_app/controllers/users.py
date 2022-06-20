from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, post, message 
from flask_app.models.address import Address
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/jamal/OneDrive/Desktop/coding dojo/projectsAndAlgos/soloProject/flask_app/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bcrypt = Bcrypt(app)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/profile/pic', methods=['GET', 'POST'])
def upload_profile_pic():        
    file = request.files['file']
    filename = secure_filename(file.filename)
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        if file and allowed_file(file.filename):
            filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('saved')
    data = {
        'id' : session['user_id'],
        'profile_pic' : filename
    }
    if file:
        user.User.add_profile_pic(data)
    id = session['user_id']
    return redirect(f'/edit/profile/{int(id)}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/<int:id>')
def profile(id):
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'id' : id
    }
    feeds = post.Post.post_feed()
    profile = user.User.user_profile(data)
    requests = user.User.users_friend_requests(data)
    my_friends = user.User.users_friend_list(data)
    return render_template('profile.html', profile = profile, requests = requests, friends = my_friends, my_feeds = feeds )

@app.route('/register', methods =['POST'])
def register():
    if not user.User.user_validation(request.form):
        return redirect('/')
    pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'firstname' : request.form['firstname'],
        'lastname' : request.form['lastname'], 
        'email' : request.form['email'],
        'password' : pw
    }

    user.User.new_user(data)
    
    dt = {
        'email' : request.form['email']
    }
    user_id = user.User.get_user_by_email(dt)
    session['user_id'] = user_id.id
    id = session['user_id']
    return redirect(f'/profile/{int(id)}')

@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db:
        flash('Invalid email/password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid email/password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/home')


@app.route('/home')
def home():
    if not 'user_id' in session:
        return redirect('/')
    feeds = post.Post.post_feed()
    data = {
        "name" : ''
    }
    likes = post.Post.post_likes()
    results = user.User.search(data)
    return render_template('feeds.html', feeds = feeds,  results = results, posts_likes = likes)

@app.route('/search', methods = ['POST'])
def search():
    data = {
        "name" : request.form['search']
    }
    results = user.User.search(data)
    feeds = post.Post.post_feed()
    if len(feeds) == 0:
        return redirect('/')
    return render_template('feeds.html', feeds = feeds, results = results)

@app.route('/edit/profile/<int:id>')
def edit(id):
    data = {
        'id' : id
    }
    profile = user.User.user_profile(data)
    return render_template('edit_profile.html', profile = profile)

@app.route('/update/info', methods = ['POST'])
def update():
    data = {
        'firstname':request.form['firstname'],
        'lastname':request.form['lastname'],
        'email':request.form['email'],
        'phone':request.form['phone'],
        'education':request.form['education'],
        'occupation':request.form['occupation'],
        'id' : session['user_id']
    }
    user.User.update_user_info(data)
    id = session['user_id']
    return redirect(f'/edit/profile/{id}') 

@app.route('/messages/<int:id>')
def messages(id):
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'id':id
    }
    inbox = message.Message.inbox(data)
    users = user.User.all_users()
    return render_template('messages.html', inbox = inbox, users = users)

@app.route('/message/user', methods = ['POST'])
def message_user():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'message': request.form['message'],
        'user_id' : session['user_id'],
        'friend_id': request.form['id']
    }
    if request.form['message']:
        message.Message.new_message(data)
    ID = session['user_id']
    return redirect(f'/messages/{int(ID)}')

@app.route('/new/address', methods = ['POST'])
def address():
    id = session['user_id']
    if not Address.validate_address(request.form):
        return redirect(f'/edit/profile/{int(id)}')
    data = {
        'street' : request.form['street'],
        'city' : request.form['city'],
        'state' : request.form['state'],
        'zip' : request.form['zip'],
        'user_id' : session['user_id']
    }
    Address.new_address(data)
    return redirect(f'/profile/{int(id)}')

@app.route('/add/friend/<int:id>')
def add_friend(id):
    data = {
        'user_id' : session['user_id'],
        'friend_id' : id
    }
    # dt{
    #     'user_id' : ,
    #     'friend_id':
    # }
    requests = user.User.my_requests(data)
    my_friends = user.User.my_friends(data)
    if not session['user_id'] in requests:
        user.User.send_request(data)
    return redirect(f'/profile/{id}')

@app.route('/accept/<int:id>')
def accept(id):
    data = {
        'user_id':id,
        'friend_id' : session['user_id']
    }
    user.User.accept_request(data)
    user.User.delete_request(data)
    ID = session['user_id']
    return redirect(f'/profile/{int(ID)}')

@app.route('/remove/<int:id>')
def remove(id):
    data = {
        'user_id' : id,
        'friend_id' : session['user_id']
    }
    ID = session['user_id']
    user.User.unfriend(data)
    return redirect(f'/profile/{int(ID)}')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')