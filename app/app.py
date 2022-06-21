import os
from flask import Flask, jsonify, make_response, request, abort
import serverless_wsgi
from ethnic import *
import jwt

# create and configure the app
app = Flask(__name__)

@app.route("/")
def hello_from_root():
    if not 'authorization' in request.headers:
        abort(401)  
    user = None
    data = request.headers['authorization']
    try:
        token = str.replace(str(data), 'Bearer ','')
        user = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
    except:
        abort(401)
    
    return jsonify(
            {   
                "user": user,
                "message": 'Hello from root!'
            })

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

@app.route('/analyze', methods=['POST'])
def analyze_batch():
    if not 'authorization' in request.headers:
        abort(401)  
    user = None
    data = request.headers['authorization']
    try:
        token = str.replace(str(data), 'Bearer ','')
        user = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
    except:
        abort(401)
        
    try: 
        content = request.json
        names = content["names"]
        results = []
    
        results = infer_from_batch_input(names)

        return jsonify(
            {   
                "user": user,
                "uuid": content["uuid"],
                "names": results
            })
    except Exception as e:
        return {
            'error': f"{type(e).__name__}:{e}"
        }

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)