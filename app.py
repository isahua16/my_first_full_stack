from dbhelpers import run_statement
from dbcreds import production_mode
from apihelpers import check_data
from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.get('/api/candy')
def get_candy():
    results = run_statement('call get_candy()')
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)

@app.post('/api/candy')
def post_candy():
    error = check_data(request.json, ['name', 'image_url', 'description'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call post_candy(?,?,?)', [request.json.get('name'), request.json.get('image_url'), request.json.get('description')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)
    
@app.delete('/api/candy')
def delete_candy():
    error = check_data(request.json, ['id'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call delete_candy(?)', [request.json.get('id')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)

if(production_mode == True):
    print('Running in production mode')
    import bjoern # type: ignore
    bjoern.run(app, '0.0.0.0', 5000)
else:
    print('Running in development mode')
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
    CORS(app)
