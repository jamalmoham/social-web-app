from flask_app import app
from flask import render_template, request, redirect, session, flash,url_for
from flask_app.models import post, comment 
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/jamal/OneDrive/Desktop/coding dojo/projectsAndAlgos/soloProject/flask_app/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():        
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
        'content': request.form['content'],
        'user_id' : session['user_id'],
        'file' : filename
    }
    if request.form['content'] or file:
        post.Post.new_post(data)
    return redirect('/home')

@app.route('/comment/<int:id>', methods = ['POST'])
def com(id):
    data = {
        'comment' : request.form['comment'],
        'user_id' : session['user_id'],
        'post_id' : id,
    }
    if request.form['comment']:
        comment.Comment.new_comment(data)
    return redirect('/home')

@app.route('/like/<int:id>')
def like(id):
    data = {
        'user_id' : session['user_id'],
        'id' : id,
        'post_id' : id
    }
    likers = post.Post.post_like(data)
    if not id in likers:
        post.Post.like_a_post(data)
    else:
        post.Post.unlike(data)
    return redirect('/home')