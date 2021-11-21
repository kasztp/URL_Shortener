from app import db
from app.models import URLStore, Logs


def shortened_validator(data):
    """Check if shortened URL maps to a valid DB entry."""
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


def to_base_62(number: int) -> str:
    """Convert decimal integer to base 62 for further shortening"""
    b_62 = str()
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    while number != 0:
        number, i = divmod(number, len(digits))
        b_62 = digits[i] + b_62
    return b_62


def shortener(original_url):
    """Generate shortened URL"""
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

        shortened = 'tier.app/' + url_temp.shortened

    response = {
        "original": original_url,
        "shortened": shortened,
        "is_url": True,
    }
    return response
