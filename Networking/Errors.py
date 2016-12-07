"""
Contains custom exceptions thrown during workflow
"""


class BaseServerException(Exception):
    message = ''

    def get_message(self):
        return self.message


class UnknownOrderError(BaseServerException):
    """
    Occurs when user sends oder not recognized by server.
    """
    message = 'Unknown order provided.'
    pass


class AuthenticationError(BaseServerException):
    """
    Occurs when:
     * user's ip is on banned list
     * user provides wrong password
    """
    message = 'Wrong username or password.'
    pass
