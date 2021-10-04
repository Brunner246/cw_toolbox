from collections import defaultdict

import element_controller   as ec
import attribute_controller as ac


def get_element_ids_by_type_name(preselected=None, quiet=None):
    if not preselected:
        preselected = ec.get_all_identifiable_element_ids()
    elem_ids_by_type = defaultdict(list)
    for elem_id in preselected:
        # TODO get type string generically
        if ac.get_element_type(elem_id).is_floor():
            elem_ids_by_type["floor"].append(elem_id)
        elif ac.get_element_type(elem_id).is_wall():
            elem_ids_by_type["wall"].append(elem_id)

    if not quiet:
        for elem_type_name, elem_ids in elem_ids_by_type.items():
            print(35 * "-")
            print(f"{elem_type_name} ({len(elem_ids)})\n")
            for elem_id in elem_ids:
                print(elem_id)

    return elem_ids_by_type


def get_element_names_by_id(preselected=None, quiet=None):
    if not preselected:
        preselected = ec.get_all_identifiable_element_ids()
    elem_names_by_id = {}
    for elem_id in preselected:
        elem_name = ac.get_name(elem_id)
        # print(elem_id, elem_name)
        elem_names_by_id[elem_id] = elem_name

    if not quiet:
        for elem_id, name in elem_names_by_id.items():
            print(f"{elem_id} : {name}")

    return elem_names_by_id


def get_element_ids_by_name(preselected=None, quiet=None):
    if not preselected:
        preselected = ec.get_all_identifiable_element_ids()
    elem_ids_by_name = defaultdict(list)
    for elem_id in preselected:
        elem_name = ac.get_name(elem_id)
        elem_ids_by_name[elem_name].append(elem_id)

    if not quiet:
        for name in sorted(elem_ids_by_name.keys()):
            print(35 * "-")
            print(f"{name} ({len(elem_ids_by_name[name])})\n")
            for elem_id in elem_ids_by_name[name]:
                print(elem_id)

    return elem_ids_by_name

