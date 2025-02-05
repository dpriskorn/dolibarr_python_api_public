class DebugExit(BaseException):
    pass


class DolibarrError(BaseException):
    pass


# class FuzzyMatchError(BaseException):
#     pass


class LoginError(BaseException):
    pass


class MissingInformationError(BaseException):
    pass


class ProductExpiredError(BaseException):
    pass


class ScrapeError(BaseException):
    pass


class ProductNotFoundError(BaseException):
    pass


class OutOfRangeError(BaseException):
    pass


class MultipleMatchingSebTransactionsError(BaseException):
    pass


class ParseError(BaseException):
    pass


class DeprecatedMethodError(Exception):
    pass


class AccountingError(BaseException):
    pass


class MissingDataError(BaseException):
    pass


class NotFoundError(BaseException):
    pass


class CartError(BaseException):
    pass
