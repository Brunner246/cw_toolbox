import cadwork             as cw
import geometry_controller as gc
from .bbox import get_bbox_from_elem_id, bbox_longest_ortho_edge_vector


def check_wall_ref_side_points_towards_floor_centroid(wall_id: int, floor_id: int) -> bool:
    """
    Checks on a pair of wall and floor if the wall reference side
    is oriented towards floor gravity centroid.
    :param wall_id:
    :param floor_id:
    :return:
    """
    wall_zl = gc.get_zl(wall_id)

    abs_vectors = {vec_dir:abs(getattr(wall_zl, vec_dir)) for vec_dir in ("x","y","z")}
    axis_name_of_interest = max(abs_vectors, key=abs_vectors.get)

    wall_grav  = gc.get_center_of_gravity(wall_id)
    floor_grav = gc.get_center_of_gravity(floor_id)

    local_vector_difference = getattr(floor_grav, axis_name_of_interest) - getattr(wall_grav, axis_name_of_interest)
    wall_local_vec = getattr(wall_zl, axis_name_of_interest)

    correct_zl = (local_vector_difference * wall_local_vec) >= 0
    print(f"{correct_zl =}")
    return correct_zl


def flip_ref_side(elem_id: int):
    """
    Flips reference side. (rotates height axis by 180°)
    :param elem_id:
    :return:
    """
    gc.rotate_height_axis_180([elem_id])


def set_ref_side_horizontal(elem_id: int):
    """
    Attempts to set the reference side vector to be horizontal.
    Warning: This recursive function can result in endless loops
    when applied to 'wrong' objects
    :param elem_id:
    :return:
    """
    if gc.get_xl(elem_id).z != 0.0:
        print(f"{elem_id} no horizontal ref_side_vec")
        gc.rotate_length_axis_90([elem_id])
        set_ref_side_horizontal(elem_id)
    else:
        print(f"{elem_id} horizontal ref_side_vec")


def set_ref_side_to_bottom(elem_id: int, ref_dir: cw.point_3d):
    """
    Attempts to set the reference side vector to element bottom.
    Warning: This recursive function can result in endless loops
    when applied to 'wrong' objects
    :param elem_id:
    :param ref_dir:
    :return:
    """
    elem_zl = gc.get_zl(elem_id)
    if elem_zl != ref_dir:
        print(f"{elem_id} not yet at ref_side_to_bottom")
        gc.rotate_height_axis_90([elem_id])
        set_ref_side_to_bottom(elem_id)
    else:
        print(f"{elem_id} is already at ref_side_to_bottom")
        return


def unset_ref_dir_from_longest_edge(elem_id: int):
    """
    Rotates coordinate system along length axis until reference side direction
    is not collinear to longest edge of element.
    Warning: This recursive function can result in endless loops
    when applied to 'wrong' objects
    :param elem_id:
    :return:
    """
    global_z = gc.get_local_z()
    global_z.z = -1.0
    current_ref_side_dir = gc.get_xl(elem_id)
    bbx = get_bbox_from_elem_id(elem_id)
    longest_edge_dir_name = bbox_longest_ortho_edge_vector(bbx)
    global_dir_of_longest_edge = getattr(gc, f"get_local_{longest_edge_dir_name}")()
    target_dir = global_z.cross(global_dir_of_longest_edge)
    print(f"{elem_id} {longest_edge_dir_name} {target_dir =} for ref_side_dir")
    print(f"{elem_id} {current_ref_side_dir =} longest edge: {global_dir_of_longest_edge =}")
    if current_ref_side_dir != target_dir:
        print(f"{elem_id} current_ref_side_dir is along longest_edge_dir - fixing")
        gc.rotate_length_axis_90([elem_id])
        unset_ref_dir_from_longest_edge(elem_id)
    else:
        print(f"{elem_id} correct: current_ref_side_dir is not on longest_edge_dir")

