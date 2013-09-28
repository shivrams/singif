from flask import Response, Blueprint
import simplejson
sample_response = {'status': 200, 'gifs': [{'url': 'http://media.giphy.com/media/fiMcQZFenlgFa/giphy.gif', 'loops': 8, 'style': 'center', 'ts': 0}, {'url': 'http://media.giphy.com/media/Jztx4VDq2wJBS/giphy.gif', 'loops': 4, 'style': 'center', 'ts': 14}, {'url': 'http://media.giphy.com/media/cr5u0ZEbQpVPG/giphy.gif', 'loops': -1, 'style': 'tile', 'ts': 21}], 'lines': [{'text': 'oh yeah', 'ts': 8}, {'text': 'such sweet lyrics', 'ts': 14}, {'text': 'time to gif it', 'ts': 21}], 'meta': {'original_url': 'https://www.youtube.com/watch?v=hroUeu4IvpE', 'title': 'blah'}, 'embed': '<iframe width="560" height="315" src="//www.youtube.com/watch?v=hroUeu4IvpE" frameborder="0" allowfullscreen></iframe>', 'mesg': 'success'}

mod = Blueprint('api', __name__)

@mod.route('/ping')
def ping():
    return 'pong!'

@mod.route('/api/v1/singif')
def singif_api():
    json_response = simplejson.dumps(sample_response)
    resp = Response(json_response, status=200, mimetype='application/json')
    resp.headers['X-Creator'] =  "W.A.S.T.E"
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

