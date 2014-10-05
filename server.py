from flask import Flask, render_template, request, abort
from decisions import decision

app = Flask(__name__)

# Pages
@app.route('/')
def home():
    abort(404)
    return render_template('index.html')

# API

# the only api call you'll ever need
# returns yes/no + weather and uber data
# GET /api/goto/?start_lat=<latitude>&start_lon=<longitude>&end_lat=<latitude>&end_lon=<longitude>
@app.route('/api/goto/')
def goto():
    params = request.args
    origin = (params['start_lat'], params['start_lon'])
    destination = (params['end_lat'], params['end_lon'])
    return decision(origin, destination)
    
@app.route('/api')
def api_description():
    return """
    GET /api/goto/?start_lat=<latitude>&start_lon=<longitude>&end_lat=<latitude>&end_lon=<longitude>
    """

if __name__ == '__main__':
    app.debug =True
    app.run()
