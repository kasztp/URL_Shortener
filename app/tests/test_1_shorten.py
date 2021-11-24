from flask import json
from app import app

app.testing = True


def test_shorten():
    """Tests For /v1/shorten endpoint."""
    with app.app_context():
        # Test if GET is allowed
        response = app.test_client().get('/v1/url-management/shorten')

        assert response.status_code == 405
        assert dict(json.loads(response.get_data(as_text=True))) == {'error': 'HTTP Method Not allowed'}

        # Test for missing payload
        test_input_missing_payload = {}
        expected_output_missing_payload = {'error': 'The client provided incorrect input.'}
        response = app.test_client().post('/v1/url-management/shorten', json=test_input_missing_payload)

        assert response.status_code == 400
        assert dict(json.loads(response.get_data(as_text=True))) == expected_output_missing_payload

        # Test for valid payload
        test_input_valid_payload = {
            'payload': 'https://github.com/topics/amiga'
        }

        response = app.test_client().post('/v1/url-management/shorten',
                                          json=test_input_valid_payload)

        assert response.status_code == 200
        result = dict(json.loads(response.get_data(as_text=True)))
        assert result['is_url'] == True
        assert result['original'] == "https://github.com/topics/amiga"
        assert len(result['shortened']) == len("tier.app/19e0a0eb03b63bd4")
