from flask import jsonify

class ApiError:
    def __init__(self, message):
        self.message = message
    
    def jsonify(self):
        return jsonify({"error": self.message})

class ApiErrors:
    badArgumentsError = ApiError('Bad arguments. Check what you are sending to the server!')
    badFileType = ApiError('Bad data type. Are you sure you\'re sending a jpeg?')