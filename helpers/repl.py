import sys
from ptpython.repl import embed


def rq():
    """
    shortcut to quit the repl
    :return:
    """
    sys.exit()


def start_repl():
    """
    starts ptpython repl
    :return:
    """
    return embed(globals(), locals())

