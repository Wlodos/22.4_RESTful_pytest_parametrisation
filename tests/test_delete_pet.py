import pytest
from get_function import get_auth_key
from api import pf
from string_generators import generate_string, cyrillic_chars, chinese_chars, special_symbols


@pytest.mark.xfail(raises=RuntimeError)
@pytest.mark.api
@pytest.mark.delete_pet
def test_delete_pet_positive(get_key):
    """Check possibility to delete pet with correct data"""
    pf.add_new_pet_without_photo(pf.key, name='Имя', animal_type='Тип', age='4')
    _, my_pets = pf.get_pet_list(pf.key, "my_pets")

    pf.status, result = pf.delete_pet(pf.key, my_pets['pets'][0]['id'])
    assert pf.status == 200


@pytest.mark.xfail(raises=RuntimeError)
@pytest.mark.api
@pytest.mark.delete_pet
@pytest.mark.parametrize("pet_id", ["", generate_string(255), generate_string(1001), cyrillic_chars(),
                                    cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["empty", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN",
                              "chinese", "specials", "digit"])
@pytest.mark.parametrize("key", [get_auth_key(), "", generate_string(255), generate_string(1001), cyrillic_chars(),
                                 cyrillic_chars().upper(), chinese_chars(), special_symbols(), "123"],
                         ids=["correct_key", "empty", "255 symbols", "more than 1000 symbols", "russian", "RUSSIAN",
                              "chinese", "specials", "digit"])
def test_delete_pet_positive(key, pet_id):
    """Check possibility to delete pet with incorrect data. Status code 403 - for invalid authorisation key, 400 - for
    incorrect pet_id"""
    temp_key = {}
    temp_key['key'] = get_auth_key()
    pf.add_new_pet_without_photo(temp_key, name='Имя', animal_type='Тип', age='4')

    new_key = {}
    new_key['key'] = key
    pf.status, result = pf.delete_pet(new_key, pet_id)

    if key != get_auth_key():
        assert pf.status == 403
    else:
        assert pf.status == 400

