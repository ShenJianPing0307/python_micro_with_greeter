from functools import wraps
from ratelimit.decorators import RateLimitDecorator
import time

# Use monotonic time if available, otherwise fall back to the system clock.
now = time.monotonic if hasattr(time, 'monotonic') else time.time


class MyRateLimitDecorator(RateLimitDecorator):

    def __call__(self, func):
        '''
        Return a wrapped function that prevents further function invocations if
        previously called within a specified period of time.

        :param function func: The function to decorate.
        :return: Decorated function.
        :rtype: function
        '''

        @wraps(func)
        def wrapper(*args, **kargs):
            '''
            Extend the behaviour of the decoated function, forwarding function
            invocations previously called no sooner than a specified period of
            time. The decorator will raise an exception if the function cannot
            be called so the caller may implement a retry strategy such as an
            exponential backoff.

            :param args: non-keyword variable length argument list to the decorated function.
            :param kargs: keyworded variable length argument list to the decorated function.
            :raises: RateLimitException
            '''
            with self.lock:
                period_remaining = self.__period_remaining()

                # If the time window has elapsed then reset.
                if period_remaining <= 0:
                    self.num_calls = 0
                    self.last_reset = self.clock()

                # Increase the number of attempts to call the function.
                self.num_calls += 1

                # If the number of attempts to call the function exceeds the
                # maximum then raise an exception.
                if self.num_calls > self.clamped_calls:
                    if self.raise_on_limit:
                        kargs['is_exception'] = True
                    return func(*args, **kargs)  # 自定义实现，为了捕捉装饰器中抛出的异常

            return func(*args, **kargs)

        return wrapper

    def __period_remaining(self):
        '''
        Return the period remaining for the current rate limit window.

        :return: The remaing period.
        :rtype: float
        '''
        elapsed = self.clock() - self.last_reset
        return self.period - elapsed


limits = MyRateLimitDecorator
