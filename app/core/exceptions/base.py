__all__ = ["CVAnalyzerException", "BusinessException", "UpstreamServiceError", "IllegalArgument"]


class CVAnalyzerException(Exception):
    code = "cv_analyzer_exception"


class BusinessException(CVAnalyzerException):
    code = "business_exception"


class UpstreamServiceError(CVAnalyzerException):
    code = "upstream_service_error"


class IllegalArgument(CVAnalyzerException):
    code = "illegal_argument"
