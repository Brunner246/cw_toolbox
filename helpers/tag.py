import element_controller       as ec
import geometry_controller      as gc


def label_elem_with_id_text(elem_id, text_size=None):
    """
    Adds 3d id text label to given element ids.
    :param elem_id:
    :param text_size:
    :return:
    """
    ec.create_text_object(
        str(elem_id),
        gc.get_center_of_gravity(elem_id),
        gc.get_local_x(),
        gc.get_local_y(),
        text_size or 250,
    )
