__all__ = ["CVAnalyzerException", "UserInputError", "BusinessError", "ExternalServiceError", "InternalError"]


class CVAnalyzerException(Exception):
    code = "cv_analyzer_exception"


class UserInputError(CVAnalyzerException):
    code = "user_input_error"


class BusinessError(CVAnalyzerException):
    code = "business_error"


class ExternalServiceError(CVAnalyzerException):
    code = "external_service_error"


class InternalError(CVAnalyzerException):
    code = "internal_error"
