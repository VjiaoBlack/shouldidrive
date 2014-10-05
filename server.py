from flask import Flask, render_template, request, abort, redirect
from decisions import decision

app = Flask(__name__)
app.debug = True


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



# Pages
@app.route('/')
def home():
    return redirect('/api/')
    #return render_template('index.html')

# API

# the only api call you'll ever need
# returns yes/no + weather and uber data
# GET /api/goto.json/?start_lat=<latitude>&start_lon=<longitude>&end_lat=<latitude>&end_lon=<longitude>
@app.route('/api/goto.json/')
@crossdomain(origin='*')
def goto():
    params = request.args
    origin = (params['start_lat'], params['start_lon'])
    destination = (params['end_lat'], params['end_lon'])
    return decision(origin, destination)
    
@app.route('/api/')
def api_description():
    return render_template('docs.html')

if __name__ == '__main__':
    app.run()
