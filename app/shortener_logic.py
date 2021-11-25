from uuid import uuid3, uuid4, NAMESPACE_URL
from app import db
from app.models import URLStore, Logs


def shortened_validator(data: str):
    """Check if shortened URL maps to a valid DB entry."""
    url_check = URLStore.query.filter_by(shortened=data).first()
    if url_check:
        print(f'URL Already in DB as: {url_check.shortened}')
        return url_check.original_url
    print('URL Not yet in DB.')
    return False


def logger(ip: str, url: str):
    """Basic logging to DB"""
    log_entry = Logs(ip_address=ip, endpoint=url)
    db.session.add(log_entry)
    db.session.commit()


def shortener(original_url: str) -> dict:
    """Generate shortened URL"""
    url_check = URLStore.query.filter_by(original_url=original_url).first()

    if url_check:
        print(f'URL Already in DB as: {url_check.shortened}')
        shortened = 'tier.app/' + url_check.shortened
    else:
        print('URL Not yet in DB.')
        shortened = ''.join(str(uuid3(NAMESPACE_URL, original_url)).split('-'))[:16]
        try:
            db_entry = URLStore(original_url=original_url, shortened=shortened)
            db.session.add(db_entry)
            db.session.commit()
        except:
            print('UUID already in DB, generating another.')
            shortened = ''.join(str(uuid4()).split('-'))[:17]
            db_entry = URLStore(original_url=original_url, shortened=shortened)
            db.session.add(db_entry)
            db.session.commit()
        shortened = 'tier.app/' + shortened

    response = {
        "original": original_url,
        "shortened": shortened,
        "is_url": True,
    }
    return response
