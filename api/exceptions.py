from rest_framework.exceptions import APIException


class RegisterException(APIException):
    status_code = 400
    default_detail = 'Oops!'

    def __init__(self, detail):
        self.detail = detail