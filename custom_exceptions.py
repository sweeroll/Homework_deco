class InputParameterVerificationError(Exception):
    """Исключение для входных параметров."""

    pass


class GeneralVerificationError(Exception):
    """Общее исключение для параметров."""

    pass


class ResultVerificationError(Exception):
    """Исключение для выходных параметров."""

    pass


class WrongRetryTimesError(Exception):
    """Исключение для неправильных типов."""

    pass

