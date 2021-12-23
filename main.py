from flask import Flask, config, json, request, abort, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
import os

app = Flask(__name__, static_folder='../photodatabase/build/web')

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


# @app.route('/api/getFolders', methods=['GET'])
# def getFolders():
#     return jsonify(db.getFolders())

# @app.route('/api/createFolder', methods=['POST'])
# def createFolderAPI():
#     title = request.form.get('title')
#     description = request.form.get('description')
#     return jsonify(db.createFolder(title=title, description=description))

# @app.route('/api/getFolderById/<id>', methods=['GET'])
# def getFolderByIdAPI(id):
#     return jsonify(db.getFolderById(id=id))

# @app.route('/api/deleteFolder/', methods=['DELETE'])
# def removeFolderAPI():
#     id = request.form.get('id')
#     return jsonify(db.removeFolder(id))

# @app.route('/api/uploadImage', methods=['POST'])
# def uploadImageAPI():
#     file = request.files['file']
#     title = request.form.get('title')
#     description = request.form.get('description')
#     folder = request.form.get('folder_id')
#     filename = secure_filename(file.filename)
#     path = "photos/" + filename
#     file.save(path)
#     create_image = db.createImage(title=title, description=description, path=path)
#     if (folder != 'null'):
#         db.linkImage(create_image['id'], folder)
#     return jsonify(create_image)

# @app.route('/api/getImages', methods=['GET'])
# @app.route('/api/getImages.html', methods=['GET'])
# def getImagesAPI():
#     return jsonify(db.getImages())

# @app.route('/api/images/<id>', methods=['GET'])
# def showImageAPI(id):
#     return send_file(db.getImageById(id=id)['path'])

# @app.route('/api/getUnion', methods=['GET'])
# def getUnionAPI():
#     return jsonify(db.getUnion())



# @app.route('/getImagesByFolderId/<id>', methods=['GET'])
# def getImagesByFolderId(id):
#     return jsonify(db.getImagesByFolderId(folder_id=id))

# @app.route('/getLinkImage/<id>', methods=['GET'])
# def getLinkImageFromId(id):
#     return jsonify(db.getLinkFromId(link_id=id))

# @app.route('/getLinkImage', methods=['GET'])
# def getLinkImage():
#     image_id = request.form.get('image_id')
#     folder_id = request.form.get('folder_id')
#     return jsonify(db.getLinkImage(image_id=image_id, folder_id=folder_id))



    
# @app.route('/linkImage', methods=['POST'])
# def linkImage():
#     image_id = request.form.get('image_id')
#     folder_id = request.form.get('folder_id')
#     return jsonify(db.linkImages(image_id=image_id, folder_id=folder_id))

# @app.route('/removeLinkImage', methods=['DELETE'])
# def removeLinkImage():
#     id = request.form.get('id')
#     return jsonify(db.removeLinkImage(id=id))

# @app.route('/removeImage', methods=['POST'])
# def removeImage():
#     id = request.form.get('id')
#     return jsonify(db.removeLinkImage(id=id))
    


if __name__ == '__main__':
    global db 
    config = {
        'host': 'db-learning.ithub.ru',
        'user': '2p1s16',
        'password':'134-285-256',
        'database':'2p1s16',
        'autocommit':True,
        'charset':'utf8mb4',
    }
    # db = DatabaseController(config)

    app.run(debug=False, port=1116,host='db-learning.ithub.ru')
