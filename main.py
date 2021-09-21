"""
Фабрика декораторов.

Принимает 4 параметра:
1. Валидатор входящих данных (обязательный)
2. Валидатор исходящих данных (обязательный)
3. Количество повторов вызова функции (необязательный, по умолчанию 1)
    Количество повторов не может быть 0, иначе будет выброшено исключение WrongRetryTimesError
4. Функция по умолчанию (необязательный)

Перед запуском целевой функции запускается валидатор входящих данных, если данные не прошли валидацию, выбрасывается
исключение "InputParameterVerificationError", выполнение останавливается.
Если валидация входящих данных пройдена успешно, запускается целевая функция. Результат выполнения целевой функции
проверяется валидатором исходящих данных. Если валидация успешная, возвращается результат целевой функции, если нет -
процесс повторяется столько раз, сколько было указано в переменной on_fail_repeat_times.
Если после всех попыток валидация не увенчается успехом, будет вызвана функция по умолчанию, если она задана, или
будет выкинуто исключение "ResultVerificationError" в противном случае.
Если значение переменной "on_fail_repeat_times" отрицательное, вызов функции будет производится до тех пор,
пока валидаця исходящих данных не увенчается успехом, либо вечно.
"""
import os
from typing import Callable, Union, Dict, Any, Tuple
from custom_exceptions import InputParameterVerificationError, WrongRetryTimesError, ResultVerificationError, \
    GeneralVerificationError
from validators import regex_validator, json_validator


def my_decorator_factory(
        input_validation: Callable,
        result_validation: Callable,
        on_fail_repeat_times: int = 1,
        default_behaviour: Union[Callable, None] = None
) -> Callable:
    """Фабрика для декоратора. Нужна для передачи аргументов."""

    def my_decorator(func: Callable) -> Callable:
        def wrapper(*args: Tuple[Any], **kwargs: Dict[Any, Any]) -> Any:
            nonlocal on_fail_repeat_times
            if on_fail_repeat_times == 0:
                raise WrongRetryTimesError
            try:
                input_validation(*args)
            except GeneralVerificationError as e:
                raise InputParameterVerificationError from e

            while on_fail_repeat_times != 0:
                if on_fail_repeat_times > 0:
                    on_fail_repeat_times -= 1
                result = func(*args)
                try:
                    if result_validation(result):
                        return result
                except GeneralVerificationError:
                    continue
            if default_behaviour is not None:
                default_behaviour()
            raise ResultVerificationError

        return wrapper

    return my_decorator


if __name__ == "__main__":
    def def_beh() -> None:
        """Отладочная функция поведения по умолчанию."""


    @my_decorator_factory(regex_validator,
                          json_validator,
                          on_fail_repeat_times=10,
                          default_behaviour=def_beh)
    def test(data: str) -> str:
        print(data)
        """Отладочная функция проверки декоратора."""
        with open(os.path.join(os.getcwd(), "good_data.json")) as json_file:
            return json_file.read()


    test("ttt")
