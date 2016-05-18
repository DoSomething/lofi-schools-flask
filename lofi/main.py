from flask import Flask, request, jsonify
try:
    from flask.ext.cors import CORS  # The typical way to import flask-cors
except ImportError:
    # Path hack allows examples to be run without installation.
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask.ext.cors import CORS

import json, os

app = Flask(__name__)

# Load configuration file lofi/config.py
app.config.from_object('config')

# Set CORS options on app configuration
app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/search*": {"origins": "*"}}
app.config['DEBUG'] = True

cors = CORS(app)

# override variables with config file from local config file
# if 'LOFI_CONFIG_FILE' in os.environ:
#     app.config.from_envvar('LOFI_CONFIG_FILE')

app.config['MONGODB_SETTINGS'] = {
  'DB': os.environ['LOFI_DB_NAME'],
  'USERNAME': os.environ['LOFI_DB_USERNAME'],
  'PASSWORD': os.environ['LOFI_DB_PASSWORD'],
  'HOST': os.environ['LOFI_DB_HOST'],
  'PORT': int(os.environ['LOFI_DB_PORT'])
}

from models import db, Location
db.init_app(app)

@app.route('/search', methods=['GET'])
def search():
    if 'query' not in request.args or not request.args['query']:
        return json.dumps({
            'meta': {
                'code': 400,
                'errorType': 'param_error',
                'errorDetail': 'Missing or empty query parameter'
            },
        }), 400

    limit = 10
    if 'limit' in request.args and request.args['limit'] and request.args['limit'].isdigit():
        limit = int(request.args['limit'])

    # Replacing whitespace with .* to offer more flexibility in what schools get
    # returned in the search. ex: If the query is "Belleville High School", we'd
    # still want it to return "Belleville Senior High School" as a result.
    name_regex = request.args['query'];
    name_regex = name_regex.replace(' ', '.*');

    query = {'name':{'$regex': '%s' % name_regex, '$options': 'i'}};

    if 'state' in request.args:
        query['state'] = request.args['state'];

    total_results = Location.objects(__raw__=query).count()
    locations = Location.objects(__raw__=query).limit(limit)
    results = []
    for location in locations:
        results.append(
            {
                'name': location.name,
                'street': location.street,
                'city': location.city,
                'state': location.state,
                'zip': location.zip,
                'lat': location.lat,
                'lon': location.lon,
                'country': location.country,
                'gsid': location.gsid
            }
        )

    return json.dumps({
        'meta': {
            'code': 200,
            'more_results': len(results) < total_results,
            'total_results': total_results
        },
        'results': results
    }), 200

port = os.environ.get('PORT', 5000)

if __name__ == '__main__':
    app.run(
        debug=True,
        port=int(port),
        host='0.0.0.0'
    )
