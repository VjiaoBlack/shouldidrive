from flask import Flask, render_template, request, abort, redirect
from decisions import decision

app = Flask(__name__)
app.debug = True


# Pages
@app.route('/')
def home():
    return render_template('index.html')

# API

# the only api call you'll ever need
# returns yes/no + weather and uber data
# GET /api/goto.json/?start_lat=<latitude>&start_lon=<longitude>&end_lat=<latitude>&end_lon=<longitude>
@app.route('/api/goto.json/')
def goto():
    params = request.args
    origin = (params['start_lat'], params['start_lon'])
    destination = (params['end_lat'], params['end_lon'])
    hurry = params['hurry'] == 'true'
    return decision(origin, destination, hurry)
    
@app.route('/api/')
def api_description():
    return render_template('docs.html')

if __name__ == '__main__':
    app.run()
