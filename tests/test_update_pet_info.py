import pytest
from get_function import get_auth_key
import os
from api import pf
from string_generators import generate_string, cyrillic_chars, chinese_chars, special_symbols


@pytest.mark.xfail(raises=RuntimeError)
@pytest.mark.api
@pytest.mark.update_pet_info
@pytest.mark.parametrize("age", ["1"], ids=["min"])
@pytest.mark.parametrize("animal_type", [generate_string(255), generate_string(1001), cyrillic_chars(),
                                         cyrillic_chars().upper(), chinese_chars()],
                         ids=["255 symbols", "more than 1000 symbols", "russian", "RUSSIAN", "chinese"])
@pytest.mark.parametrize("name", [generate_string(255), generate_string(1001), cyrillic_chars(),
                                  cyrillic_chars().upper(), chinese_chars()],
                         ids=["255 symbols", "more than 1000 symbols", "russian", "RUSSIAN", "chinese"])
def test_update_pet_info_positive(get_key, name, animal_type, age):
    """Check if update_pet_info request changes pet data"""

    _, my_pets = pf.get_pet_list(pf.key, "my_pets")
    if len(my_pets['pets']) > 0:
        pf.status, result = pf.update_pet_info(pf.key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert pf.status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


@pytest.mark.xfail(raises=RuntimeError)
@pytest.mark.api
@pytest.mark.update_pet_info
@pytest.mark.parametrize("age", ["", "-1", "0", "100", "1.5", "2147483647", "2147483648", generate_string(5),
                                 cyrillic_chars(), cyrillic_chars().upper(), chinese_chars(), special_symbols()],
                         ids=["empty", "negative", "zero", "greater than max", "float", "int max", "int max + 1",
                              " abc symbols", "russian", "RUSSIAN", "chinese", "specials"])
@pytest.mark.parametrize("animal_type", ["", special_symbols(), "123"], ids=["empty", "specials", "digit"])
@pytest.mark.parametrize("name", ["", special_symbols(), "123"], ids=["empty", "specials", "digit"])
@pytest.mark.parametrize("pet_id", ["", generate_string(255), generate_string(1001), cyrillic_chars(),
                                    cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["empty", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN",
                              "chinese", "specials", "digit"])
@pytest.mark.parametrize("key", [get_auth_key(), "", generate_string(255), generate_string(1001), cyrillic_chars(),
                                 cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["correct_key", "empty", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN",
                              "chinese", "specials", "digit"])
def test_update_pet_info_negative(key, pet_id, name, animal_type, age):
    """Check if update_pet_info request with incorrect data returns status code 400 or 403 - for invalid authorisation
    key"""
    temp_key = {}
    temp_key['key'] = get_auth_key()
    new_key = {}
    new_key['key'] = key

    _, my_pets = pf.get_pet_list(temp_key, "my_pets")
    if len(my_pets['pets']) > 0:
        pf.status, result = pf.update_pet_info(new_key, pet_id, name, animal_type, age)
        if key != get_auth_key():
            assert pf.status == 403
        else:
            assert pf.status == 400
    else:
        raise Exception("There is no my pets")
