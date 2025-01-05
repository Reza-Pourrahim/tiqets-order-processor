from http import HTTPStatus

from flask import jsonify

from . import bp


@bp.errorhandler(Exception)
def handle_error(error):
    """Global error handler for the API"""
    response = {"status": "error", "message": str(error)}

    if hasattr(error, "code"):
        return jsonify(response), error.code

    return jsonify(response), HTTPStatus.INTERNAL_SERVER_ERROR
