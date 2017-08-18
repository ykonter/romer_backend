""" The til module
by Yuri
"""

def run_once(f):
    """elegant decorator to run functions only once in lifetime
    """
    res = False
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.result = f(*args, **kwargs)
            wrapper.has_run = True
        return wrapper.result
    wrapper.has_run = False  # this peace of code is runned at creation.
    return wrapper

def cleanse_dict(input_dictionary):
    # prepare dict for insertion into firebase (no timestamps)
    d=dict()
    for key, value in input_dictionary.items():
        d[key] = str(value)
    return d
