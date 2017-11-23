from webdike.models import *


"""
Design Goal

1. Users can see only two candidates for a vote because of a large amount of text.
2. Users can continue or stop each step immediately with their free will.
3. Most of the users' task results should be useful to the entire system.

"""

# We can manipulate this value for our purpose.
MAX_POOL = 10


def get_work_routing_info(sid, is_sentence=True):
    """Get information for routing works to users.

    Return value is a dictionary that contains
        votable -- Boolean: whether there're sufficient elements to vote, (N >= 1).
        creatable -- Boolean: whether there're places for new creation, (N < MAX_POOL).
        step_gen -- Generator: Generator of Step whose state is state_next
    where
        state_current -- Integer: state of Sentence(sid).
        state_next -- Integer: state_current + 1.
        N -- Integer: the number of Step whose state is state_next.

    :param sid: integer id of sentence.
    :param is_sentence: boolean
    :return: dictionary {votable, creatable, step_gen}

    """

    # Find Sentence or Step from sid w/ is_sentence

    # Count N, the number of Step instances w/ *next state*


    # Determine votable, creatable

    # If N < 1
    #   votable: False, creatable: True

    # If 1 <= N < MAX_POOL
    #   votable: True, creatable: True

    # If N >= MAX_POOL
    #   votable: True, creatable: False


    # Make step_gen

    # If votable == True
    #   step_gen = generator which yields Step (state_next) in descending order by votes

    # If votable == False
    #   step_gen = None


    # Return dictionary


def select_survived(sid):
    """Pick the Step as a new starting point & update state of Sentence(sid)

    Return value is Tuple T (Boolean B, Step S)
        B -- Boolean: whether natural selection succeed
        S -- Step: Step instance as a starting point

    :param sid: Integer id of sentence.
    :return: Tuple T (B, S)

    """

    # Find Sentence or Step from sid w/ is_sentence

    # Get list of Step instances w/ *next state*

    # Determine B, whether natural selection succeed
    # TODO Make criteria w/ votes

    # Get Step instance S
    # If B == True, S is a new starting point, and update the value
    # Else, S is same as a previous starting point


def select_extinct(sid):
    """

    This is an advanced feature of natural selection algorithm.

    Return value is Tuple T (Boolean B, listof Step LS)
        B -- Boolean: whether natural selection succeed
        LS -- listof Step: List of Step instances which will be delete from the pool

    :param sid: Integer id of sentence.
    :return: Tuple T (B, LS)

    """

    raise NotImplementedError

