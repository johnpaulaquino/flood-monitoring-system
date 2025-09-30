from fastapi import status


class BaseAppException(Exception):
     def __init__(self, message_status='error', message='Internal server error. Contact support if the problem persists.',
                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
          self.message_status = message_status
          self.message = message
          self.status_code = status_code
          super().__init__(message_status, message, status_code)


class DataBaseDataNotFoundException(BaseAppException):
     def __init__(self, message_status='fail', message='The requested data was not found.',
                  status_code=status.HTTP_404_NOT_FOUND):
          self.message_status = message_status
          self.message = message
          self.status_code = status_code
          super().__init__(message_status, message, status_code)


class JWTExpiredException(BaseAppException):
     def __init__(self, message_status='error', message='Your session has expired. Please log in again.',
                  status_code=status.HTTP_400_BAD_REQUEST):
          self.message_status = message_status
          self.message = message
          self.status_code = status_code
          super().__init__(message_status, message, status_code)


class DataForbiddenException(BaseAppException):
     def __init__(self, message_status='fail', message="Access forbidden. You don’t have permission to perform this action.",
                  status_code=status.HTTP_403_FORBIDDEN):
          self.message_status = message_status
          self.message = message
          self.status_code = status_code
          super().__init__(message_status, message, status_code)


class UnAuthorizeAccessException(BaseAppException):
     def __init__(self, message_status='fail', message="You are not authorized to access this resource. ",
                  status_code=status.HTTP_403_FORBIDDEN):
          self.message_status = message_status
          self.message = message
          self.status_code = status_code
          super().__init__(message_status, message, status_code)