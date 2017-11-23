from webdike.models import *


MAX_POOL = 3


def is_same_parent_step(step_1, step_2):
    """
    :param step_.*:
    """
    p_1 = step_1.parent_step
    p_2 = step_2.parent_step
    return (p_1.id == p_2.id)


def get_sibling_steps(step_query_set):
    x = step_query_set[0]
    y = step_query_set[1]
    z = step_query_set[2]

    if is_same_parent_step(x, y):
        return (x, y)
    elif is_same_parent_step(x, z):
        return (x, z)
    else:
        return (y, z)


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
    sentence = Sentence.objects.get(id=sid)

    # Count N, the number of Step instances w/ *next state*
    current_state = int(sentence.state)
    next_state = current_state + 1
    steps = sentence.step_set.filter(stage=next_state)
    population = len(steps)

    # If N >= MAX_POOL:
    #   No need proliferation.
    if population >= MAX_POOL:
        need = False

    # If N == 2 and Steps (next) have same parent Step (current):
    #   No need proliferation.
    # If N == 2 and Steps (next) have different Step (current):
    #   Need prolifeation.
    elif population == 2:
        need = not is_same_parent_step(steps[0], steps[1])

    # If N < 2:
    #   Need proliferation.
    else:
        need = True

    # If No need proliferation:
    #   B = False, T = (Step_next_X, Step_next_Y)
    #   Note that Step_next_X and Step_next_Y have same parent Step (current)
    if not need:
        return (need, get_sibling_steps(steps))

    # If need proliferation:
    #   B = True, T = (Step_current,)
    else:
        step_current = sentence.step_set.filter(stage=current_state, active=True)
        if step_current:
            step_current = step_current[0]
        else:
            raise Exception("No current step")
        return (need, (step_current,))

