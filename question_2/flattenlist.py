"""Flattens a list of nested lists into a one dimensional list."""


def flatten_list(input_list):
    """Flattens a list of lists into a single list.

    Note: Although this problem lends itself to a recursive solution, the Python
    stack size is low by default. It is possible to increase the stack size,
    but to make the function more rigorous, I have implemented the
    iterative solution.

    Args:
        input_list: A list of lists containing any type of element.

    Returns:
        A list with all the elements of the input list without any nested lists.
    """
    stack = [input_list]
    result = []
    while len(stack) > 0:
        current_element = stack.pop()
        if isinstance(current_element, list):
            # Add elements to the stack from current_element from end to start.
            for index in xrange(len(current_element)-1, -1, -1):
                stack.append(current_element[index])
        else:
            result.append(current_element)
    return result
