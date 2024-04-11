# Utitlity function and classes
from rest_framework import status
from rest_framework.response import Response


def send_response(result=True, message="", error=None, data=None):
    if not result:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            'success': 'False',
            'status code': status_code,
            'message': message,
        }
        if error is not None:
            response.__setitem__("error", error)
    else:
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': message,
        }
        if data is not None:
            response.__setitem__("data", data)

    return Response(response, status=status_code)
