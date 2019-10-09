import os

from bson.objectid import ObjectId
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Dreams')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
dreams = db.dreams
comments = db.comments

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template("dreams_index.html", dreams=dreams)

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
        # 'created_at': datetime.now()
    }
    dream_id = dreams.insert_one(dream).inserted_id
    print(request.form.to_dict())

    return redirect(url_for('dreams_show', dream_id=dream_id))

@app.route('/dreams/<dream_id>')
def dreams_show(dream_id):
    """Show a single playlist."""
    dream = dreams.find_one({'_id': ObjectId(dream_id)})
    # playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    return render_template('dreams_show.html', dream=dream)

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
    return redirect(url_for('dreams_new'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
