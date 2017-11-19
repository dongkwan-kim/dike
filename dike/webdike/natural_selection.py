from webdike.models import *


MAX_POOL = 3


def need_proliferation(sid):
    """
    Return value is a tuple of boolean value B and a tuple T.
    B represents necessity of more candidate to go to next step.
    T represents Step instance(s) which is/are necessary for next interface.
    - If B is True, T is signleton tuple w/ a Step (current) for current step interface.
    - If B is False, T is a pair of Steps (next) for voting interface.
    :param sid: integer id of sentence.
    :return: (Boolean B, Tuple T)
    """

    # Find Sentence from sid

    # Count N, the number of Step instances w/ *next state*

    # If N >= MAX_POOL:
    #   No need proliferation.
    # If N == 2 and Steps (next) have same parent Step (current):
    #   No need proliferation.
    # If N == 2 and Steps (next) have different Step (current):
    #   Need prolifeation.
    # If N < 2:
    #   Need proliferation.

    # If No need proliferation:
    #   B = False, T = (Step_next_X, Step_next_Y)
    #   Note that Step_next_X and Step_next_Y have same parent Step (current)
    # If need proliferation:
    #   B = True, T = (Step_current,)

    # TODO How to vote when the current step is After-EXPLAINED
