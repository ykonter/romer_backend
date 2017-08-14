""" The til module
by Yuri
"""

def run_once(f):
    """elegant decorator to run functions only once in lifetime
    """
    res = False
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
             wrapper.has_run = True
             wrapper.result = f(*args, **kwargs)
        return wrapper.result
    wrapper.has_run = False  # this peace of code is runned at creation.
    return wrapper
