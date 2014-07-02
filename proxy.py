import urllib2
import os
from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/')
def index():
    try:
        response = urllib2.urlopen(request.query_string)
    except:
        return ("Cannot fetch remote URL %s" % request.query_string, 500, {})

    resp = make_response(response.read())
    resp.headers['Access-Control-Allow-Origin'] = 'gpgverify.github.io'
    resp.headers['Content-Type'] = response.info().getheader('Content-Type')
    resp.headers['Content-Length'] = response.info().getheader('Content-Length')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
