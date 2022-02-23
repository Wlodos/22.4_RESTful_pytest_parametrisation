import pytest
from get_function import get_auth_key
import os
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
@pytest.mark.parametrize("pet_photo", ["images/cat1.jpg", "images/img.png"], ids=["jpg", "png"])
def test_add_new_pet_positive(get_key, name, animal_type, age, pet_photo):
    """Check possibility to add new pet with correct data"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.status, result = pf.add_new_pet(pf.key, name, animal_type, age, pet_photo)
    assert pf.status == 200
    assert result['name'] == name


@pytest.mark.api
@pytest.mark.new_pet
@pytest.mark.parametrize("pet_photo", ["images/cat1.jpg", "images/GIF.gif"], ids=["jpg correct", "gif-unsupported"])
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
def test_add_new_pet_negative(key, name, animal_type, age, pet_photo):
    """Check if add_new_pet request with incorrect data returns status code 400 or 403 - for incorrect authorisation
    key"""
    new_key = {}
    new_key['key'] = key
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.status, result = pf.add_new_pet(new_key, name, animal_type, age, pet_photo)
    if key != get_auth_key():
        assert pf.status == 403
        assert "Please provide 'auth_key'" in result
    else:
        assert pf.status == 400


