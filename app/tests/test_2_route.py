from flask import json
from app import app

app.testing = True


def test_route():
    """Tests For /v1/route endpoint"""
    with app.app_context():
        # Test if GET is allowed
        response = app.test_client().get('/v1/url-management/route')

        assert response.status_code == 405
        assert dict(json.loads(response.get_data(as_text=True))) == {'error': 'HTTP Method Not allowed'}

        # Test for URL not already shortened
        test_input_not_in_db = {'payload': 'TEST'}
        expected_output_not_in_db = {
            'error': 'Invalid input - URL not in DB.',
            'in_database': False,
            'shortened': 'TEST'
        }

        response = app.test_client().post('/v1/url-management/route', json=test_input_not_in_db)
        assert response.status_code == 400
        assert dict(json.loads(response.get_data(as_text=True))) == expected_output_not_in_db

        # Test for valid shortened URL
        test_input_url_in_db = {'payload': '1'}
        expected_output_url_in_db = 'https://github.com/topics/amiga?l=python&amp;o=asc&amp;s=updated'
        response = app.test_client().post('/v1/url-management/route',
                                          json=test_input_url_in_db,
                                          follow_redirects=True)

        assert response.status_code == 200
        assert expected_output_url_in_db in response.get_data(as_text=True)
