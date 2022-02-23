import pytest
from get_function import get_auth_key
import os
from api import pf
from string_generators import generate_string, cyrillic_chars, chinese_chars, special_symbols


@pytest.mark.xfail(raises=RuntimeError)
@pytest.mark.api
@pytest.mark.set_photo
@pytest.mark.parametrize("pet_photo", ["images/cat1.jpg", "images/img.png"], ids=["jpg", "png"])
def test_set_photo_of_pet_positive(get_key, pet_photo):
    """Check possibility to add photo of existing pet"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, my_pets = pf.get_pet_list(pf.key, "my_pets")

    if len(my_pets['pets']) > 0:  # if list of my_pets is not empty
        pf.status, result = pf.set_pet_photo(pf.key, my_pets['pets'][0]['id'], pet_photo)
    else:  # if my_pets is empty, add new pet without photo
        pf.add_new_pet_without_photo(pf.key, name='Имя', animal_type='Тип', age='4')
        _, my_pets = pf.get_pet_list(pf.key, "my_pets")

        pf.status, result = pf.set_pet_photo(pf.key, my_pets['pets'][0]['id'], pet_photo)

    assert pf.status == 200
    assert result['pet_photo']


@pytest.mark.api
@pytest.mark.set_photo
@pytest.mark.parametrize("pet_photo", ["images/cat1.jpg", "images/GIF.gif"], ids=["jpg correct", "gif-unsupported"])
@pytest.mark.parametrize("pet_id", ["", generate_string(255), generate_string(1001), cyrillic_chars(),
                                    cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["empty", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN",
                              "chinese", "specials", "digit"])
@pytest.mark.parametrize("key", [get_auth_key(), "", generate_string(255), generate_string(1001), cyrillic_chars(),
                                 cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["correct_key", "empty", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN",
                              "chinese", "specials", "digit"])
def test_set_photo_of_pet_negative(key, pet_id, pet_photo):
    """Check if set_pet_photo request with invalid authorisation key returns status code 403 or 400 - for incorrect
    data"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    temp_key = {}
    temp_key['key'] = get_auth_key()
    pf.add_new_pet_without_photo(temp_key, name='Имя', animal_type='Тип', age='4')  # add new pet without photo
    _, my_pets = pf.get_pet_list(temp_key, "my_pets")  # list of my_pets

    new_key = {}
    new_key['key'] = key
    pf.status, result = pf.set_pet_photo(new_key, pet_id, pet_photo)
    if key != get_auth_key():
        assert pf.status == 403
    else:
        assert pf.status == 400


















