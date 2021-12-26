import time
from re import X
from random import randint
from flask import Flask, config, json, request, abort, send_file, jsonify, render_template
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
import json
import asyncio
import os
from datetime import datetime

from database_controller import DatabaseController
from error import ApiErrors
from longpolling_methods import getHashFromState, longPolling

app = Flask(__name__, static_folder='../photodatabase/build/web')

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/api/folder', methods=['POST'])
def postFolder():
    title = request.form.get('title')
    description = request.form.get('description')
    if title.strip() == "":
        return ApiErrors.badArgumentsError.jsonify()
    return jsonify(db.folders.create(title=title, description=description))


@app.route('/api/folder/<id>/edit', methods=['POST'])
def patchFolder(id):
    title = request.form.get('title')
    description = request.form.get('description')
    if not id.isnumeric:
        return ApiErrors.badArgumentsError.jsonify()
    return jsonify(db.folders.edit(id=id, title=title, description=description))


@app.route('/api/folder/<id>/delete', methods=['POST'])
def deleteFolder(id):
    if not id.isnumeric:
        return ApiErrors.badArgumentsError.jsonify()
    return jsonify(db.folders.delete(id=id))

@app.route('/api/folder/<id>', methods=['GET'])
def getFolder(id):
    if not id.isnumeric:
        return ApiErrors.badArgumentsError.jsonify()
    return jsonify(db.folders.get(id=id))

@app.route('/api/folder/', methods=['GET'])
def getFolders():
    return jsonify(db.folders.getAll())

@app.route('/api/image/', methods=['GET'])
def getImages():
    return jsonify(db.images.getAll())

@app.route('/api/image/<id>', methods=['GET'])
def getImage(id):
    return jsonify(db.images.get(id=id))

@app.route('/api/image/<id>/show', methods=['GET'])
def getImageShow(id):
    return send_file(db.images.get(id)['path'], mimetype='image/jpg')

@app.route('/api/image/', methods=['POST'])
def postImage():
    image = request.files['file']
    title = request.form.get('title')
    description = request.form.get('description')
    # folder_id = request.form.get('folder_id')
    if image.content_type.split('/')[0] != "image":
        return ApiErrors.badFileType.jsonify()
    path = "photos/" + secure_filename(title + description + str(randint(1, 100000)) + str(datetime.now()))
    image.save(path)
    create_image = db.images.create(title=title, description=description, path=path)
    # if folder_id != 'null':
    #     db.linkImage(create_image['id'], folder_id)
    return jsonify(create_image)

@app.route('/api/image/<id>/edit', methods=['POST'])
def patchImage(id):
    title = request.form.get('title')
    description = request.form.get('description')
    return jsonify(db.images.edit(id=id,title=title, description=description))

@app.route('/api/image/<id>/delete', methods=['POST'])
def deleteImage(id):
    return jsonify(db.images.delete(id=id))

@app.route('/api/image/<id>/link/<folder>', methods=['POST'])
def postLink(id, folder):
    return jsonify(db.images.addToFolder(image_id=id, folder_id=folder))

# @app.route('/api/image/<id>/link/<folder>', methods=['DELETE'])
# def deleteLink(id, folder):
#     return jsonify(db.images.removeFromFolder(image_id=id, folder_id=folder))

@app.route('/api/union', methods=['GET'])
def getUnion():
    return jsonify(db.getUnion())

@app.route('/lp/union', methods=['GET'])
async def getUnionLongPolling():
    last_state_hash = request.args['last_state_hash']
    if (last_state_hash == None):
        output = db.getUnion()
        return jsonify({"state": output, "hash": getHashFromState(output)})
    else:
        return jsonify(longPolling(last_state_hash, db.getUnion))
  
@app.route('/lp/folder/<id>/', methods=['GET'])
async def getFolderLongPooling(id):
    if not id.isnumeric:
        return ApiErrors.badArgumentsError.jsonify()
    last_state_hash = request.args['last_state_hash']
    if (last_state_hash == None):
        output = db.folders.get(id=id)
        return jsonify({"state": output, "hash": getHashFromState(output)})
    else:
        return jsonify(longPolling(last_state_hash, db.folders.get, id=id))


@app.route('/lp/folder/', methods=['GET'])
async def getFoldersLongPooling():
    last_state_hash = request.args['last_state_hash']
    if (last_state_hash == None):
        output = db.folders.getAll()
        return jsonify({"state": output, "hash": getHashFromState(output)})
    else:
        return jsonify(longPolling(last_state_hash, db.folders.getAll))


@app.route('/lp/image/', methods=['GET'])
async def getImageLongPooling():
    last_state_hash = request.args['last_state_hash']
    if (last_state_hash == None):
        output = db.folders.getAll()
        return jsonify({"state": output, "hash": getHashFromState(output)})
    else:
        return jsonify(longPolling(last_state_hash, db.images.getAll))


@app.route('/lp/image/<id>/', methods=['GET'])
async def getImagesLongPooling(id):
    last_state_hash = request.args['last_state_hash']
    if (last_state_hash == None):
        output = db.image.get(id=id)
        return jsonify({"state": output, "hash": getHashFromState(output)})
    else:
        return jsonify(longPolling(last_state_hash, db.images.get, id=id))


@app.errorhandler(404)
def error404(error):
    print(error)
    print(404)
    return ApiErrors.notFound.jsonify()

@app.errorhandler(500)
async def error500(error):
    return ApiErrors.serverError.jsonify()

@app.after_request
async def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def main():
    app.config.from_file("config.json", load=json.load)
    __dbpassword = app.config.get("DBPASSWORD")
    if not __dbpassword:
        raise ValueError("Not found DBPASSWORD in config.json. Check README.MD!")
    config = {
        'host': 'db-learning.ithub.ru',
        'user': '2p1s16',
        'password':__dbpassword,
        'database':'2p1s16',
        'autocommit': True,
        'charset':'utf8mb4',
    }
    global db 
    db = DatabaseController(config)
    app.run(
        debug=True, 
        port=1116,
        # host='db-learning.ithub.ru',
        host='192.168.0.118',
        # host='192.168.1.71',
        # threaded=True,
    )

if __name__ == "__main__":
    main()