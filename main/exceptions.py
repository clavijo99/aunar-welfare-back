from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken

HTTP_452_TOKEN_NOT_VALID = 452


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None and isinstance(exc, InvalidToken) and exc.default_code == 'token_not_valid':
        response.data['status_code'] = HTTP_452_TOKEN_NOT_VALID
        response.status_code = HTTP_452_TOKEN_NOT_VALID
        response.data = 'token_not_valid'
    return response
