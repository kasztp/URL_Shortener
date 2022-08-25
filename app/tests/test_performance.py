from os import path
from concurrent.futures import ThreadPoolExecutor
from flask import json
import pandas as pd
from time import time
from app import app, db
from app.models import Logs, URLStore

basedir = path.abspath(path.dirname(__file__))
app.testing = True


def get_url_count() -> int:
    number_of_urls = db.session.query(URLStore).count()
    return number_of_urls


def shorten(test_input):
    """Tests For /v1/shorten endpoint."""
    with app.app_context():
        test_input_valid_payload = {'payload': test_input}

        start_time = time()
        response = app.test_client().post('/v1/url-management/shorten', json=test_input_valid_payload)
        response_data = dict(json.loads(response.get_data(as_text=True)))
        execution_time = time() - start_time

        assert response.status_code == 200
        assert test_input == response_data['original'] and response_data['is_url']

        return execution_time


def test_multithreaded_wrapper():
    """Wrapper for running a large number of tests concurrently"""
    url_count = 512
    max_threads = 16

    # Read test dataset
    test_data_df = pd.read_csv(path.join(basedir, 'test_data/urlset.csv'))
    test_data_df['domain'] = 'https://' + test_data_df['domain'].astype(str)
    test_urls = test_data_df['domain'].head(url_count)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        request_times = list(executor.map(shorten, test_urls))

    assert sum(request_times) / url_count < 0.25


def test_db_cleanup():
    """Cleanup DB after test suite ends"""
    db.session.query(URLStore).delete()
    db.session.query(Logs).delete()
    db.session.commit()
    assert get_url_count() == 0
