from flask import json
from app import app

app.testing = True


def test_shorten():
    """Tests For /v1/shorten endpoint."""
    with app.app_context():
        response = app.test_client().get('/v1/url-management/shorten')

        assert response.status_code == 405
        assert dict(json.loads(response.get_data(as_text=True))) == {'error': 'HTTP Method Not allowed'}

        test_input_missing_payload = {}

        expected_output_missing_payload = {'error': 'The client provided incorrect input.'}

        response = app.test_client().post('/v1/url-management/shorten', json=test_input_missing_payload)

        assert response.status_code == 400
        assert dict(json.loads(response.get_data(as_text=True))) == expected_output_missing_payload

        test_input_valid_payload = {'payload': 'https://github.com/topics/amiga?l=python&o=asc&s=updated'}

        expected_output_valid_payload = {
          "is_url": True,
          "original": "https://github.com/topics/amiga?l=python&o=asc&s=updated",
          "shortened": "tier.app/1"
        }

        response = app.test_client().post('/v1/url-management/shorten', json=test_input_valid_payload)

        assert response.status_code == 200
        assert dict(json.loads(response.get_data(as_text=True))) == expected_output_valid_payload
