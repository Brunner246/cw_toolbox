import os
import sys
from pathlib import Path
from pprint import pprint
from collections import namedtuple, defaultdict

import cadwork                  as cw
import attribute_controller     as ac
import element_controller       as ec
import geometry_controller      as gc
import utility_controller       as uc
import bim_controller           as bc
import material_controller      as mc
import visualization_controller as vc
import scene_controller         as sc
import file_controller          as fc
import list_controller          as lc
import shop_drawing_controller  as sdc
import menu_controller          as mec


def reset():
    """
    shortcut to delete all elements in model
    :return:
    """
    ec.delete_elements(ec.get_all_identifiable_element_ids())
    vc.refresh()


print(sys.version_info)
print(sys.executable)
for p in sys.path:
    print(p)


cwps = [
    r"C:\Program Files\cadwork.dir\EXE_28\Pclib.x64\python38\site-packages",
    str(Path().home() / ".virtualenvs" / "cadwork" / "Lib" / "site-packages"),
]
for cwp in cwps:
    if cwp not in sys.path:
        print(f"appending to path: {cwp}")
        sys.path.append(cwp)

print("")

selection = ec.get_active_identifiable_element_ids()
if selection:
    s0 = selection[0]
if len(selection) > 1:
    s1 = selection[1]
selection_names = [ac.get_name(eid) for eid in selection]
print(f"INFO: found {len(selection) :5} selected elements")

all_ids = ec.get_all_identifiable_element_ids()

elem_names_by_id = {}
elem_ids_by_type = defaultdict(list)
for elem_id in all_ids:
    elem_name = ac.get_name(elem_id)
    # print(elem_id, elem_name)
    elem_names_by_id[elem_id] = elem_name
    if ac.get_element_type(elem_id).is_floor():
        elem_ids_by_type["floor"].append(elem_id)
    elif ac.get_element_type(elem_id).is_wall():
        elem_ids_by_type["wall"].append(elem_id)

print(f"INFO: found {len(elem_names_by_id) :5} elements in model\n")


if __name__ == "__main__":
    from cw_toolbox.helpers.repl import start_repl

    ptp_repl = start_repl()

    del(ptp_repl)

