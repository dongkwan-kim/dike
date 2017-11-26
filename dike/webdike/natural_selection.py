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
   dN/dt of Steps will grow, c of Steps will die.


"""

# We can manipulate this value for our purpose.

# Carrying capacity of the environment.
K = 10

# Death rate.
c = 0.1


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

    # Count TN, the number of Step instances w/ *next state*


    # Determine votable, creatable

    # If TN < 1
    #   votable: False, creatable: True

    # If 1 <= TN < K
    #   votable: True, creatable: True

    # If TN >= K
    #   votable: True, creatable: False


    # Make step_list

    # If votable == True
    #   step_list = list of Steps (state_next) in descending order by votes

    # If votable == False
    #   step_list = None


    # Return dictionary


def change_populations():
    """Make Steps grow and die.

    dN/dt of Steps will grow, c of Steps will die.
    :return: Boolean whether the total population is greater or equal to K.
    """

    # In iterations of all Steps,
    # Add dN/dt, substract c to Step.population

    # return TN >= K

