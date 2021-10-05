import geometry_controller as gc


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
