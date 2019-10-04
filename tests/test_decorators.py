import warnings

from unittest import TestCase

from aioa2squery.decorators import deprecated


class TestFunctionDecorators(TestCase):
    def test_warn_decorator(self):
        @deprecated(message="Please don't use this!")
        def func():
            return True

        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            self.assertTrue(func())
            assert len(warning) == 1
            assert issubclass(warning[-1].category, DeprecationWarning)
            assert str(warning[-1].message) == "Please don't use this!"
