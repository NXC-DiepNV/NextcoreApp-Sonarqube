class CustomException(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return f"Error {self.code}: {self.message}" if self.code else self.message


class ExceptionCore:

    @staticmethod
    def raise_custom_exception(message, code: int = None):
        raise CustomException(message, code)

    @staticmethod
    def handle_exception(exception):
        if isinstance(exception, CustomException):
            return f"Custom Exception - {exception}"
        else:
            return f"Unknown Exception - {str(exception)}"

    @staticmethod
    def log_exception(exception, log_file="error_log.txt"):
        with open(log_file, "a") as f:
            f.write(f"{exception}\n")
