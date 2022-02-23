import pytest
from settings import valid_email, valid_password
import os
from api import pf
from string_generators import generate_string, cyrillic_chars, chinese_chars, special_symbols


@pytest.mark.api
@pytest.mark.auth
def test_get_api_key_positive(email=valid_email, password=valid_password):
    """Check if api key request returns status 200 and result has 'key' word """

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.parametrize("password", ["", generate_string(255), generate_string(1001), cyrillic_chars(),
                                      cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["empty", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN", "chinese",
                              "specials", "digit"])
@pytest.mark.parametrize("email", ["", generate_string(255), generate_string(1001), cyrillic_chars(),
                                   cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["empty", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN", "chinese",
                              "specials", "digit"])
def test_get_api_key_negative(email, password):
    """Check if api key request with incorrect email and password returns 403 error"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "This user wasn't found in database" in result
