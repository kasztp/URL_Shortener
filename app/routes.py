from flask import abort, escape, redirect, render_template, request
from validator_collection.checkers import is_url
from app import app
from app.shortener_logic import logger, shortener, shortened_validator


@app.route('/')
def root():
    """Route for /"""
    logger(request.remote_addr, '/')
    return render_template('index.html', title='URL Shortener API - Quick Start')


@app.route('/v1/url-management/shorten', methods=["POST"])
def shorten():
    """Endpoint for shortening the supplied URL."""
    data = request.get_json(silent=True)
    logger(request.remote_addr, '/v1/url-management/shorten')
    if not request.json or 'payload' not in request.json:
        abort(400)
    original = escape(is_url(data["payload"]))
    print(original)
    if not original:
        response = {
            "error": "Invalid input - Not valid URL.",
            "original": data["payload"],
            "is_url": False
        }
        return response, 400
    else:
        response = shortener(data)
        return response


@app.route('/v1/url-management/route', methods=["POST"])
def route():
    """Endpoint for basic routing based on the shortened value."""
    data = request.get_json(silent=True)
    logger(request.remote_addr, '/v1/url-management/route')
    if not request.json or 'payload' not in request.json:
        abort(400)
    original = escape(shortened_validator(data["payload"]))
    print(original)
    if not original:
        response = {
            "error": "Invalid input - URL not in DB.",
            "in_database": False,
            "shortened": data["payload"]
        }
        return response, 400
    else:
        response = redirect(original)
        return response, 200
