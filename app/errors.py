from app import app


@app.errorhandler(400)
def incorrect_properties(error):
    return {'error': 'The client provided incorrect input.'}, 400


@app.errorhandler(401)
def auth_error(error):
    return {'error': 'Authentication error.'}, 401


@app.errorhandler(403)
def operation_error(error):
    return {'error': 'The operation cannot be performed by the client'}, 403


@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404


@app.errorhandler(405)
def not_allowed(error):
    return {'error': 'HTTP Method Not allowed'}, 405
