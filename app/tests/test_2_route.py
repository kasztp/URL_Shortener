from flask import json
from app import app
from app.models import URLStore

app.testing = True


def test_route():
    """Tests For /v1/route endpoint"""
    with app.app_context():
        # Test if POST is allowed
        response = app.test_client().post('/v1/url-management/route/0123456789qwertz')

        assert response.status_code == 405
        assert dict(json.loads(response.get_data(as_text=True))) == {'error': 'HTTP Method Not allowed'}

        # Test for URL not already shortened
        expected_output_not_in_db = {
            'error': 'Invalid input - URL not in DB.',
            'in_database': False,
            'shortened': '0123456789qwertz'
        }

        response = app.test_client().get('/v1/url-management/route/0123456789qwertz')
        assert response.status_code == 400
        assert dict(json.loads(response.get_data(as_text=True))) == expected_output_not_in_db

        # Test for valid shortened URL
        expected_output_url_in_db = 'https://github.com/topics/amiga'
        test_input_url_in_db = URLStore.query.filter_by(original_url=expected_output_url_in_db).first().shortened
        print(test_input_url_in_db)
        response = app.test_client().get(f'/v1/url-management/route/{test_input_url_in_db}',
                                         follow_redirects=True)

        assert response.status_code == 200
        assert expected_output_url_in_db in response.get_data(as_text=True)
