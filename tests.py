"""Модуль с юнит-тестами."""
import os
import unittest

from custom_exceptions import InputParameterVerificationError, WrongRetryTimesError, GeneralVerificationError, \
    ResultVerificationError
from main import my_decorator_factory
from validators import json_validator, regex_validator, default_validator


class TestValidators(unittest.TestCase):
    """Класс с тестами валидаторов."""

    def test_json_validator_raises_exception(self) -> None:
        """Валидатор, получив неправильные данные, выкидывает исключение."""
        with self.assertRaises(GeneralVerificationError):
            json_validator("{}")

    def test_json_validator_passes(self) -> None:
        """Валидатор, получив правильные данные, должен вернуть True."""
        with open(os.path.join(os.getcwd(), "good_data.json")) as json_file:
            json_data = json_file.read()
        self.assertTrue(json_validator(json_data))

    def test_regex_validator_raises_exception(self) -> None:
        """Валидатор, получив неправильные данные, выкидывает исключение."""
        with self.assertRaises(GeneralVerificationError):
            regex_validator("t")

    def test_regex_validator_passes(self) -> None:
        """Валидатор, получив правильные данные, должен вернуть True."""
        self.assertTrue(regex_validator("ttt"))


class TestDecorator(unittest.TestCase):
    """Класс с тестами декоратора."""

    def test_repeat_times_zero_causes_exception(self) -> None:
        """Декоратор выкидает исключение, если количество повторов равно 0."""

        @my_decorator_factory(lambda x: True,
                              lambda x: True,
                              on_fail_repeat_times=0)
        def target_function() -> str:
            return "result"

        with self.assertRaises(WrongRetryTimesError):
            target_function()

    def test_input_validation_fails(self) -> None:
        """Неверные входящие данные вызывают исключение."""

        @my_decorator_factory(json_validator,
                              lambda x: True)
        def target_function() -> str:
            return "result"

        with self.assertRaises(InputParameterVerificationError):
            target_function('{1: "wrong json data"}')

    def test_input_validation_passes_output_validation_fails(self) -> None:
        """Неверные исходящие данные вызывают исключение."""

        @my_decorator_factory(regex_validator,
                              json_validator)
        def target_function(input_data: str) -> str:
            return "result"

        with self.assertRaises(ResultVerificationError):
            target_function("ttt")

    def test_input_validation_passes_output_validation_passes(self) -> None:
        """Входящая и исходящая проверка проходит успешно"""

        @my_decorator_factory(json_validator,
                              regex_validator,
                              on_fail_repeat_times=1)
        def target_function(input_data: str) -> str:
            return "ttt"

        with open(os.path.join(os.getcwd(), "good_data.json")) as json_file:
            json_data = json_file.read()
        self.assertEqual(target_function(json_data), "ttt")

    def test_default_validation_pass(self) -> None:
        """Дефолтная проверка проходит успешно."""

        @my_decorator_factory(default_validator,
                              lambda x: True)
        def target_function() -> str:
            return "result"

        self.assertEqual(target_function(), "result")
