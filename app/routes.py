from flask import abort, redirect, render_template, request
from validator_collection.checkers import is_url
from app import app, db
from app.models import URLStore, Logs


def shortened_validator(data):
    url_check = URLStore.query.filter_by(shortened=data).first()
    if url_check:
        print(f'URL Already in DB as: {url_check.shortened}')
        return url_check.original_url
    else:
        print('URL Not yet in DB.')
        return False


def logger(ip, url):
    """Basic logging to DB"""
    log_entry = Logs(ip_address=ip, endpoint=url)
    db.session.add(log_entry)
    db.session.commit()


def to_base_62(number):
    """Convert decimal integer to base 62 for further shortening"""
    b_62 = str()
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    while number != 0:
        number, i = divmod(number, len(digits))
        b_62 = digits[i] + b_62
    return b_62


@app.route('/')
def root():
    logger(request.remote_addr, '/')
    return render_template('index.html', title='URL Shortener API - Quick Start')


@app.route('/v1/url-management/shorten', methods=["POST"])
def shorten():
    data = request.get_json(silent=True)
    logger(request.remote_addr, '/v1/url-management/shorten')
    if not request.json or 'payload' not in request.json:
        abort(400)
    original = is_url(data["payload"])
    print(original)
    if not original:
        response = {
            "error": "Invalid input - Not valid URL.",
            "original": data["payload"],
            "is_url": False
        }
        return response, 400
    else:
        original_url = data["payload"]
        url_check = URLStore.query.filter_by(original_url=original_url).first()
        if url_check:
            print(f'URL Already in DB as: {url_check.shortened}')
            shortened = 'tier.app/' + url_check.shortened
        else:
            print('URL Not yet in DB.')
            db_entry = URLStore(original_url=original_url)
            db.session.add(db_entry)
            db.session.commit()

            url_temp = URLStore.query.filter_by(original_url=original_url).first()
            shortened = str(to_base_62(url_temp.id))
            url_temp.shortened = shortened
            db.session.commit()

            print(f'{url_temp.id} -> {shortened}')
            shortened = 'tier.app/' + url_temp.shortened
        response = {
            "original": data["payload"],
            "shortened": shortened,
            "is_url": True,
        }
        return response


@app.route('/v1/url-management/route', methods=["POST"])
def route():
    data = request.get_json(silent=True)
    logger(request.remote_addr, '/v1/url-management/route')
    if not request.json or 'payload' not in request.json:
        abort(400)
    original = shortened_validator(data["payload"])
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
