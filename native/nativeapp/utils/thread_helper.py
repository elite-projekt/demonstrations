import threading


def lock_function(func):
    """
    Only allows the function to be called by one thread at a time
    """
    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper
