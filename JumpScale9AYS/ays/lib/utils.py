"""
Utilites modules for ays libs
"""

import re

def validate_service_name(name):
    """
    Validates that services have valid name

    Returns a tuple of (True/False, message)
    """
    message = ''
    if not re.sub("[-_.]", "", name).isalnum():
        message = "Service instance name should be digits or alphanumeric. you passed [%s]" % name
        return False, message
    return True, message
