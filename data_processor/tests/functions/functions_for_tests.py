"""
Functions used to help simplify tests
"""


def find_pop_and_return(looking_for, expected_list):
    """
    Takes in the expected list of items, looks for the item,
    if found returns the found item and the edited list
    :param expected_list: the list of what the expected test results should have
    :param looking_for: string of what should be in the list
    :return: the found item as a string and the edited list
    """

    for index, item in enumerate(expected_list):
        if looking_for == item:
            found_item = item
            expected_list.pop(index)
            return found_item, expected_list
