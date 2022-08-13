from functools import wraps

from ratelimit.decorators import RateLimitDecorator
import time

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
                    return func(*args, **kargs)

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


import requests

FIFTEEN_MINUTES = 900


@MyRateLimitDecorator(calls=5, period=FIFTEEN_MINUTES)
def call_api(url, *args, **kwargs):
    if "is_exception" in kwargs:
        print("kwargs", "请求次数过多，请稍后重试！")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))

    return response


if __name__ == '__main__':
    for i in range(20):
        call_api("http://www.baidu.com")
