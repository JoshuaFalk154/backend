from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Auf der Suche nach der verlorenen Zeit ',
        'author': 'Marcel Proust ',
        'jahr': 'Zwischen 1913 und 1927'

    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Ulysses ',
        'author': 'James Joyce',
        'jahr': '1922'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Don Quijote',
        'author': 'Miguel de Cervantes',
        'jahr': '1605 und 1615'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Hundert Jahre Einsamkeit ',
        'author': 'Gabriel Garcia Marquez',
        'jahr': '1967'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Der große Gatsb',
        'author': 'F. Scott Fitzgerald',
        'jahr': '1925'
    },
]


# Anfrage von den entsprechenden Path .../books aus frontend
@app.route('/books', methods=['GET', 'POST'])
def all_books():
    global BOOKS
    response_object = {'status': 'success'}
    if request.method == 'POST':
        # Code zum Hinzufügen eines Buches zum Backend
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'jahr': post_data.get('jahr')
        })
        response_object['message'] = 'Book added!'
    else:
        sort_by = request.args.get('sortBy')  # 'title' oder 'author'
        if sort_by == 'author':
            BOOKS.sort(key=lambda x: x['author'])
        else:
            BOOKS.sort(key=lambda x: x['title'])
        response_object['books'] = BOOKS
    
    return jsonify(response_object)





#DELETE-Anfrage
@app.route('/books/<book_id>', methods=['DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False








