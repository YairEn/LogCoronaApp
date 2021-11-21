from LogCorona.validators import _is_empty, validate_inputs
import pytest

ATTRIBUTE_ERROR = "'int' object has no attribute 'strip'"


class TestValidators:
    @staticmethod
    def test_validate_inupts_valid():
        assert validate_inputs('hey', 'world') is None

    @staticmethod
    def test_validate_inupts_invalid():
        assert validate_inputs('hey', '') is True

    @staticmethod
    def test_is_empty_false():
        assert _is_empty('hey') is False

    @staticmethod
    def test_is_empty_true():
        assert _is_empty('') is True

    @staticmethod
    def test_is_empty_wrong_type():
        with pytest.raises(AttributeError) as err:
            assert _is_empty(1)
        assert ATTRIBUTE_ERROR in str(err)
