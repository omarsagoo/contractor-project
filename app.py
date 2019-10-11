import os

from bson.objectid import ObjectId
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient
from datetime import datetime

host = os.environ.get('MONGODB_URI', 'mongodb://omarsagoo:makeschool2019@ds233268.mlab.com:33268/heroku_vjnrq1bv/?authSource=admin')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
dreams = db.dreams
users = db.users
comments = db.comments


app = Flask(__name__)

@app.route('/')
def index(): 
    """Return homepage."""
    read_dreams = dreams.find()
    # dream = dreams.find_one({'_id': ObjectId(dream_id)})
    # print(read_dreams['_id'])
    return render_template("dreams_index.html", dreams=read_dreams)

@app.route('/dreams/new')
def dreams_new():
    """create a new dream"""
    return render_template('dream_new.html', dream={}, title='New Dream')

@app.route('/dreams', methods=['POST'])
def dreams_submit():
    """Submit a new dream."""
    dream = {
        'title': request.form.get('title'),
        'body': request.form.get('body'),
        'tag': request.form.get('tag'),
        'created_at': datetime.now()
    }
    dream_id = dreams.insert_one(dream).inserted_id

    return redirect(url_for('dreams_show', dream_id=dream_id))

@app.route('/dreams/<dream_id>')
def dreams_show(dream_id):
    """Show a single playlist."""
    dream = dreams.find_one({'_id': ObjectId(dream_id)})
    dream_comments = comments.find({'dream_id': ObjectId(dream_id)})
    return render_template('dreams_show.html', dream=dream, comments=dream_comments)

@app.route('/dreams/<dream_id>/edit')
def dreams_edit(dream_id):
    """Show the edit form for a dream."""
    dream = dreams.find_one({'_id': ObjectId(dream_id)})
    return render_template('dreams_edit.html', dream=dream, title='Edit Dream')

@app.route('/dreams/<dream_id>', methods=['POST'])
def dreams_update(dream_id):
    """Submit an edited dream."""
    updated_dream = {
        'title': request.form.get('title'),
        'description': request.form.get('body'),
        'tag': request.form.get('tag')
    }
    dreams.update_one(
        {'_id': ObjectId(dream_id)},
        {'$set': updated_dream})
    return redirect(url_for('dreams_show', dream_id=dream_id))

@app.route('/dreams/<dream_id>/delete', methods=['POST'])
def dreams_delete(dream_id):
    """Delete one dream."""
    dreams.delete_one({'_id': ObjectId(dream_id)})
    return redirect(url_for('index'))

@app.route('/dreams/comments', methods=['POST'])
def dream_comment_new():
    ''' submit a comment for a dream'''
    comment = {
        'user': request.form.get('user'),
        'content': request.form.get('content'),
        'dream_id': ObjectId(request.form.get('dream_id'))
    }
    comment_id = comments.insert_one(comment).inserted_id

    return redirect(url_for('dreams_show', dream_id=request.form.get('dream_id')))

@app.route('/dreams/comments/<comment_id>')
def dream_delete_comment(comment_id):
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('dreams_show', dream_id=comment.get('dream_id')))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
