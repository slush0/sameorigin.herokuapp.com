import requests
import os
from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/')
def index():
    try:
        response = requests.get(request.query_string)
    except:
        return ("Cannot fetch remote URL %s" % request.query_string, 500, {})

    if '-----BEGIN PGP SIGNED MESSAGE-----' not in response.text:
        return ("Provided URL does not contain any PGP signed message", 500, {})

    if len(response.text) > 100000:
        return ("Provided URL is over 100kB in size", 500, {})

    resp = make_response(response.text)
    resp.headers['Access-Control-Allow-Origin'] = '*'

    forward_headers = ['Content-Type', 'Content-Length']
    for h in forward_headers:
        if h in response.headers:
            resp.headers[h] = response.headers[h]

    return resp

if __name__ == '__main__':
    app.run(debug=True)
