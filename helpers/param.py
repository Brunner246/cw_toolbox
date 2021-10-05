import json
from pathlib import Path
from functools import lru_cache
import attribute_controller as ac
import utility_controller   as uc


def get_element_user_attributes(elem_id: int) -> dict:
    """
    Returns a mapping of parameter name - value
    for user attributes of specified element.
    :param elem_id:
    :return:
    """
    user_param_map = {}
    user_attribute_map_by_name = get_user_attribute_map_by_name()
    for name, i in user_attribute_map_by_name.items():
        attr_value = ac.get_user_attribute(elem_id, i)
        user_param_map[i] = {
            "name" : name,
            "value": attr_value,
        }
    return user_param_map


def ensure_user_parameters(quiet=None) -> dict:
    """
    Ensures that the canonical mapping of user parameters
    according to a single source are set.
    :return:
    """
    user_profile_path = Path(uc.get_3d_userprofil_path())
    company_user_profile_path = user_profile_path / "company_user_attributes.json"
    if not company_user_profile_path.exists():
        print(f"ERROR: Sorry {company_user_profile_path} seems to be missing")
        return {}
    with open(company_user_profile_path) as attr_json:
        cw_attributes = json.load(attr_json)["cw_user_attributes"]

    for attr_name, cw_user_attr_nr in cw_attributes.items():
        if ac.get_user_attribute_name(cw_user_attr_nr) == f"User{cw_user_attr_nr}":
            ac.set_user_attribute_name(cw_user_attr_nr, attr_name)
            if not quiet:
                print(f"INFO: ensure_user_parameters: successfully set user attribute: {attr_name}")
        elif ac.get_user_attribute_name(cw_user_attr_nr) == attr_name:
            if not quiet:
                print(f"INFO: ensure_user_parameters: user attribute already set: {attr_name}")
            continue
        else:
            if not quiet:
                print(f"INFO: ensure_user_parameters: user attribute {cw_user_attr_nr} named {attr_name} already in use!")
    return cw_attributes


@lru_cache(maxsize=128)
def get_user_attribute_map_by_name() -> dict:
    """
    Get user attribute mapping by attribute names
    :return:
    """
    user_attribute_name_map = {}
    for i in range(USER_ATTRIBUTE_SEARCH_COUNT):
        attr_name = ac.get_user_attribute_name(i)
        if attr_name.startswith("User"):
            continue
        user_attribute_name_map[attr_name] = i
    return user_attribute_name_map


@lru_cache(maxsize=128)
def get_user_attribute_map_by_id() -> dict:
    """
    Get user attribute mapping by attribute id
    :return:
    """
    user_attribute_id_map = {}
    for i in range(USER_ATTRIBUTE_SEARCH_COUNT):
        attr_name = ac.get_user_attribute_name(i)
        if attr_name.startswith("User"):
            continue
        user_attribute_id_map[i] = attr_name
    return user_attribute_id_map


USER_ATTRIBUTE_SEARCH_COUNT = 399
