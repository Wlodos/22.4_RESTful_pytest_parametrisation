import pytest
from get_function import get_auth_key
from api import pf
from string_generators import generate_string, cyrillic_chars, chinese_chars, special_symbols


@pytest.mark.api
@pytest.mark.new_pet
@pytest.mark.parametrize("name", [generate_string(255), generate_string(1001), cyrillic_chars(),
                                  cyrillic_chars().upper(), chinese_chars()],
                         ids=["255 symbols", "more than 1000 symbols", "russian", "RUSSIAN", "chinese"])
@pytest.mark.parametrize("animal_type", [generate_string(255), generate_string(1001), cyrillic_chars(),
                                         cyrillic_chars().upper(), chinese_chars()],
                         ids=["255 symbols", "more than 1000 symbols", "russian", "RUSSIAN", "chinese"])
@pytest.mark.parametrize("age", ["1"], ids=["min"])
def test_add_new_pet_without_photo_positive(get_key, name, animal_type, age):
    """Check possibility to add new pet without photo with correct data"""

    pf.status, result = pf.add_new_pet_without_photo(pf.key, name, animal_type, age)
    assert pf.status == 200
    assert result['name'] == name


@pytest.mark.api
@pytest.mark.new_pet
@pytest.mark.parametrize("age", ["", "-1", "0", "100", "1.5", "2147483647", "2147483648", generate_string(5),
                                 cyrillic_chars(), cyrillic_chars().upper(), chinese_chars(), special_symbols()],
                         ids=["empty", "negative", "zero", "greater than max", "float", "int max", "int max + 1",
                              " abc symbols", "russian", "RUSSIAN", "chinese", "specials"])
@pytest.mark.parametrize("animal_type", ["", special_symbols(), "123"], ids=["empty", "specials", "digit"])
@pytest.mark.parametrize("name", ["", special_symbols(), "123"], ids=["empty", "specials", "digit"])
@pytest.mark.parametrize("key", [get_auth_key(), "", generate_string(255), generate_string(1001), cyrillic_chars(),
                                 cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["correct_key", "empty", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN",
                              "chinese", "specials", "digit"])
def test_add_new_pet_without_photo_negative(key, name, animal_type, age):
    """Check if add_new_pet_without_photo request with invalid authorisation key returns status code 403 or 400 - for
    incorrect data"""

    new_key = {}
    new_key['key'] = key

    pf.status, result = pf.add_new_pet_without_photo(new_key, name, animal_type, age)
    if key != get_auth_key():
        assert pf.status == 403
        assert "Please provide 'auth_key'" in result
    else:
        assert pf.status == 400









