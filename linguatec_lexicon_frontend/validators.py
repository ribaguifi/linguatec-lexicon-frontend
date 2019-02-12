from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_balanced_parenthesis(value):
    # https://leetcode.com/problems/valid-parentheses/
    """
    :type value: str
    :rtype: bool
    """
    stack = []
    # Hash map for keeping track of mappings.
    mapping = {")": "("}
    for char in value:
        # If the character is an closing bracket
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                raise ValidationError(_('Unbalanced parenthesis!'))
        elif char in mapping.values():
            # We have an opening bracket
            stack.append(char)

    # In the end, if the stack has elements, then we have an invalid expression.
    if stack:
        raise ValidationError(_('Unbalanced parenthesis!'))
    return value
