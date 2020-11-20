def view_function_timer(prefix='', writeto=print):

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                t0 = time.time()
                return func(*args, **kwargs)
            finally:
                t1 = time.time()
                writeto(
                    'View Function',
                    '({})'.format(prefix) if prefix else '',
                    func.__name__,
                    args[1:],
                    'Took',
                    '{:.2f}ms'.format(1000 * (t1 - t0)),
                    args[0].build_absolute_uri(),
                )
        return inner

    return decorator
