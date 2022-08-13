import pybreaker
from config import config


# 可以在熔断器上添加侦听器，如果出现熔断，会被侦听到
class FuncListener(pybreaker.CircuitBreakerListener):
    "Listener used by circuit breakers that execute database operations."

    def before_call(self, cb, func, *args, **kwargs):
        "Called before the circuit breaker `cb` calls `func`."
        pass

    def state_change(self, cb, old_state, new_state):
        "Called when the circuit breaker `cb` state changes."
        pass

    def failure(self, cb, exc):
        "Called when a function invocation raises a system error."
        print("1min内请求错误次数大于5次,出现熔断...")

    def success(self, cb):
        "Called when a function invocation succeeds."
        pass


# 熔断机制
# 在60s内请求错误次数达到5次,进行熔断
# 通过模块的方式导出,成为一个单例，全局使用
breaker = pybreaker.CircuitBreaker(fail_max=config.FAIL_MAX, reset_timeout=config.RESET_TIMEOUT)
breaker.add_listeners(FuncListener(),)
