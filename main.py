from datetime import time
from re import X
from flask import Flask, config, json, request, abort, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
import json
import asyncio
import os

from database_controller import DatabaseController
from error import ApiErrors
from longpolling_methods import getHashFromState

app = Flask(__name__, static_folder='../photodatabase/build/web')

LONG_POLLING_TIMING_SECONDS = 2

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
    if title.isspace:
        return ApiErrors.badArgumentsError.jsonify()
    return jsonify(db.folders.create(title=title, description=description))


@app.route('/api/folder/<id>', methods=['PATCH'])
def patchFolder(id):
    title = request.form.get('title')
    description = request.form.get('description')
    if not id.isnumeric:
        return ApiErrors.badArgumentsError.jsonify()
    return jsonify(db.folders.edit(id=id, title=title, description=description))


@app.route('/api/folder/<id>', methods=['DELETE'])
def deleteFolder(id):
    if not id.isnumeric:
        return ApiErrors.badArgumentsError.jsonify()
    db.folders.delete(id=id)
    return 

@app.route('/api/folder/<id>', methods=['GET'])
def getFolder(id):
    if not id.isnumeric:
        return ApiErrors.badArgumentsError.jsonify()
    return jsonify(db.folders.get(id=id))

@app.route('/api/folder/', methods=['GET'])
def getFolders():
    return jsonify(db.folders.getAll())

@app.route('/api/image/', methods=['GET'])
def getImage():
    return jsonify(db.image.getAll())

@app.route('/api/image/<id>', methods=['GET'])
def getImages(id):
    return jsonify(db.image.get(id=id))

@app.route('/api/image', methods=['POST'])
def postImage():
    image = request.files['file']
    title = request.form.get('title')
    description = request.form.get('description')
    folder_id = request.form.get('folder_id')
    if image.content_type.split('/')[0] == "image":
        return ApiErrors.badFileType.jsonify()
    filename = secure_filename(image.filename)
    path = "photos/" + filename
    image.save(path)
    create_image = db.images.create(title=title, description=description, path=path)
    if folder_id != 'null':
        db.linkImage(create_image['id'], folder_id)
    return jsonify(create_image)

@app.route('/api/image/<id>', methods=['PATCH'])
def patchImage(id):
    title = request.form.get('title')
    description = request.form.get('description')
    return jsonify(db.images.edit(id=id,title=title, description=description))

@app.route('/api/image/<id>', methods=['DELETE'])
def deleteImage(id):
    db.images.delete(id=id)
    return

@app.route('/api/image/<id>/link/<folder>', methods=['POST'])
def postLink(id, folder):
    return jsonify(db.images.addToFolder(image_id=id, folder_id=folder))

@app.route('/api/image/<id>/link/<folder>', methods=['DELETE'])
def deleteLink(id, folder):
    return jsonify(db.images.removeFromFolder(image_id=id, folder_id=folder))

@app.route('/api/union', methods=['GET'])
def getUnion():
    return jsonify(db.getUnion())

### Для LP снизу
# @app.route('/api/folder/<id>', methods=['GET'])
# def getFolder(id):
#     if not id.isnumeric:
#         return ApiErrors.badArgumentsError.jsonify()
#     return jsonify(db.folders.get(id=id))

# @app.route('/api/folder/', methods=['GET'])
# def getFolders():
#     return jsonify(db.folders.getAll())

# @app.route('/api/image/', methods=['GET'])
# def getImage():
#     return jsonify(db.image.getAll())

# @app.route('/api/image/<id>', methods=['GET'])
# def getImages(id):
#     return jsonify(db.image.get(id=id))

@app.route('/lp/union', methods=['GET'])
async def getUnionLongPolling():
    last_state_hash = request.form.get('last_state_hash')
    if (last_state_hash == None):
        output = db.getUnion()
        return jsonify({"state": output, "hash": getHashFromState(output)})
    else:
        output = db.getUnion()
        hash = getHashFromState(output)
        while last_state_hash == hash:
            await asyncio.sleep(LONG_POLLING_TIMING_SECONDS)
            output = db.getUnion()
            hash = getHashFromState(output)
        return jsonify({"state": output, "hash": getHashFromState(output)})
  

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
        'autocommit':True,
        'charset':'utf8mb4',
    }
    global db 
    db = DatabaseController(config)
    app.run(
        debug=False, 
        port=1117,
        # host='db-learning.ithub.ru',
        threaded=True,
    )
    del db

if __name__ == "__main__":
    main()