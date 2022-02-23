import pytest
import os
from api import pf
from string_generators import generate_string, cyrillic_chars, chinese_chars, special_symbols
from get_function import get_auth_key

@pytest.mark.api
@pytest.mark.pet_list
@pytest.mark.parametrize("filter", ["", "my_pets"], ids=["empty filter", "filter = my_pets"])
def test_get_all_pets_positive(get_key, filter):
    """Check if pet_list request returns not an empty list. Available value for filter - 'my_pets' or '' """

    pf.status, result = pf.get_pet_list(pf.key, filter)
    assert pf.status == 200
    assert len(result['pets']) > 0


@pytest.mark.api
@pytest.mark.pet_list
@pytest.mark.parametrize("filter", [generate_string(255), generate_string(1001), cyrillic_chars(),
                         cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["255 symbols", "more than 1000 symbols", "russian", "RUSSIAN", "chinese",
                              "specials", "digit"])
@pytest.mark.parametrize("key", [get_auth_key(), generate_string(255), generate_string(1001), cyrillic_chars(),
                                 cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["correct_key", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN", "chinese",
                              "specials", "digit"])
def test_get_all_pets_negative(key, filter):
    """Check if status of pet_list request with invalid filter is 500 or 403 for incorrect authorisation key.
     Available value for filter - 'my_pets' or '' """
    new_key = {}
    new_key['key'] = key

    pf.status, result = pf.get_pet_list(new_key, filter)

    if key != get_auth_key():
        assert pf.status == 403
        assert "Please provide 'auth_key'" in result
    else:
        assert pf.status == 500
        assert "Filter value is incorrect" in result

