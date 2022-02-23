from settings import valid_email, valid_password
from api import pf


def get_auth_key():
    status, result = pf.get_api_key(valid_email, valid_password)
    return result['key']


# def get_pet_id():
#     new_key = {}
#     new_key['key'] = get_auth_key()
#
#     _, my_pets = pf.get_pet_list(new_key, "my_pets")
#     return my_pets['pets'][0]['id']



#Delete (all - 5) pets
# @pytest.mark.xfail(raises=RuntimeError)
# @pytest.mark.api
# @pytest.mark.delete_pet
# def test_delete_pet_with_valid_data(get_key):
#     """Check possibility to delete pet with correct data"""
#     _, my_pets = pf.get_pet_list(pf.key, "my_pets")
#     if len(my_pets['pets']) > 0:
#         print(f"len = {len(my_pets['pets'])}")
#         for i in range(len(my_pets['pets']) - 5):
#
#             pf.status, result = pf.delete_pet(pf.key, my_pets['pets'][i]['id'])
#             assert pf.status == 200
#     else:
#         raise Exception("There is not my pets")