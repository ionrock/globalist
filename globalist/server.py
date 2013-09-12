import json
import bson
import bson.json_util

from flask import Flask, jsonify, url_for, request, make_response, g, redirect
from mgoquery import Parser, ParseException
from db import get_conn
from config import config


mgoparser = Parser()
db = get_conn()

app = Flask(__name__)


def bsonify(obj):
    resp = make_response(json.dumps(obj, default=bson.json_util.default))
    resp.headers['Content-Type'] = 'application/json'
    return resp


def abs_url_for(*args, **kw):
    tail = url_for(*args, **kw)
    return '%s%s' % (app.config['base_url'], tail)


@app.url_value_preprocessor
def find_mongo_object(endpoint, values):
    g.database = None
    if 'database' in values:
        g.database = db[values['database']]

    if 'collection' in values and g.database:
        g.collection = g.database[values['collection']]


@app.route('/')
def index():
    names = [
        abs_url_for('database', database=name) for name in db.database_names()
    ]
    return jsonify({
        'databases': names
    })


@app.route('/<database>/')
def database(database):
    names = [
        abs_url_for('collection', database=database, collection=name)
        for name in g.database.collection_names()
    ]
    return jsonify({
        'collections': names
    })


@app.route('/<database>/<collection>/')
def collection(database, collection):
    return jsonify({
        'number of docs': g.collection.count(),
        'actions': {
            'find': abs_url_for('find',
                                database=database,
                                collection=collection),
            'save': abs_url_for('save',
                                database=database,
                                collection=collection),
        }
    })


@app.route('/<database>/<collection>/find/')
def find(database, collection):
    query = mgoparser.parse(request.args.get('q', ''))
    result = list(g.collection.find(query))
    return bsonify({'result': result})


@app.route('/<database>/<collection>/save/')
def save(database, collection):
    if request.json:
        id = g.collection.save(request.json)
        return redirect(url_for('findone', q=id, **request.view_args))

    id = '51b8c8f77a58ec382663682d'
    return redirect(url_for('findone', q=id, **request.view_args))


@app.route('/<database>/<collection>/findone/<q>')
def findone(database, collection, q):
    try:
        query = mgoparser.parse(q)
    except ParseException:
        query = {'_id': bson.ObjectId(q)}

    return bsonify(g.collection.find_one(query))


if __name__ == '__main__':
    app.debug = True
    app.config.update(config)
    app.run()
