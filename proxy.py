import requests
import os
from flask import Flask, make_response, request

app = Flask(__name__)

WHITELIST_URL = ('https://bitcoinfees.21.co/api/v1/fees/',)
WHITELIST_CONTENT = ('-----BEGIN PGP SIGNED MESSAGE-----',)

@app.route('/')
def index():
    try:
        headers = {"x-forwarded-for": request.remote_addr}
        response = requests.get(request.query_string, headers=headers)
    except:
        return ("Cannot fetch remote URL %s" % request.query_string, 401, {})

    if len(response.text) > 100000:
        return ("Provided URL is over 100kB in size", 401, {})

    if request.query_string.startswith(WHITELIST_URL):
        return process_response(response)

    if any(x in response.text for x in WHITELIST_CONTENT):
        return process_response(response)

    return ("Provided URL does not pass whitelist conditions", 401, {})

def process_response(response):
    resp = make_response(response.text)
    resp.headers['Access-Control-Allow-Origin'] = '*'

    forward_headers = ['Content-Type', 'Content-Length']
    for h in forward_headers:
        if h in response.headers:
            resp.headers[h] = response.headers[h]

    return resp

if __name__ == '__main__':
    app.run(debug=True)
