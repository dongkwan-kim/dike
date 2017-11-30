from webdike.models import *


"""
Design Goal
1. Users can see only two candidates for a vote because of a large amount of text.
2. Users can continue or stop each step immediately with their free will.
3. Most of the users' task results should be useful to the entire system.

Basic Idea
- Obtain 'modeling popuation growth' w/ natural selection
- dN/dt = rN(1 - N/K) where
    K is the carrying capacity of the environment,
    N is the current polutation size,
    r is the maximum growth rate.
- In our algorithm,
    r is the increasing function regarding to voting counts v, r(v).
    Initial N is 1.
    c, death rate per time unit is constant.
    Each Step has own N and v.

Scenenario
1. When the user calls get_work_routing_info, one time unit starts.
2. In this time unit, the user votes or creates a Step or does both.
3. After this, with voting counts at that moment,
   |dN/dt| of Steps will grow (>0) or die (<0).

"""

# We can manipulate this value for our purpose.
# Carrying capacity of the environment.
K = 10


def get_work_routing_info(sid):
    """Get information for routing works to users.
    Return value is a dictionary that contains
        votable -- Boolean: whether there're sufficient elements to vote, (TN >= 1).
        creatable -- Boolean: whether there're places for new creation, (TN < K).
        step_list -- List: list of Step whose state is state_next
    where
        state_current -- Integer: state of Sentence(sid).
        state_next -- Integer: state_current + 1.
        TN -- Integer: the total number of Steps whose state is state_next.
    :param sid: integer id of step.
    :return: dictionary {votable, creatable, step_list}
    """

    # Find Step from sid
    step = Step.objects.get(id=sid)

    # Count g, the number of Step instances w/ *next stage*
    current_stage = int(step.stage)
    next_stage = current_stage

    (g, steps) = (-1, None)
    for _ in range(5):
        next_stage = next_stage + 1
        steps_total = Step.objects.filter(stage=next_stage)
        steps = steps_total.filter(population__gte=1)

        g_total = steps_total.count()
        g = steps.count()

        if next_stage >= 5:
            break

        # Natural selected.
        if g_total < 5 or g != 1:
            break

    # Determine votable, creatable
    # Alternative way: creatable = True always
    if next_stage == 5:
        votable, creatable = (False, False)
    elif g < 1:
        votable, creatable = (False, True)
    elif g < 5:
        votable, creatable = (True, True)
    else:
        votable, creatable = (True, False)

    # Make step_list
    if votable:
        # step_list = list of Steps (next_stage) in descending order by votes
        step_list = list(steps.order_by('-population'))
    else:
        step_list = []

    return {
        'votable': votable,
        'creatable': creatable,
        'step_list': step_list,
        'next_stage': next_stage,
    }


def change_populations(target_stage):
    """Steps wil grow or die.

    |dN/dt| of Steps will grow (>0) or die (<0).

    :param target_stage: integer
    :return: Boolean whether the total population is greater or equal to K.
    """

    TN = 0

    # In iterations of Steps whose stage is target_stage
    # Add dN/dt to Step.population
    current_steps = Step.objects.filter(stage=target_stage).exclude(population=0)
    for step in current_steps:
        N = step.population
        N += step.get_growth_rate(K)
        if N < 0:
            N = 0

        step.population = N
        step.save()
        TN += N

    return TN >= K

